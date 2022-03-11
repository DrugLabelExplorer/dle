USE drug_label_explorer;

LOAD DATA INFILE '/sample_record.csv'
INTO TABLE drug_labels
FIELDS TERMINATED BY ','
IGNORE 1 ROWS
(source, generic_name,   brand_name,application_num,schedule,ndc,unii,set_id,characteristics,manufactuer,label,class,marketing_categories,country,version);

SELECT * FROM drug_labels;
