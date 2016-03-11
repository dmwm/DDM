-- define procedures
-- MVREFRESH: refresh materialized views
-- arguments: mvlist: list of MVs to refresh; mvarg: refresh mode ('F' for fast, etc.)
CREATE OR REPLACE PROCEDURE MVREFRESH (mvlist IN VARCHAR2, mvarg IN VARCHAR2:= NULL ) IS
BEGIN
  DBMS_MVIEW.REFRESH(mvlist, mvarg);
END MVREFRESH;

create or replace
PROCEDURE REFRESHAllMVs IS
BEGIN
MVREFRESH('MV_invest_corrupted');
END REFRESHAllMVs;

BEGIN
 -- Job defined entirely by the CREATE JOB procedure.
 DBMS_SCHEDULER.create_job (
   job_name        => 'refreshMV_job',
   job_type        => 'PLSQL_BLOCK',
   job_action      => 'BEGIN REFRESHALLMVs; END;',
   start_date      => to_date('2012-12-03 10:30:00','yyyy-mm-dd hh24:mi:ss'),
   repeat_interval => 'FREQ=Daily',
   end_date        => NULL,
   enabled         => TRUE,
   comments        => 'Refresh the MVs of the account as defined in REFRESHAllMVs procedure'
   );
END;