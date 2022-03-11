service mariadb restart
mysql -u root -e 'source database_setup.sql;'
mysql -u root -e 'source insert_record.sql;'
