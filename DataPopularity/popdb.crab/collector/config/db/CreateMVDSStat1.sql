-----------------------------------------------------------------------
--- Unify Stat on DS
-----------------------------------------------------------------------

--- This MV allows analysis aggregation along time 
--- per DS and dataTier (RECO, AOD, etc), siteName, users 
--- Popularity is in number of accesses and totCPU
--- Selection is performed only on fileexitflag=1
--- FIXME: CURRENTLY DIFFERENT NAME FOR TESTING, SHOULD REPLACE
--- MV_DS_stat0 EVENTUALLY

CREATE MATERIALIZED VIEW MV_DS_stat1
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
commit;
