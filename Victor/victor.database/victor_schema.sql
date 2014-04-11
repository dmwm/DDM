--- @copyright: European Organization for Nuclear Research (CERN)
--- @author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011-2012
--- @license: Licensed under the Apache License, Version 2.0 (the "License");
--- You may not use this file except in compliance with the License.
--- You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}


-- DROP TABLE t_cleaned_dataset;
-- DROP TABLE t_accounting_record;
-- DROP TABLE t_run_config;
-- DROP TABLE t_run_site;
-- DROP TABLE t_run;
-- DROP SEQUENCE seq_run;

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
-- Sequence to auto_increment the runId
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

CREATE SEQUENCE seq_run MINVALUE 1 START WITH 1 INCREMENT BY 1 NOCACHE ORDER NOCYCLE ;

-- GRANT SELECT ON seq_run TO CMS_CLEANING_AGENT_W;


--INSERT INTO t_run (runId) VALUES (seq_run.nextval)

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
-- Cleaning run
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

CREATE TABLE t_run (
    runId          NUMBER(8),
    runDate        DATE default sysdate,
    FINISHED	   NUMBER(1,0) DEFAULT 0,	
CONSTRAINT pk_RunId  PRIMARY KEY(runId)
);

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
-- Trigger to increment the runId
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 


-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
-- Cleaning run for a site
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

CREATE TABLE t_run_site (
    runId      NUMBER(8), 
    siteName   VARCHAR(256),
    cloud      VARCHAR(64) default NULL,
    tier       NUMBER(1)   default NULL,
CONSTRAINT fk_RunSiteId  FOREIGN KEY(runId) REFERENCES t_run(runId),
CONSTRAINT pk_RunSiteId  PRIMARY KEY(runId, siteName)
);

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
-- Accounting record
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

CREATE TABLE t_accounting_record (
    total               NUMBER(20), 
    used                NUMBER(20), 
    toBeDeleted         NUMBER(20), 
    inDeletionQueue     NUMBER(20), 
    newlyCleaned        NUMBER(20),
    runId               NUMBER(8), 
    siteName            VARCHAR(256),
CONSTRAINT fk_AccountingRecord FOREIGN KEY(runId, siteName) REFERENCES t_run_site(runId, siteName),
CONSTRAINT pk_AccountingRecord PRIMARY KEY(runId, siteName)
);

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
-- Cleaned dataset/block
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

CREATE TABLE t_cleaned_dataset (
    dsn                VARCHAR(512),  --Dataset name          
    cont               VARCHAR(512) default NULL,
    rcdate             DATE,
    dsSize             NUMBER(15), --1TB as maximum dataset size should be enough
    nAcc               NUMBER(8),  --ATLAS: normalized file accesses | CMS: file accesses
    cpuTime            NUMBER(12,2) default NULL,  -- Only available for CMS CRAB jobs
    runId              NUMBER(8),
    nBlock             NUMBER(8) default NULL,
    maxAccsCont        NUMBER(8) default NULL, 
    totalAccsCont      NUMBER(8)default NULL,
    siteName           VARCHAR(256),
CONSTRAINT fk_CleanedDataset FOREIGN KEY(runId, siteName) REFERENCES t_run_site(runId, siteName),
CONSTRAINT pk_CleanedDataset PRIMARY KEY(dsn, runId, siteName)
);

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
-- Cleaning run config
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

CREATE TABLE T_RUN_CONFIG (
    RUNID              NUMBER(8,0),
    SPACETOKEN         VARCHAR2(256 BYTE),
    FREERATIO          NUMBER(3,2),
    FREEABSOLUTE       NUMBER(15,0),
    FREETARGETRATIO    NUMBER(3,2),
    FREETARGETABSOLUTE NUMBER(15,0),
    CONSTRAINT PK_RUNCONFIGID PRIMARY KEY (RUNID, SPACETOKEN) ,
    CONSTRAINT FK_RUNCONFIGID FOREIGN KEY (RUNID) REFERENCES T_RUN(RUNID)
); 

CREATE INDEX runid_index ON t_cleaned_dataset (runId);

------------------------------------------------------------

GRANT SELECT ON T_ACCOUNTING_RECORD TO CMS_CLEANING_AGENT_R;
GRANT SELECT ON T_RUN               TO CMS_CLEANING_AGENT_R;
GRANT SELECT ON T_RUN_SITE          TO CMS_CLEANING_AGENT_R;
GRANT SELECT ON T_CLEANED_DATASET   TO CMS_CLEANING_AGENT_R;
GRANT SELECT ON T_RUN_CONFIG        TO CMS_CLEANING_AGENT_R;
commit;
