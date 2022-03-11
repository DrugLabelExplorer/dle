CREATE DATABASE IF NOT EXISTS drug_label_explorer;

USE drug_label_explorer;

CREATE TABLE IF NOT EXISTS drug_labels (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	source INT NOT NULL,  -- 0=FDA 1=EU
	generic_name VARCHAR(255),
	brand_name VARCHAR(255),
	application_num VARCHAR(255),  -- Includes letters
	schedule VARCHAR(255), -- May map to other table instead?
	ndc VARCHAR(255),
	unii VARCHAR(255),  -- Integers with dashes
	set_id VARCHAR(255),
	characteristics TEXT, -- includes multiple fields, color, shape etc.
	manufactuer VARCHAR(255),  -- may may to other table instead
	label TEXT,  -- largest section, may need to up size
	class VARCHAR(255),  -- need more info
	marketing_categories VARCHAR(255),  -- may map to other table
	country INT,  -- will map to other table, 0=USA
    version DATE,
	create_date DATETIME DEFAULT CURRENT_TIMESTAMP
	);
