-- SQL USED FOR POPDB SCHEMA MIGRATION ON 2015-05-24
-- NOT TO BE USED FOR A FRESH SCHEMA DEPLOYMENT
-- TO DEPLOY SCHEMA FROM SCRATCH, RUN CreateMVTable 
-- and CreateMVDSStat1

DROP MATERIALIZED VIEW MV_DS_stat0;

CREATE MATERIALIZED VIEW MV_DS_stat0
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
REFRESH FAST
ENABLE QUERY REWRITE
AS
select  trunc(finishedtimestamp) as TDay , siteName, userid, inputcollection as collName, isRemote,
 submissiontool, 
 count(*) as numAccesses, sum(CPUTIME) as totCPU
from raw_file 
where fileexitflag=1
GROUP BY trunc(finishedtimestamp), siteName, userid, inputcollection, isRemote, submissiontool
;

CREATE MATERIALIZED VIEW MV_DS_stat1_aggr1
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay , siteName, collName, 
sum(numAccesses) as numAccesses, sum(totCPU) as totCPU, count(distinct userid) as numUsers
from  MV_DS_stat0
where submissiontool!='wmagent'
GROUP BY TDay, siteName, collName
;

CREATE MATERIALIZED VIEW MV_DS_stat1_aggr1_summ
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay , collName, 
sum(numAccesses) as numAccesses, sum(totCPU) as totCPU, count(distinct userid) as numUsers
from  MV_DS_stat0
where submissiontool!='wmagent'
GROUP BY TDay, collName
;

CREATE MATERIALIZED VIEW MV_DS_stat1_aggr2
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay , siteName, substr(collName,INSTR(collName, '/',-1)+1) as collName, 
sum(numAccesses) as numAccesses, sum(totCPU) as totCPU, count (distinct userid) as numUsers
from  MV_DS_stat0
where submissiontool!='wmagent'
GROUP BY TDay, siteName, substr(collName,INSTR(collName, '/',-1)+1)
;

CREATE MATERIALIZED VIEW MV_DS_stat1_aggr2_summ
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay ,  substr(collName,INSTR(collName, '/',-1)+1) as collName, 
sum(numAccesses) as numAccesses, sum(totCPU) as totCPU, count (distinct userid) as numUsers
from  MV_DS_stat0
where submissiontool!='wmagent'
GROUP BY TDay, substr(collName,INSTR(collName, '/',-1)+1)
;

CREATE MATERIALIZED VIEW MV_DS_stat1_aggr4
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay , siteName, 
substr(collname,INSTR(collname, '/',-1,2)+1,INSTR(collname, '/',-1,1)-INSTR(collname, '/',-1,2)-1) as collName,
sum(numAccesses) as numAccesses, sum(totCPU) as totCPU, count (distinct userid) as numUsers
from  MV_DS_stat0
where 
substr(collname,INSTR(collname, '/',-1,1)+1) not like 'USER'
and 
collname not like 'unknown'
and submissiontool!='wmagent'
GROUP BY TDay, siteName, substr(collname,INSTR(collname, '/',-1,2)+1,INSTR(collname, '/',-1,1)-INSTR(collname, '/',-1,2)-1)
;

CREATE MATERIALIZED VIEW MV_DS_stat1_aggr4_summ
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay ,  
substr(collname,INSTR(collname, '/',-1,2)+1,INSTR(collname, '/',-1,1)-INSTR(collname, '/',-1,2)-1) as collName,
sum(numAccesses) as numAccesses, sum(totCPU) as totCPU, count (distinct userid) as numUsers
from  MV_DS_stat0
where 
substr(collname,INSTR(collname, '/',-1,1)+1) not like 'USER'
and 
collname not like 'unknown'
and submissiontool!='wmagent'
GROUP BY TDay, substr(collname,INSTR(collname, '/',-1,2)+1,INSTR(collname, '/',-1,1)-INSTR(collname, '/',-1,2)-1)
;

grant select on MV_DS_STAT1_AGGR1 to CMS_POPULARITY_SYSTEM_R;
grant select on MV_DS_STAT1_AGGR1_SUMM to CMS_POPULARITY_SYSTEM_R;
grant select on MV_DS_STAT1_AGGR2 to CMS_POPULARITY_SYSTEM_R;
grant select on MV_DS_STAT1_AGGR2_SUMM to CMS_POPULARITY_SYSTEM_R;
grant select on MV_DS_STAT1_AGGR4 to CMS_POPULARITY_SYSTEM_R;
grant select on MV_DS_STAT1_AGGR4_SUMM to CMS_POPULARITY_SYSTEM_R;

grant select, insert, update, delete on MV_DS_STAT1_AGGR1 to CMS_POPULARITY_SYSTEM_W;
grant select, insert, update, delete on MV_DS_STAT1_AGGR1_SUMM to CMS_POPULARITY_SYSTEM_W;
grant select, insert, update, delete on MV_DS_STAT1_AGGR2 to CMS_POPULARITY_SYSTEM_W;
grant select, insert, update, delete on MV_DS_STAT1_AGGR2_SUMM to CMS_POPULARITY_SYSTEM_W;
grant select, insert, update, delete on MV_DS_STAT1_AGGR4 to CMS_POPULARITY_SYSTEM_W;
grant select, insert, update, delete on MV_DS_STAT1_AGGR4_SUMM to CMS_POPULARITY_SYSTEM_W;
