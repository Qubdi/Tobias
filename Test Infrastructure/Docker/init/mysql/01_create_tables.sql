USE tobias;

CREATE TABLE variables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    calculation_type VARCHAR(10) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_by VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE variable_versions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    variable_id INT NOT NULL,
    version_number INT NOT NULL,
    sql_script TEXT NOT NULL,
    change_reason TEXT,
    edited_by VARCHAR(50),
    edited_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (variable_id) REFERENCES variables(id) ON DELETE CASCADE,
    UNIQUE (variable_id, version_number)
);

CREATE TABLE variable_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    application_id VARCHAR(50) NOT NULL,
    variable_id INT NOT NULL,
    value TEXT,
    calculated_by VARCHAR(50),
    calculated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (variable_id) REFERENCES variables(id) ON DELETE CASCADE,
    UNIQUE (application_id, variable_id)
);

CREATE TABLE variable_executions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    application_id VARCHAR(50) NOT NULL,
    variable_id INT,
    executed_by VARCHAR(50),
    result TEXT,
    executed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (variable_id) REFERENCES variables(id)
);
