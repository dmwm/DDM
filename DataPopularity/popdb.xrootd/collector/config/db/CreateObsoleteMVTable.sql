------------------------------------------------------
--- THESE MVS ARE OBSOLETE SINCE 2012 AND NO LONGER
--- DEPLOYED IN THE SCHEMA
--- KEEPING HERE ONLY FOR REFERENCE
------------------------------------------------------

------------------------------------------------------
--- CMS
------------------------------------------------------

------------------------------------------------------
---xrd Monitoring MV
------------------------------------------------------

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
--- Monitor the PPS tests
--- 

--drop materialized view MV_xrdmon_pps_srmmon_test_x_H;
commit;
CREATE MATERIALIZED VIEW MV_xrdmon_pps_srmmon_test_x_H
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
REFRESH FAST
ENABLE QUERY REWRITE
AS
select trunc(starttimestamp,'HH24') as xTime, count(file_lfn) as yValue  from T_xrd_raw_file 
where client_host like 'srmmon%' and file_lfn like '/eos/ppsscratch/test/slstest-eospps/%'
GROUP BY trunc(starttimestamp,'HH24');

exec DBMS_MVIEW.REFRESH('MV_xrdmon_pps_srmmon_test_x_H');

commit;

--drop materialized view MV_xrdmon_pps_dteam_test_x_H;
commit;
CREATE MATERIALIZED VIEW MV_xrdmon_pps_dteam_test_x_H
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
REFRESH FAST
ENABLE QUERY REWRITE
AS
select trunc(starttimestamp,'HH24') as xTime, count(file_lfn) as yValue  from T_xrd_raw_file 
where server_username = 'dteam001' and file_lfn like '/eos/ppsscratch/test/slstest-eospps/%' 
GROUP BY trunc(starttimestamp,'HH24');

exec DBMS_MVIEW.REFRESH('MV_xrdmon_pps_dteam_test_x_H');

commit;

---
--- stats end - start time 
---

--drop materialized view MV_xrdmon_procTime_x_H;
commit;
CREATE MATERIALIZED VIEW MV_xrdmon_procTime_x_H
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
REFRESH FAST ON DEMAND
with rowid
ENABLE QUERY REWRITE
AS
select trunc(starttimestamp,'HH24') as xTime, file_lfn, read_bytes_at_close, 
(end_time - start_time) as procTime, read_bytes_at_close/(end_time - start_time) as readRate,
server_username,
trunc(LOG(10,end_time - start_time),0) as decade
from T_xrd_raw_file where
(end_time - start_time)>0;

exec DBMS_MVIEW.REFRESH('MV_xrdmon_procTime_x_H');

commit;

--drop materialized view MV_xrdmon_procTime_x_H_v2;
commit;
CREATE MATERIALIZED VIEW MV_xrdmon_procTime_x_H_v2
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
REFRESH FAST ON DEMAND
with rowid
ENABLE QUERY REWRITE
AS
select trunc(starttimestamp,'HH24') as xTime, sum(read_bytes_at_close) as totBytes, 
sum(end_time - start_time) as TotProcTime,
count(*) as entries
--avg(read_bytes_at_close/(end_time - start_time)) as avgreadByteRate
from T_xrd_raw_file where
(end_time - start_time)>0 
and
file_lfn like '/replicate%'
group by trunc(starttimestamp,'HH24');

exec DBMS_MVIEW.REFRESH('MV_xrdmon_procTime_x_H_v2');

commit;


--drop materialized view MV_xrdmon_procTime_x_H_aggr1;
commit;
CREATE MATERIALIZED VIEW MV_xrdmon_procTime_x_H_aggr1
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select xtime, decade,
count(*) as entries, 
round(sum(read_bytes_at_close)/1024/1024 ,1) as totMB,
round(avg(readRate)/1024,1) as meankBsec, sum(procTime) as totProcTimeInSec,
round(sum(read_bytes_at_close)/1024/1024 / count(*),1) as meanOpenSizeMB
from MV_xrdmon_procTime_x_H
where file_lfn  not like '/replicate%'
group by xtime, decade
;

commit;

--- and now just for the replicate
--drop materialized view MV_xrdmon_procTime_x_H_aggr2;
CREATE MATERIALIZED VIEW MV_xrdmon_procTime_x_H_aggr2
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select xtime, decade,
count(*) as entries, 
round(sum(read_bytes_at_close)/1024/1024 ,1) as totMB,
round(avg(readRate)/1024,1) as meankBsec, sum(procTime) as totProcTimeInSec,
round(sum(read_bytes_at_close)/1024/1024 / count(*),1) as meanOpenSizeMB
from MV_xrdmon_procTime_x_H
where file_lfn  like '/replicate%'
group by xtime, decade
;

commit;


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

----------------------------
---- TEST MVs
----------------------------

--drop materialized view MV_XRD_stat0_tmp;
CREATE MATERIALIZED VIEW MV_XRD_stat0_tmp
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
tb.dsname,
count(ta.client_host) as numAccesses,
sum(ta.end_time - ta.start_time) as procTime,
sum(ta.read_bytes_at_close) as readBytes
from T_XRD_RAW_FILE ta, T_XRD_LFC tb 
where 
ta.file_lfn = tb.fullname
and ta.end_time - ta.start_time > 0
GROUP BY trunc(ta.endtimestamp), ta.client_host, NVL(ta.server_username,'unknown'), tb.dsname
;

--drop MATERIALIZED VIEW MV_XRD_DS_stat0_tmp_aggr1;
CREATE MATERIALIZED VIEW MV_XRD_DS_stat0_tmp_aggr1
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select  TDay , dsname as collName, 
REGEXP_INSTR(server_username,'^cms') as isUSERCMS,
sum(readBytes) as readBytes,
sum(numAccesses) as numAccesses, sum(procTime) as totCPU, count(distinct server_username) as numUsers
from  MV_XRD_stat0_tmp
group by TDay, dsname, REGEXP_INSTR(server_username,'^cms') 
;


commit;

--drop MATERIALIZED VIEW MV_XRD_DS_stat0_aggr1_tst;
CREATE MATERIALIZED VIEW MV_XRD_DS_stat0_aggr1_tst
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

exec MVREFRESHLOG('MV_XRD_DS_stat0_aggr1_tst','C')

