--- aggregation: day, sitename, dataset
--- exclude production
--- count distinct users per day, aggregating later more days will 
--- double count the same users that submitted in several days
--- FIXME: CURRENTLY QUERYING MV_DS_STAT1 FOR TESTING
--- SHOULD QUERY MV_DS_STAT0 EVENTUALLY

CREATE MATERIALIZED VIEW MV_DS_stat1_aggr1
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay , siteName, collName, 
sum(numAccesses) as numAccesses, sum(totCPU) as totCPU, count(distinct userid) as numUsers
from  MV_DS_stat1
where submissiontool!='wmagent'
GROUP BY TDay, siteName, collName
;

--- aggregation: day, dataset                                                                                                                                                      
--- exclude production
--- count distinct users per day, aggregating later more days will                                                                                                                            
--- double count the same users that submitted in several days
--- FIXME: CURRENTLY QUERYING MV_DS_STAT1 FOR TESTING                                                                                                                                         
--- SHOULD QUERY MV_DS_STAT0 EVENTUALLY       

CREATE MATERIALIZED VIEW MV_DS_stat1_aggr1_summ
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay , collName, 
sum(numAccesses) as numAccesses, sum(totCPU) as totCPU, count(distinct userid) as numUsers
from  MV_DS_stat1
where submissiontool!='wmagent'
GROUP BY TDay, collName
;

commit;