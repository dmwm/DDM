
--drop table T_CORRUPTEDFILES;
CREATE table T_investCORRUPTEDFILES 
(
TDAY Date DEFAULT to_date('2011/01/01 12:00:00am', 'yyyy/mm/dd hh:mi:ssam') NOT NULL, 
FLAG NUMBER(38,0) DEFAULT 0 NOT NULL, 
isRemote NUMBER(38,0) DEFAULT 0 NOT NULL,  
FILENAME VARCHAR2(400 BYTE) DEFAULT 'unknown' NOT NULL,
JobExitCode NUMBER(38,0) DEFAULT 0 NOT NULL, 
CONSTRAINT "T_CORRUPTEDFILES_UC_A" UNIQUE (TDAY, SITENAME, JobExitCode, FILENAME)
);

