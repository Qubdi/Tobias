-- DROP TABLES IF EXISTS
DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS payments;

-- CREATE TABLES
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    birthdate DATE,
    income INTEGER,
    gender TEXT,
    region TEXT
);

CREATE TABLE applications (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    status TEXT,
    created_at DATETIME
);

CREATE TABLE loans (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount INTEGER,
    status TEXT,
    opened_at DATETIME
);

CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    application_id INTEGER,
    customer_id INTEGER,
    amount INTEGER,
    days_late INTEGER,
    delay_flag INTEGER,
    paid_at DATETIME
);

-- SEED CUSTOMERS (100k)
WITH RECURSIVE c(x) AS (
  SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x < 100000
)
INSERT INTO customers (id, name, birthdate, income, gender, region)
SELECT
  x,
  'Customer_' || x,
  date('1970-01-01', '+' || (x % 10000) || ' days'),
  (RANDOM() % 5000) + 1000,
  CASE WHEN x % 2 = 0 THEN 'M' ELSE 'F' END,
  CASE x % 5
    WHEN 0 THEN 'East'
    WHEN 1 THEN 'West'
    WHEN 2 THEN 'South'
    WHEN 3 THEN 'North'
    ELSE 'Central' END
FROM c;

-- SEED APPLICATIONS (1M)
WITH RECURSIVE a(x) AS (
  SELECT 1 UNION ALL SELECT x+1 FROM a WHERE x < 1000000
)
INSERT INTO applications (id, customer_id, status, created_at)
SELECT
  x,
  ((RANDOM() % 100000) + 1),
  CASE x % 3
    WHEN 0 THEN 'pending'
    WHEN 1 THEN 'approved'
    ELSE 'rejected' END,
  datetime('now', '-' || (x % 365) || ' days')
FROM a;

-- SEED LOANS (2M)
WITH RECURSIVE l(x) AS (
  SELECT 1 UNION ALL SELECT x+1 FROM l WHERE x < 2000000
)
INSERT INTO loans (id, customer_id, amount, status, opened_at)
SELECT
  x,
  ((RANDOM() % 100000) + 1),
  (RANDOM() % 5000) + 500,
  CASE x % 4
    WHEN 0 THEN 'active'
    WHEN 1 THEN 'closed'
    ELSE 'default' END,
  datetime('now', '-' || (x % 1000) || ' days')
FROM l;

-- SEED PAYMENTS (5M)
WITH RECURSIVE p(x) AS (
  SELECT 1 UNION ALL SELECT x+1 FROM p WHERE x < 5000000
)
INSERT INTO payments (id, application_id, customer_id, amount, days_late, delay_flag, paid_at)
SELECT
  x,
  ((RANDOM() % 1000000) + 1),
  ((RANDOM() % 100000) + 1),
  (RANDOM() % 300) + 50,
  (RANDOM() % 60),
  CASE WHEN x % 5 = 0 THEN 1 ELSE 0 END,
  datetime('now', '-' || (x % 720) || ' hours')
FROM p;
