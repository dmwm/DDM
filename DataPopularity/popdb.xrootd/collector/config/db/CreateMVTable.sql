------------------------------------------------------
--- CMS
------------------------------------------------------

------------------------------------------------------
---xrd Monitoring MV
------------------------------------------------------

--drop materialized view MV_xrdmon_rates_x_H;
--commit;
CREATE MATERIALIZED VIEW MV_xrdmon_rates_x_H
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select trunc(starttimestamp,'HH24') as sTime, trunc(endtimestamp,'HH24') as eTime,
trunc(inserttimestamp,'HH24') as iTime, 
INSTR(file_lfn,'/replicate%') as replica,
count(file_lfn) as yValue  
from T_xrd_raw_file
group by trunc(starttimestamp,'HH24'), trunc(endtimestamp,'HH24'), trunc(inserttimestamp,'HH24'), INSTR(file_lfn,'/replicate%');

exec DBMS_MVIEW.REFRESH('MV_xrdmon_rates_x_H');

commit;

select * from MV_xrdmon_rates_x_H;
---
--- Select the number of inserted rows per min
--- 

--drop materialized view MV_xrdmon_inserts_x_MI;

---CREATE MATERIALIZED VIEW MV_XRDmon_inserts_x_MI
---COMPRESS
---PCTFREE 0
---BUILD IMMEDIATE
---REFRESH FAST
---ENABLE QUERY REWRITE
---AS
---select trunc(inserttimestamp,'MI') as xTime, count(file_lfn) as yValue  from T_xrd_files 
---GROUP BY trunc(inserttimestamp,'MI');

--exec DBMS_MVIEW.REFRESH('MV_xrdmon_inserts_x_MI');

---
--- Select the number of inserted rows per H
--- 

--drop materialized view MV_xrdmon_inserts_x_H;
commit;
CREATE MATERIALIZED VIEW MV_xrdmon_inserts_x_H
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select iTime as xTime, sum(yValue) as yValue  from MV_xrdmon_rates_x_H
group by iTime;

exec DBMS_MVIEW.REFRESH('MV_xrdmon_inserts_x_H');

commit;
 

---
--- Select the number of files opened per H
--- 
--drop materialized view MV_xrdmon_starttime_x_H;
commit;
CREATE MATERIALIZED VIEW MV_xrdmon_starttime_x_H
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select sTime as xTime, sum(yValue) as yValue   from MV_xrdmon_rates_x_H
GROUP BY sTime;

exec DBMS_MVIEW.REFRESH('MV_xrdmon_starttime_x_H');

commit;



---
--- Select the number of files opened per H excluding the /replicate
--- 
--drop materialized view MV_xrdmon_starttime_norepl_x_H;
commit;
CREATE MATERIALIZED VIEW MV_xrdmon_starttime_norepl_x_H
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select sTime as xTime, sum(yValue) as yValue  from MV_xrdmon_rates_x_H
where replica = 0
group by sTime;

exec DBMS_MVIEW.REFRESH('MV_xrdmon_starttime_norepl_x_H');

commit;


---
--- Select the number of files opened per H only for the /replicate
--- 
--drop materialized view MV_xrdmon_starttime_repl_x_H;
commit;
CREATE MATERIALIZED VIEW MV_xrdmon_starttime_repl_x_H
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select sTime as xTime, sum(yValue) as yValue  from MV_xrdmon_rates_x_H
where replica != 0
GROUP BY sTime;

exec DBMS_MVIEW.REFRESH('MV_xrdmon_starttime_repl_x_H');

commit;

---
--- Select the number of files closed per H
--- 
--drop materialized view MV_xrdmon_endtime_x_H;
commit;
CREATE MATERIALIZED VIEW MV_xrdmon_endtime_x_H
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select eTime as xTime, sum(yValue) as yValue   from MV_xrdmon_rates_x_H
GROUP BY eTime;

exec DBMS_MVIEW.REFRESH('MV_xrdmon_endtime_x_H');

commit;

---
--- stats end - start time 
---

------------------------------------------------------
--- CMS specific 
------------------------------------------------------

-- Comment about MV_XRD_stat0
-- This MV has been built to aggregate information at the level of dataset, 
-- for monitoring purpose of popularity queries.
-- In order to extend the popcombine application, I had to introduce also an aggregation at blockname level.
-- To avoid generation of two MVs, I tried to include both blockname and dsname into the same MV_XRD_stat0,
-- but the index length is too long:
-- SQL Error: ORA-01450: maximum key length (6398) exceeded
-- As a workaround I create an initial MV based on blockname, then I aggregate on dsname, keeping the MV names

--drop materialized view MV_XRD_stat0_pre;
CREATE MATERIALIZED VIEW MV_XRD_stat0_pre
COMPRESS
PCTFREE 0
--BUILD IMMEDIATE
BUILD DEFERRED
REFRESH FAST
ENABLE QUERY REWRITE
AS
select trunc(ta.endtimestamp) as TDay ,
ta.client_host,
NVL(ta.server_username,'unknown') as server_username,
tb.blockname,
count(ta.client_host) as numAccesses,
sum(ta.end_time - ta.start_time) as procTime,
sum(ta.read_bytes_at_close) as readBytes
from T_XRD_RAW_FILE ta, T_XRD_LFC tb 
where 
ta.file_lfn = tb.fullname
and ta.end_time - ta.start_time > 0
GROUP BY trunc(ta.endtimestamp), ta.client_host, NVL(ta.server_username,'unknown'), tb.blockname
;

--exec DBMS_MVIEW.REFRESH('MV_XRD_stat0_pre');

select * from MV_XRD_stat0_pre;


-- aggregating at level of blocks, datasets
CREATE or replace
VIEW V_XRD_LFC_aggr1
AS
select distinct blockname as blockname,  dsname as dsname from T_XRD_LFC;
commit;



--drop materialized view MV_XRD_stat0;
CREATE MATERIALIZED VIEW MV_XRD_stat0
COMPRESS
PCTFREE 0
--BUILD IMMEDIATE
BUILD DEFERRED
ENABLE QUERY REWRITE
AS
select TDay ,
client_host,
server_username,
tb.dsname,
sum(numAccesses) as numAccesses,
sum(procTime) as procTime,
sum(readBytes) as readBytes
from MV_XRD_stat0_pre ta, V_XRD_LFC_aggr1 tb 
where 
ta.blockname = tb.blockname
GROUP BY TDay, client_host, server_username, tb.dsname
;

--exec DBMS_MVIEW.REFRESH('MV_XRD_stat0');
-- exec MVREFRESHLOG('MV_XRD_stat0','C'); exec MVREFRESHLOG('MV_XRD_DS_stat0_aggr1_tst','C'); commit; 

--- aggregation: day, dataset
--- count distinct users per day, aggregating later more days will 
--- double count the same users that submitted in several days

--drop materialized view MV_XRD_DS_stat0_aggr1;
commit;

CREATE MATERIALIZED VIEW MV_XRD_DS_stat0_aggr1
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay , dsname as collName, 
REGEXP_INSTR(server_username,'^cms') as isUSERCMS,
sum(readBytes) as readBytes,
sum(numAccesses) as numAccesses, sum(procTime) as totCPU, count(distinct server_username) as numUsers
from  MV_XRD_stat0
group by TDay, dsname, REGEXP_INSTR(server_username,'^cms') 
;

commit;

--- MV_DS table provides the list of DSs in the popDB
--- Used for validation of inputs
---
CREATE MATERIALIZED VIEW MV_DS
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select distinct(collName) as collName from MV_XRD_DS_stat0_aggr1 order by collName;

commit;

--- aggregation: day, dataTier
--- count distinct users per day, aggregating later more days will 
--- double count the same users that submitted in several days

--drop materialized view MV_XRD_DS_stat0_aggr2;
commit;

CREATE MATERIALIZED VIEW MV_XRD_DS_stat0_aggr2
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay , substr(dsname,INSTR(dsname, '/',-1)+1) as collName, 
REGEXP_INSTR(server_username,'^cms') as isUSERCMS,
sum(readBytes) as readBytes,
sum(numAccesses) as numAccesses, sum(procTime) as totCPU, count (distinct server_username) as numUsers
from  MV_XRD_stat0
group by TDay, substr(dsname,INSTR(dsname, '/',-1)+1),REGEXP_INSTR(server_username,'^cms')
;

commit;

--- MV_DataTier table provides the list of DataTiers in the popDB
--- Used for validation of inputs
---

CREATE MATERIALIZED VIEW MV_DataTier
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select distinct(collName) as collName from MV_XRD_DS_stat0_aggr2 order by collName;



--- aggregation: day, user, dataTier
--- distinct users per day, aggregating later more days 

--drop materialized view MV_XRD_DS_stat0_aggr3;
commit;

CREATE MATERIALIZED VIEW MV_XRD_DS_stat0_aggr3
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay , server_username, substr(dsname,INSTR(dsname, '/',-1)+1) as collName, 
sum(readBytes) as readBytes,
sum(numAccesses) as numAccesses, sum(procTime) as totCPU
from  MV_XRD_stat0
group by TDay, server_username, substr(dsname,INSTR(dsname, '/',-1)+1)
;

commit; 

--- First aggregation: day, sitename, dataset namespace (ReReco, Summer2011, etc)
--- count distinct users per day, aggregating later more days will 
--- double count the same users that submitted in several days

--drop materialized view MV_XRD_DS_stat0_aggr4;
commit;

CREATE MATERIALIZED VIEW MV_XRD_DS_stat0_aggr4
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay ,  
substr(dsname,INSTR(dsname, '/',-1,2)+1,INSTR(dsname, '/',-1,1)-INSTR(dsname, '/',-1,2)-1) as collName,
REGEXP_INSTR(server_username,'^cms') as isUSERCMS,
sum(readBytes) as readBytes,
sum(numAccesses) as numAccesses, sum(procTime) as totCPU, count (distinct server_username) as numUsers
from  MV_XRD_stat0
where 
substr(dsname,INSTR(dsname, '/',-1,1)+1) not like 'USER'
and 
dsname not like 'unknown'
group by TDay, substr(dsname,INSTR(dsname, '/',-1,2)+1,INSTR(dsname, '/',-1,1)-INSTR(dsname, '/',-1,2)-1),REGEXP_INSTR(server_username,'^cms')
;



--- MV_DSName table provides the list of DSNames in the popDB
--- Used for validation of inputs
---

CREATE MATERIALIZED VIEW MV_DSName
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select distinct(collName) as collName from MV_XRD_DS_stat0_aggr4 order by collName;

commit;

---
--- create MV for block statistics
---

--drop MATERIALIZED VIEW MV_block_stat0_aggr_180_days;

CREATE MATERIALIZED VIEW MV_block_stat0_aggr_180_days
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select trunc(tday,'W') as Tday, 
'T2_CH_CERN' as sitename, 
blockname as collName, 
sum(numAccesses) as numAccesses, 
round(sum(procTime),0) as totCPU,
sum(readBytes) as readBytes
from MV_XRD_stat0_pre 
where trunc(Tday,'W') >  trunc(add_months(sysdate, -1) ,'W') 
GROUP BY trunc(tday,'W'), 'T2_CH_CERN', blockname;

select max(tday) from MV_block_stat0_aggr_180_days order by tday;


CREATE MATERIALIZED VIEW MV_block_stat0_aggr_12_months
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select trunc(tday,'W') as Tday, 
'T2_CH_CERN' as sitename, 
blockname as collName, 
sum(numAccesses) as numAccesses, 
round(sum(procTime),0) as totCPU,
sum(readBytes) as readBytes
from MV_XRD_stat0_pre 
where trunc(Tday,'W') > trunc(systimestamp - interval '12' month,'W') 
GROUP BY trunc(tday,'W'), 'T2_CH_CERN', blockname;

select max(tday) from MV_block_stat0_aggr_12_months order by tday;

--drop MATERIALIZED VIEW MV_block_stat0_last_access;
CREATE MATERIALIZED VIEW MV_block_stat0_last_access
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select max(trunc(Tday,'W')) as TDAY, 'T2_CH_CERN' as sitename, blockname as collName
from MV_XRD_stat0_pre 
GROUP BY 'T2_CH_CERN', blockname;

select max(tday) from MV_block_stat0_last_access;

------------------------------------------------------
--- User Files
------------------------------------------------------

--- In order to provide popularity metrics of user files, stored on EOS and 
--- accessed by the same or other users, another MV is provided, where the 
--- join among T_XRD_RAW_FILE and T_XRD_USERFILE is produced.
--- In this approach, there is parallel among what in MV_XRD_stat0 is the dsname and what
--- here is the ownerUserName

--drop materialized view MV_XRD_stat1;

CREATE MATERIALIZED VIEW MV_XRD_stat1
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
REFRESH FAST
ENABLE QUERY REWRITE
AS
select trunc(ta.endtimestamp) as TDay ,
ta.client_host,
NVL(ta.server_username,'unknown') as server_username,
tb.username as ownerUsername,
count(ta.client_host) as numAccesses,
sum(ta.end_time - ta.start_time) as procTime,
sum(ta.read_bytes_at_close) as readBytes
from T_XRD_RAW_FILE ta, T_XRD_USERFILE tb 
where 
ta.file_lfn = tb.lfn
and ta.end_time - ta.start_time > 0
group by trunc(ta.endtimestamp), ta.client_host, NVL(ta.server_username,'unknown'), tb.username
;

exec DBMS_MVIEW.REFRESH('MV_XRD_stat1');


commit;


select * from MV_XRD_stat1;

--- aggregation: day, ownerusername
--- count distinct users per day, aggregating later more days will 
--- double count the same users that submitted in several days

--drop materialized view MV_XRD_DS_stat1_aggr1;
commit;

CREATE MATERIALIZED VIEW MV_XRD_DS_stat1_aggr1
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay , ownerUsername as collName, 
REGEXP_INSTR(server_username,'^cms') as isUSERCMS,
sum(readBytes) as readBytes,
sum(numAccesses) as numAccesses, sum(procTime) as totCPU, count(distinct server_username) as numUsers
from  MV_XRD_stat1
group by TDay, ownerUsername, REGEXP_INSTR(server_username,'^cms') 
;

commit;



select * from MV_XRD_DS_stat1_aggr1;


---
--- The following MV is used to assess the EOS popularity for user areas, where no correspondance with LFC, dsname and blockname is found
---
--drop materialized view MV_XRD_stat2;
commit;
CREATE MATERIALIZED VIEW MV_XRD_stat2
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
REFRESH FAST
ENABLE QUERY REWRITE
AS
select trunc(endtimestamp) as TDay ,
sum(read_bytes_at_close) as readBytes,
sum(1) as Nentries,
substr(file_lfn,0,instr(file_lfn,'/',-1)) as dirName
from T_XRD_RAW_FILE 
where
file_lfn not like '/replicate%'
GROUP BY trunc(endtimestamp), substr(file_lfn,0,instr(file_lfn,'/',-1))
;


select min(tday), max(tday) from MV_XRD_stat2  order by tday desc;



CREATE or replace
VIEW V_XRD_stat2_aggr1
AS
select dirname as path, min(tday) as min_tday, max(tday) as max_tday, sum(readbytes)/1000/1000 as read_bytes, sum(nentries) as read_acc
from MV_XRD_stat2
--where 
--   dirname like '/eos/cms/store/user%' 
--or dirname like '/eos/cms/store/caf%'    
--or dirname like '/eos/cms/store/group%'
--or dirname like '/eos/cms/store/cmst3%'
GROUP BY 
--substr(dirname,0,instr(dirname,'/',-1)-1),  <---- I do not remember why this was needed. grouping is the same just with dirname
dirname
order by max(tday) desc;
commit;



