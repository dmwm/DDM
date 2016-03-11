-----------------------------------------
----- STATISTICS
-----------------------------------------

alter session set NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS';

select * from user_ts_quotas;

-- Size of the tables

--select count(size_in_GB) from (
select sum(bytes)/1024/1000/1000 as size_in_GB, segment_name from user_segments 
--where segment_name like 'MV_%' 
group by segment_name order by size_in_gb desc
--)
;

select sum(bytes)/1024/1000/1000 as size_in_GB from user_segments 
where segment_name like 'MV_%' 
 order by size_in_gb desc
--)
;


select table_name, num_rows from user_tables order by num_rows desc;

select * from user_tables order by num_rows desc;


select trunc(endtimestamp), count(*) from T_XRD_RAW_FILE
group by trunc(endtimestamp)
order by trunc(endtimestamp);

select INSTR(file_lfn,'/replicate') from T_XRD_RAW_FILE where file_lfn not like '/replicate%';


select * from USER_MVIEW_ANALYSIS where MVIEW_NAME='MV_DS_STAT0';

select min(endtimestamp) from T_XRD_RAW_FILE;

select count(*) from T_XRD_RAW_FILE;


select count(*) from T_XRD_LFC;
select count(*) from T_XRD_USERFILE;
select * from MV_XRD_STAT2;

select trunc(Tday,'month') as tday, count(distinct client_domain) from MV_XRDMON_SRV_CLT 
group by trunc(Tday,'month') order by tday asc;

select trunc(Tday,'month') as tday, count(distinct server_domain) from MV_XRDMON_SRV_CLT 
group by trunc(Tday,'month') order by tday asc;


select  trunc(endtimestamp,'month') as tday, count(distinct user_dn) from T_XRD_RAW_FILE
group by trunc(endtimestamp,'month') order by tday asc;

select count(distinct user_dn) from T_XRD_RAW_FILE;

select trunc(xtime,'j'), sum(yvalue) from MV_xrdmon_starttime_norepl_x_H group by trunc(xtime,'j') order by trunc(xtime,'j') desc;
select trunc(xtime,'month'), sum(yvalue) from MV_xrdmon_starttime_norepl_x_H group by trunc(xtime,'month') order by trunc(xtime,'month') desc;
