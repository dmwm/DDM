create or replace
PROCEDURE MVREFRESH (mvlist IN VARCHAR2) IS
BEGIN
  DBMS_MVIEW.REFRESH(mvlist);
END MVREFRESH;


drop procedure MVREFRESHLOG;

create or replace
PROCEDURE MVREFRESHLOG (theMVName IN VARCHAR2, theoption IN VARCHAR2 := NULL) IS
BEGIN

DECLARE 
theID  NUMBER(16,0);
theStartTime DATE;
BEGIN

select supplier_seq.nextval into theID from dual;
select sysdate into theStartTime from dual;
insert into  T_MVREFRESH_LOG (unique_id,mvName, starttime, endtime)  values(theID,theMVName,theStartTime, to_date('19700101','YYYYMMDD') );
DBMS_MVIEW.REFRESH(theMVName,theoption);
update T_MVREFRESH_LOG set endtime=sysdate where unique_id=theID;
END;

END MVREFRESHLOG;


create or replace
PROCEDURE REFRESHAllMVs IS
BEGIN
MVREFRESHLOG('MV_xrdmon_rates_x_H');
MVREFRESHLOG('MV_xrdmon_inserts_x_H');
MVREFRESHLOG('MV_xrdmon_starttime_x_H');
MVREFRESHLOG('MV_xrdmon_starttime_norepl_x_H');
MVREFRESHLOG('MV_xrdmon_starttime_repl_x_H');
MVREFRESHLOG('MV_xrdmon_endtime_x_H');
--MVREFRESHLOG('MV_xrdmon_pps_srmmon_test_x_H');
--MVREFRESHLOG('MV_xrdmon_pps_dteam_test_x_H');
--MVREFRESHLOG('MV_xrdmon_procTime_x_H');
END REFRESHAllMVs;


create or replace
PROCEDURE REFRESHSTAT0MVs IS
BEGIN

MVREFRESHLOG('MV_XRD_stat0_pre');
MVREFRESHLOG('MV_XRD_stat0','C');
MVREFRESHLOG('MV_XRD_DS_stat0_aggr1','C');
MVREFRESHLOG('MV_XRD_DS_stat0_aggr2','C');
MVREFRESHLOG('MV_XRD_DS_stat0_aggr3','C');
MVREFRESHLOG('MV_XRD_DS_stat0_aggr4','C');  
MVREFRESHLOG('MV_block_stat0_aggr_180_days','C');
MVREFRESHLOG('MV_block_stat0_aggr_12_months','C');
MVREFRESHLOG('MV_block_stat0_last_access','C');  

MVREFRESHLOG('MV_DS','C');
MVREFRESHLOG('MV_DSName','C');
MVREFRESHLOG('MV_DataTier','C');

END REFRESHSTAT0MVs;


create or replace
PROCEDURE REFRESHSTAT1MVs IS
BEGIN

MVREFRESHLOG('MV_XRD_stat1');
MVREFRESHLOG('MV_XRD_DS_stat1_aggr1','C');

END REFRESHSTAT1MVs;


create or replace
PROCEDURE REFRESHSTAT2MVs IS
BEGIN

MVREFRESHLOG('MV_XRD_stat2');

END REFRESHSTAT2MVs;
