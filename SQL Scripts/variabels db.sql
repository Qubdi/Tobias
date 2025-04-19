-- Table: variables
CREATE TABLE variables (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    calculation_type VARCHAR(10) NOT NULL, -- 'live', 'dwh', 'hybrid'
    is_active BOOLEAN DEFAULT 1,
    created_by VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table: variable_versions
CREATE TABLE variable_versions (
    id INTEGER PRIMARY KEY,
    variable_id INTEGER NOT NULL,
    version_number INTEGER NOT NULL,
    sql_script TEXT NOT NULL,
    change_reason TEXT,
    edited_by VARCHAR(50),
    edited_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (variable_id) REFERENCES variables(id) ON DELETE CASCADE,
    UNIQUE (variable_id, version_number)
);

-- Table: variable_results
CREATE TABLE variable_results (
    id INTEGER PRIMARY KEY,
    application_id VARCHAR(50) NOT NULL,
    variable_id INTEGER NOT NULL,
    value TEXT,
    calculated_by VARCHAR(50),
    calculated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (variable_id) REFERENCES variables(id) ON DELETE CASCADE,
    UNIQUE (application_id, variable_id)
);

-- Table: variable_executions
CREATE TABLE variable_executions (
    id INTEGER PRIMARY KEY,
    application_id VARCHAR(50) NOT NULL,
    variable_id INTEGER,
    executed_by VARCHAR(50),
    result TEXT,
    executed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (variable_id) REFERENCES variables(id)
);
