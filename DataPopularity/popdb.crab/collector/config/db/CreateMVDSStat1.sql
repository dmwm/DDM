--- aggregation: day, sitename, dataset
--- exclude production
--- count distinct users per day, aggregating later more days will 
--- double count the same users that submitted in several days

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

--- aggregation: day, dataset                                                                                                                                                      
--- exclude production
--- count distinct users per day, aggregating later more days will                                                                                                                            
--- double count the same users that submitted in several days

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

--- aggregation: day, sitename, dataTier
--- count distinct users per day, aggregating later more days will 
--- double count the same users that submitted in several days
--- excludes wmagent jobs

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


--- aggregation: day, datatier
--- count distinct users per day, aggregating later more days will 
--- double count the same users that submitted in several days
--- excludes wmagent jobs

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


--- First aggregation: day, sitename, dataset namespace (ReReco, Summer2011, etc)
--- count distinct users per day, aggregating later more days will 
--- double count the same users that submitted in several days
--- excludes wmagent jobs

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


--- Second aggregation: day, dataset namespace (ReReco, Summer2011, etc)
--- count distinct users per day, aggregating later more days will 
--- double count the same users that submitted in several days
--- excludes wmagent jobs

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
