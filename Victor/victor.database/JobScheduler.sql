BEGIN
 -- Job defined entirely by the CREATE JOB procedure.
 DBMS_SCHEDULER.create_job (
   job_name        => 'refreshMV_victor_job',
   job_type        => 'PLSQL_BLOCK',
   job_action      => 'BEGIN MVREFRESH; END;',
   start_date      => to_date('2012-08-28 11:25:00','yyyy-mm-dd hh24:mi:ss'),
   repeat_interval => 'FREQ=Daily',
   end_date        => NULL,
   enabled         => TRUE,
   comments        => 'Refresh the MVsin MVRefresh procedure'
   );
END;


--BEGIN
--  DBMS_SCHEDULER.DROP_JOB ('refreshMV_victor_job');
--END;

