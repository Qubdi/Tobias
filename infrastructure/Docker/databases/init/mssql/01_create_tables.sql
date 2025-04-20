USE tobias;
GO

CREATE TABLE variables (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    calculation_type VARCHAR(10) NOT NULL,
    is_active BIT DEFAULT 1,
    created_by VARCHAR(50),
    created_at DATETIME DEFAULT GETDATE()
);
GO

CREATE TABLE variable_versions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    variable_id INT NOT NULL,
    version_number INT NOT NULL,
    sql_script TEXT NOT NULL,
    change_reason TEXT,
    edited_by VARCHAR(50),
    edited_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT fk_variable FOREIGN KEY (variable_id) REFERENCES variables(id) ON DELETE CASCADE,
    CONSTRAINT uq_version UNIQUE (variable_id, version_number)
);
GO

CREATE TABLE variable_results (
    id INT IDENTITY(1,1) PRIMARY KEY,
    application_id VARCHAR(50) NOT NULL,
    variable_id INT NOT NULL,
    value TEXT,
    calculated_by VARCHAR(50),
    calculated_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT fk_var_result FOREIGN KEY (variable_id) REFERENCES variables(id) ON DELETE CASCADE,
    CONSTRAINT uq_result UNIQUE (application_id, variable_id)
);
GO

CREATE TABLE variable_executions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    application_id VARCHAR(50) NOT NULL,
    variable_id INT,
    executed_by VARCHAR(50),
    result TEXT,
    executed_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (variable_id) REFERENCES variables(id)
);
GO
