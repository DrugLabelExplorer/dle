from bs4 import BeautifulSoup
from contextlib import closing
from datetime import datetime, timedelta
import logging
import re
import shutil
import urllib.request as request
import os
from zipfile import ZipFile
from distutils.util import strtobool

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.utils import IntegrityError, OperationalError

from data.models import DrugLabel, LabelProduct, ProductSection
from users.models import MyLabel
from data.constants import FDA_SECTION_NAME_MAP

logger = logging.getLogger(__name__)

# python manage.py load_fda_data --type test --cleanup False --insert False --count_titles True
# python manage.py load_fda_data --type my_label --my_label_id 9 --cleanup False --insert False
# runs with `python manage.py load_fda_data --type {type}`
class Command(BaseCommand):
    help = "Loads data from FDA"
    re_combine_whitespace = re.compile(r"\s+")
    re_remove_nonalpha_characters = re.compile("[^a-zA-Z ]")

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        root_logger = logging.getLogger("")
        root_logger.setLevel(logging.INFO)

        self.root_dir = settings.MEDIA_ROOT / "fda"
        os.makedirs(self.root_dir, exist_ok=True)
        super().__init__(stdout, stderr, no_color, force_color)

    def add_arguments(self, parser):
        parser.add_argument(
            "--type", type=str, help="full, monthly, test or my_label", default="monthly"
        )
        parser.add_argument(
            "--insert", type=strtobool, help="Set to connect to DB", default=True
        )
        parser.add_argument(
            "--cleanup", type=strtobool, help="Set to cleanup files", default=False
        )
        parser.add_argument(
            "--my_label_id", type=int, help="set my_label_id for --type my_label", default=None
        )
        parser.add_argument(
            "--count_titles", type=strtobool, help="output counts of the section_names", default=False
        )

    """
    Entry point into class from command line
    """

    def handle(self, *args, **options):
        import_type = options["type"]
        insert = options["insert"]
        cleanup = options["cleanup"]
        my_label_id = options["my_label_id"]
        count_titles = options["count_titles"]
        logger.debug(f"options: {options}")

        # my_label type already has the xml uploaded/downloaded
        if import_type == "my_label":
            record_zips = []
            xml_files = []
        else:
            root_zips = self.download_records(import_type)
            record_zips = self.extract_prescription_zips(root_zips)
            xml_files = self.extract_xmls(record_zips)

        if count_titles:
            self.count_titles(xml_files)

        self.import_records(xml_files, insert, my_label_id)

        if cleanup:
            self.cleanup(record_zips)
            self.cleanup(xml_files)

        logger.info("DONE")

    # Test function for data exploration
    def get_names(self, xml_files):
        unapproved_count = 0
        exception_count = 0
        total_count = 0
        for xml_file in xml_files:
            total_count += 1
            with open(xml_file) as f:
                content = BeautifulSoup(f.read(), "lxml")
                product_name = ""
                generic_name = ""
                try:
                    product_name = content.find("subject").find("name").text.upper()
                    generic_name = content.find("genericmedicine").find("name").text
                    unapproved_bool = False
                    approval = content.find("approval")
                    if approval is not None:
                        for code in approval.find_all("code"):
                            if "unapproved" in code.get("displayname", "").lower():
                                unapproved_bool = True
                except Exception as e:
                    print(e)
                    exception_count +=1
                if unapproved_bool:
                    unapproved_count += 1
                    print(f"{product_name:50}\t{generic_name:50}\t{str(xml_file).split('/')[-1]}")
            if total_count % 100 == 0:
                print(f"{unapproved_count}:{len(xml_files)}\t{exception_count}")

        print(f"{unapproved_count}:{len(xml_files)}\t{exception_count}")

    def download_records(self, import_type):
        logger.info("Downloading bulk archives.")
        file_dir = self.root_dir / import_type
        os.makedirs(file_dir, exist_ok=True)
        records = []

        if import_type == "full":
            for i in range(1, 5):
                archive_url = f"ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_release_human_rx_part{i}.zip"
                records.append(self.download_single_zip(archive_url, file_dir))
        elif import_type == "monthly":
            now = datetime.now()
            prev_month_lastday = now.replace(day=1) - timedelta(days=1)
            month, year = (
                prev_month_lastday.strftime("%b").lower(),
                prev_month_lastday.year,
            )
            archive_url = f"ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_monthly_update_{month}{year}.zip"
            records.append(self.download_single_zip(archive_url, file_dir))
        elif import_type == "test":
            archive_url = f"ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_daily_update_10262021.zip"
            records.append(self.download_single_zip(archive_url, file_dir))
            archive_url = f"ftp://public.nlm.nih.gov/nlmdata/.dailymed/dm_spl_daily_update_10182021.zip"
            records.append(self.download_single_zip(archive_url, file_dir))
        else:
            raise CommandError("Type must be one of 'full', 'monthly', or 'test'")

        return records

    def download_single_zip(self, ftp, dest):
        url_filename = ftp.split("/")[-1]
        file_path = dest / url_filename

        if os.path.exists(file_path):
            logger.info(f"File already exists: {file_path}. Skipping.")
            return file_path

        # Download the drug labels archive file
        with closing(request.urlopen(ftp)) as r:
            with open(file_path, "wb") as f:
                logger.info(f"Downloading {ftp} to {file_path}")
                shutil.copyfileobj(r, f)
        return file_path

    """
    Daily Med will package it's bulk and monthly into groups of zips. This step is neccesary to
    extract individual drug label zips from the bulk archive.
    """

    def extract_prescription_zips(self, zips):
        logger.info("Extracting prescription Archives")
        file_dir = self.root_dir / "record_zips"
        os.makedirs(file_dir, exist_ok=True)
        record_zips = []

        for zip_file in zips:
            with ZipFile(zip_file, "r") as zip_file_object:
                for file_info in zip_file_object.infolist():
                    if file_info.filename.startswith(
                        "prescription"
                    ) and file_info.filename.endswith(".zip"):
                        outfile = file_dir / os.path.basename(file_info.filename)
                        file_info.filename = os.path.basename(file_info.filename)
                        if os.path.exists(outfile):
                            logger.info(
                                f"Record Zip already exists: {outfile}. Skipping."
                            )
                        else:
                            logger.info(f"Creating Record Zip {outfile}")
                            zip_file_object.extract(file_info, file_dir)
                        record_zips.append(outfile)
        return record_zips

    def extract_xmls(self, zips):
        logger.info("Extracting XMLs")
        file_dir = self.root_dir / "xmls"
        os.makedirs(file_dir, exist_ok=True)
        xml_files = []

        for zip_file in zips:
            with ZipFile(zip_file, "r") as zip_file_object:
                for file in zip_file_object.namelist():
                    if file.endswith(".xml"):
                        outfile = file_dir / file
                        if os.path.exists(outfile):
                            logger.info(f"XML already exists: {outfile}. Skipping.")
                        else:
                            logger.info(f"Creating XML {outfile}")
                            zip_file_object.extract(file, file_dir)
                        xml_files.append(outfile)
        return xml_files

    def count_titles(self, xml_records):
        titles = []
        for xml_file in xml_records:
            try:
                with open(xml_file) as f:
                    content = BeautifulSoup(f.read(), "lxml")

                    for section in content.find_all("component"):
                        # the structuredbody component is the parent that contains everything, skip it
                        structured_body = section.find_next("structuredbody")
                        if structured_body is not None:
                            logger.debug(f"SKIPPING: structuredbody")
                            continue

                        code = section.find(
                            "code", attrs={"codesystem": "2.16.840.1.113883.6.1"}
                        )
                        if code is None:
                            continue
                        title = str(code.get("displayname")).upper()
                        if title == "SPL UNCLASSIFIED SECTION":
                            try:
                                title = code.find_next_sibling().get_text(strip=True)
                                logger.debug(f"UNCLASSIFIED title: {title}")
                            except AttributeError:
                                pass
                        title = self.re_combine_whitespace.sub(" ", title).strip()
                        title = self.re_remove_nonalpha_characters.sub("", title)
                        title = self.re_combine_whitespace.sub(" ", title).strip()

                        titles.append(title)
            except Exception as e:
                logger.error("Error")
                raise e

        import collections

        counter = collections.Counter(titles)
        logger.info(counter.most_common(10))
        import csv

        with open("top_displaynames.csv", "w") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["displayname", "count"])
            csvwriter.writerows(counter.most_common(3000))

    def import_records(self, xml_records, insert, my_label_id):
        logger.info("Building Drug Label DB records from XMLs")

        if len(xml_records) == 0 and my_label_id is not None:
            logger.info(f"processing my_label_id: {my_label_id}")
            ml = MyLabel.objects.filter(pk=my_label_id).get()
            xml_file = ml.file.path
            dl = ml.drug_label
            self.process_xml_file(xml_file, insert, dl, my_label_id)
            # TODO better way to know if the process_xml_file was successful
            ml.is_successfully_parsed = True
            ml.save()
        else:
            for xml_file in xml_records:
                try:
                    dl = DrugLabel()
                    self.process_xml_file(xml_file, insert, dl, my_label_id)
                except Exception as e:
                    logger.error(f"Could not parse {xml_file}")
                    logger.error(str(e))
                    continue


    def process_xml_file(self, xml_file, insert, dl, my_label_id=None):
        logger.debug(f"insert: {insert}")
        with open(xml_file) as f:
            content = BeautifulSoup(f.read(), "lxml")

            # Skip unapproved drug labels
            if self.check_if_unapproved(content):
                logger.info(f"Skipping {xml_file} because it is not approved")
                return

            dl.source = "FDA"
            dl.product_name = content.find("subject").find("name").text.title()
            try:
                generic_name = content.find("genericmedicine").find("name").text
            except AttributeError:
                # don't insert record if we cannot find this
                logger.error("unable to find generic_name")
                return
            dl.generic_name = generic_name[:255].title()

            try:
                dl.version_date = datetime.strptime(
                    content.find("effectivetime").get("value"), "%Y%m%d"
                )
            except ValueError:
                dl.version_date = datetime.now()

            try:
                dl.marketer = content.find("author").find("name").text.title()
            except AttributeError:
                dl.marketer = ""

            # Ensure always selecting the same ndc code if multiple
            ndc_codes = [ndc_code.get("code") for ndc_code in content.find_all("code", attrs={"codesystem": "2.16.840.1.113883.6.69"})]
            dl.source_product_number = sorted(ndc_codes)[0]
            
            
            if my_label_id is not None:
                dl.source_product_number = f"my_label_{my_label_id}" + dl.source_product_number

            # texts = [p.text for p in content.find_all("paragraph")]
            # dl.raw_text = "\n".join(texts)
            dl.raw_rext = ""

            lp = LabelProduct(drug_label=dl)

            root = content.find("setid").get("root")
            dl.link = f"https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={root}"

            try:
                if insert:
                    dl.save()
                    logger.info(f"Saving new drug label: {dl}")
            except IntegrityError as e:
                logger.error(str(e))
                return

            try:
                if insert:
                    lp.save()
                    logger.info(f"Saving new label product")
            except IntegrityError as e:
                logger.error(str(e))
                return

            # In the following section we will build the different sections. We do this by matching XML components
            # to predetermined FDA_SECTION_NAMES, and for components that do not match, we add them to an "OTHER"
            # category
            section_map = {}
            for section in content.find_all("component"):
                # the structuredbody component is the parent that contains everything, skip it
                structured_body = section.find_next("structuredbody")
                if structured_body is not None:
                    logger.debug(f"SKIPPING: structuredbody")
                    continue
                logger.debug(f"section: {repr(section)}")

                code = section.find(
                    "code", attrs={"codesystem": "2.16.840.1.113883.6.1"}
                )
                if code is None:
                    continue

                title = str(code.get("displayname")).upper()
                logger.debug(f"title: {title}")

                if title == "SPL UNCLASSIFIED SECTION":
                    try:
                        title = code.find_next_sibling().get_text(strip=True)
                        logger.debug(f"UNCLASSIFIED title: {title}")
                    except AttributeError:
                        pass

                title = self.re_combine_whitespace.sub(" ", title).strip()
                title = self.re_remove_nonalpha_characters.sub("", title)
                title = self.re_combine_whitespace.sub(" ", title).strip()

                if title not in FDA_SECTION_NAME_MAP.keys():
                    section_name = "OTHER"
                else:
                    section_name = FDA_SECTION_NAME_MAP[title]

                # Now that we have determined what section, grab all the text in the component and add it as the
                # value to a corresponding hashmap. If a value already exists, add it to the end
                raw_section_texts = [str(p) for p in section.find_all("text")]
                section_texts = "<br>".join(raw_section_texts)
                logger.debug(f"section_texts: {section_texts}")

                # Save other titles in section text
                if section_name == "OTHER":
                    section_texts = title + "<br>" + section_texts

                # Save to keyed section of map, concatenating repeat sections
                if section_map.get(section_name) is None:
                    section_map[section_name] = section_texts
                else:
                    if section_name != "OTHER":
                        logger.debug(
                            f"Found another section: {section_name}\twith title\t{title}"
                        )
                    section_map[section_name] = (
                            section_map[section_name]
                            + f"<br>{title}<br>"
                            + section_texts
                    )

            # Now that the sections have been parsed, save them
            for section_name, section_text in section_map.items():
                ps = ProductSection(
                    label_product=lp,
                    section_name=section_name.title(),
                    section_text=section_text,
                )
                try:
                    if insert:
                        ps.save()
                        logger.debug(f"Saving new product section {ps}")
                except IntegrityError as e:
                    logger.error(str(e))
                except OperationalError as e:
                    logger.error(str(e))

    def check_if_unapproved(self, content):
        try:
            approval = content.find("approval")
            if approval is not None:
                for code in approval.find_all("code"):
                    if "unapproved" in code.get("displayname", "").lower():
                        return True  # It is unapproved
        except Exception as e:
            logger.warning(e)
        return False  # Otherwise assume it is approved

    def cleanup(self, files):
        for file in files:
            logger.debug(f"remove: {file}")
            os.remove(file)
