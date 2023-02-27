-- GNU AGPL v3 License
-- Written by John Nunley

DROP TABLE IF EXISTS apps;
DROP TABLE IF EXISTS vulnerabilities;
DROP TABLE IF EXISTS vuln_mapping;

CREATE TABLE apps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_name TEXT NOT NULL,
    app_id TEXT NOT NULL,
    icon TEXT NOT NULL,
    developer TEXT NOT NULL,
    category TEXT NOT NULL,
    summary TEXT NOT NULL,
    analysis_state INTEGER NOT NULL 
);

CREATE TABLE vulnerabilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vulnname TEXT NOT NULL,
    owasp_mobile TEXT NOT NULL,
    cwe TEXT NOT NULL,
    descript TEXT NOT NULL,
    severity TEXT NOT NULL
);

CREATE TABLE vuln_mapping (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_id INTEGER NOT NULL,
    vuln_id INTEGER NOT NULL,
    FOREIGN KEY (app_id) REFERENCES analyzed_apps(id),
    FOREIGN KEY (vuln_id) REFERENCES vulnerabilities(id)
);
