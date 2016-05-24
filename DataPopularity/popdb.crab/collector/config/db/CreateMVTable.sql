CREATE MATERIALIZED VIEW LOG ON raw_file WITH SEQUENCE, ROWID
(INSERTTIME,
FILENAME,
FILEEXITFLAG,
FILESIZE,
FILETYPE,
PROTOCOL,
ISPARENT,
ISREMOTE,
LUMIRANGE,
FILEEXECEXITCODE,
FILESTARTEDRUNNINGTIMESTAMP,
FILEFINISHEDTIMESTAMP,
FILERUNNINGTIME,
BLOCKID,
BLOCKNAME,
INPUTCOLLECTION,
APPLICATION,
TASKTYPE,
SUBMISSIONTOOL,
INPUTSE,
TARGETCE,
SITENAME,
SCHEDULERNAME,
JOBID,
JOBMONITORID,
TASKMONITORID,
TASKJOBID,
TASKID,
JOBEXECEXITCODE,
JOBEXECEXITTIMESTAMP,
STARTEDRUNNINGTIMESTAMP,
FINISHEDTIMESTAMP,
WALLCLOCKCPUTIME,
CPUTIME,
USERID,
USERNAME,
STRIPPEDFILES,
STRIPPEDBLOCKS,
STRIPPEDPARENTFILES,
STRIPPEDLUMIS
)
INCLUDING NEW VALUES;



create index log_snap_idx_detail on mlog$_RAW_FILE (snaptime$$);


------------------------------------------------------
--- DATA REDUCTION AGENT MVs VERSION 2
------------------------------------------------------

--
-- Modified time aggregation and information retrieved. adding the CPUtime and the accesses
--

--drop MATERIALIZED VIEW MV_block_stat0;

CREATE MATERIALIZED VIEW MV_block_stat0
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
REFRESH FAST
ENABLE QUERY REWRITE
AS
select  trunc(finishedtimestamp,'W') as TDay , siteName, blockname as collName, 
inputcollection as cont,
 count(*) as numAccesses, sum(CPUTIME) as totCPU
from raw_file 
where fileexitflag=1 and InputCollection != 'unknown'
GROUP BY trunc(finishedtimestamp,'W'), siteName, blockname, inputcollection
;


CREATE MATERIALIZED VIEW MV_block_stat0_aggr_5_weeks
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select Tday, sitename, collName, 
sum(numAccesses) as numAccesses, round(sum(totCPU),0) as totCPU
from MV_block_stat0 
where Tday > trunc(systimestamp - interval '35' day,'W') 
GROUP BY tday, sitename, collName;



CREATE MATERIALIZED VIEW MV_block_stat0_aggr_90_days
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select Tday, sitename, collName, 
sum(numAccesses) as numAccesses, round(sum(totCPU),0) as totCPU
from MV_block_stat0 
where Tday > trunc(systimestamp - interval '90' day,'W') 
GROUP BY tday, sitename, collName;

grant select on MV_block_stat0_aggr_90_days to CMS_POPULARITY_SYSTEM_R;

--drop MATERIALIZED VIEW  MV_block_stat0_aggr_180_days;
CREATE MATERIALIZED VIEW MV_block_stat0_aggr_180_days
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select Tday, sitename, collName, 
sum(numAccesses) as numAccesses, round(sum(totCPU),0) as totCPU
from MV_block_stat0 
where Tday > trunc(add_months(sysdate, -1) ,'W') 
GROUP BY tday, sitename, collName;

grant select on MV_block_stat0_aggr_180_days to CMS_POPULARITY_SYSTEM_R;

CREATE MATERIALIZED VIEW MV_block_stat0_aggr_12_months
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select Tday, sitename, collName, 
sum(numAccesses) as numAccesses, round(sum(totCPU),0) as totCPU
from MV_block_stat0 
where Tday > trunc(systimestamp - interval '12' month,'W') 
GROUP BY tday, sitename, collName;

grant select on MV_block_stat0_aggr_12_months to CMS_POPULARITY_SYSTEM_R;

--- TEST ---
select * from 
MV_block_stat0_aggr_5_weeks
--MV_block_stat0_aggr_90_days
where collname = '/MuOnia/Run2011B-PromptReco-v1/AOD#1cdc4096-e982-11e0-9718-003048caaace'
and sitename = 'T2_IT_Pisa'
;

----------------------------------------
---- FIND last access week for a dataset

--drop MATERIALIZED VIEW MV_block_stat0_last_access;

CREATE MATERIALIZED VIEW MV_block_stat0_last_access
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select max(Tday) as TDAY, sitename, collName
from MV_block_stat0 
GROUP BY sitename, collName;

grant select on MV_block_stat0_last_access to CMS_POPULARITY_SYSTEM_R;

--- TEST ---
select SITENAME, COLLNAME, tday, extract(day from TDAY-systimestamp) as nACC, 
 (tday - to_date('1970-01-01','YYYY-MM-DD')) * 86400,
 (tday - to_date('1970-01-01','YYYY-MM-DD')),
0 as TOTCPU 
from MV_block_stat0_last_access;
------

----------------------------------------
-- This part was intended to improve Victor. 
-- It contains selections, to evaluate the popularity of a DS.
-- At the end has not been used for Victor, the counters has been implemented in victor

create or replace view v_temporary_block as
select Tday, sitename, collName, 
  sum(numAccesses) as numAccesses,   sum(totCPU) as totcpu, 
  substr(collname,0,instr(collname,'#',1)) as cont
from MV_block_stat0 
GROUP BY Tday, sitename, collName, substr(collname,0,instr(collname,'#',1))
;

select * from v_temporary_block order by sitename, collname;


create or replace view v_accountDSpop_block as
select Tday, sitename, collName, 
  numAccesses,   totCPU, 
sum(numAccesses) OVER (partition by tday, sitename, cont) as naccDS,
round(sum(totcpu) OVER (partition by tday, sitename, cont),0) as totcpuDS 
from  v_temporary_block
where Tday > trunc(systimestamp - interval '35' day,'W') ;

select * from v_accountDSpop_block
where sitename like 'T2%'
order by sitename, tday, collname desc;

--drop MATERIALIZED VIEW MV_block_stat0_aggr_5_weeksBIS;
CREATE MATERIALIZED VIEW MV_block_stat0_aggr_5_weeksBIS
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select Tday, sitename, collName, naccDS, totcpuDS,
numAccesses, round(totCPU,0) as totCPU
from v_accountDSpop_block 
where Tday > trunc(systimestamp - interval '35' day,'W'); 

grant select on MV_block_stat0_aggr_5_weeksBIS to CMS_POPULARITY_SYSTEM_R;

----------------------------------------------------------------------
-- TEST
----------------------------------------------------------------------

select Tday, sitename, collName, naccDS, totcpuDS,
sum(numAccesses) as numAccesses, round(sum(totCPU),0) as totCPU
from v_accountDSpop_block 
where Tday > trunc(systimestamp - interval '35' day,'W') 
GROUP BY Tday, sitename, collName, naccDS, totcpuDS
minus
select * from  MV_block_stat0_aggr_5_weeksBIS
;

----------------------------------------------------------------------
----------------------------------------------------------------------
----------------------------------------------------------------------

--exec DBMS_MVIEW.REFRESH('MV_block_stat0_aggr_5_weeksBIS','C');


-----------------------------------------------------------------------
--- Unify Stat on DS
-----------------------------------------------------------------------

--- This MV allows analysis aggregation along time 
--- per DS and dataTier (RECO, AOD, etc), siteName, users 
--- Popularity is in number of accesses and totCPU
--- Selection is performed only on fileexitflag=1

--drop MATERIALIZED VIEW MV_DS_stat0;
commit;
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
commit;

--- aggregation: day, sitename, dataset
--- count distinct users per day, aggregating later more days will 
--- double count the same users that submitted in several days

CREATE MATERIALIZED VIEW MV_DS_stat0_aggr1
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay , siteName, collName, 
sum(numAccesses) as numAccesses, sum(totCPU) as totCPU, count(distinct userid) as numUsers
from  MV_DS_stat0
GROUP BY TDay, siteName, collName
;


--- aggregation: day, sitename, dataTier
--- count distinct users per day, aggregating later more days will 
--- double count the same users that submitted in several days


CREATE MATERIALIZED VIEW MV_DS_stat0_aggr2
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay , siteName, substr(collName,INSTR(collName, '/',-1)+1) as collName, 
sum(numAccesses) as numAccesses, sum(totCPU) as totCPU, count (distinct userid) as numUsers
from  MV_DS_stat0
GROUP BY TDay, siteName, substr(collName,INSTR(collName, '/',-1)+1)
;

--- MV_SITE table provides the list of Sites in the popDB
--- Used for validation of inputs
---

CREATE MATERIALIZED VIEW MV_SITE
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select distinct(sitename) as sitename from MV_DS_stat0_aggr2 where REGEXP_LIKE(sitename , 'T[0-3]_.*') order by sitename;


--- aggregation: day, dataset
--- count distinct users per day, aggregating later more days will 
--- double count the same users that submitted in several days


CREATE MATERIALIZED VIEW MV_DS_stat0_aggr1_summ
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay , collName, 
sum(numAccesses) as numAccesses, sum(totCPU) as totCPU, count(distinct userid) as numUsers
from  MV_DS_stat0
GROUP BY TDay, collName
;


--- MV_DS table provides the list of DSs in the popDB
--- Used for validation of inputs
---

CREATE MATERIALIZED VIEW MV_DS
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select distinct(collName) as collName from MV_DS_stat0_aggr1_summ order by collName;


--- aggregation: day, datatier
--- count distinct users per day, aggregating later more days will 
--- double count the same users that submitted in several days

CREATE MATERIALIZED VIEW MV_DS_stat0_aggr2_summ
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay ,  substr(collName,INSTR(collName, '/',-1)+1) as collName, 
sum(numAccesses) as numAccesses, sum(totCPU) as totCPU, count (distinct userid) as numUsers
from  MV_DS_stat0
GROUP BY TDay, substr(collName,INSTR(collName, '/',-1)+1)
;

--- MV_DataTier table provides the list of DataTiers in the popDB
--- Used for validation of inputs
---

CREATE MATERIALIZED VIEW MV_DataTier
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select distinct(collName) as collName from MV_DS_stat0_aggr2_summ order by collName;

--- aggregation: day, user, dataTier
--- distinct users per day, aggregating later more days 

CREATE MATERIALIZED VIEW MV_DS_stat0_aggr3
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay , userid, substr(collName,INSTR(collName, '/',-1)+1) as collName, 
sum(numAccesses) as numAccesses, sum(totCPU) as totCPU, count (distinct sitename) as numSites
from  MV_DS_stat0
GROUP BY TDay, userid, substr(collName,INSTR(collName, '/',-1)+1)
;


--- First aggregation: day, sitename, dataset namespace (ReReco, Summer2011, etc)
--- count distinct users per day, aggregating later more days will 
--- double count the same users that submitted in several days

CREATE MATERIALIZED VIEW MV_DS_stat0_aggr4
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
GROUP BY TDay, siteName, substr(collname,INSTR(collname, '/',-1,2)+1,INSTR(collname, '/',-1,1)-INSTR(collname, '/',-1,2)-1)
;


--- Second aggregation: day, dataset namespace (ReReco, Summer2011, etc)
--- count distinct users per day, aggregating later more days will 
--- double count the same users that submitted in several days

CREATE MATERIALIZED VIEW MV_DS_stat0_aggr4_summ
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
GROUP BY TDay, substr(collname,INSTR(collname, '/',-1,2)+1,INSTR(collname, '/',-1,1)-INSTR(collname, '/',-1,2)-1)
;

--- MV_DSName table provides the list of DSNames in the popDB
--- Used for validation of inputs
---

CREATE MATERIALIZED VIEW MV_DSName
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select distinct(collName) as collName from MV_DS_stat0_aggr4_summ order by collName;


CREATE MATERIALIZED VIEW MV_DS_stat0_remote
COMPRESS
PCTFREE 0
BUILD deferred
ENABLE QUERY REWRITE
AS
select Tday, sitename, 
sum(isremote * numAccesses) as Nremote, sum(numAccesses) as Ntot
from MV_DS_stat0
GROUP BY Tday, sitename
;

exec DBMS_MVIEW.REFRESH('MV_DS_stat0_remote','C');



-----------------------------------------------------------------------
--- The map dataset/files
-----------------------------------------------------------------------

--- This MV allows to count how many files are associated to a
--- DS (or block). It's a sort of internal catalogue, developed to
--- attempt a normalization of the popularity
--- NB: the unique association among block and file is not guarantee
--- in the popularity DB because of a feature of the crab job splitting.
--- This need to be considered when counting of files per DS or block are made

CREATE MATERIALIZED VIEW MV_DS_Files
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
REFRESH FAST
ENABLE QUERY REWRITE
AS
select inputcollection  as collName , filename
from raw_file
GROUP BY inputcollection, filename;

CREATE MATERIALIZED VIEW MV_DS_CountFiles
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select collName , count(filename)  as Nfiles
from MV_DS_Files
GROUP BY collName;


CREATE MATERIALIZED VIEW MV_user_userid
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
REFRESH FAST
ENABLE QUERY REWRITE
AS
select userid, username 
from raw_file 
GROUP BY userid, username;


-------------------------------------------------------------------
--- Investigation at Vanderbilt
-----------------------------------------------------------------------

DROP MATERIALIZED VIEW MV_invest_corrupted;

CREATE MATERIALIZED VIEW MV_invest_corrupted
COMPRESS
PCTFREE 0
--BUILD IMMEDIATE
REFRESH FAST
AS
select filename, finishedtimestamp, fileexitflag, jobexecexitcode, isRemote, jobid from raw_file 
where  finishedtimestamp>'2012-11-16' 
and fileexitflag != 2
and sitename='T2_US_Vanderbilt' and ( 
( (jobexecexitcode=8020 or jobexecexitcode=8021) and fileexitflag=0) or isRemote=1 );

grant select on MV_block_stat0_aggr_90_days to CMS_POPULARITY_SYSTEM_R;

