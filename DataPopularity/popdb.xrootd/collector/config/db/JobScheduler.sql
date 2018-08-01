BEGIN
 -- Job defined entirely by the CREATE JOB procedure.
 DBMS_SCHEDULER.create_job (
   job_name        => 'refreshMV_eoscms_job',
   job_type        => 'PLSQL_BLOCK',
   job_action      => 'BEGIN REFRESHALLMVs; END;',
   start_date      => to_date('2012-02-29 11:00:00','yyyy-mm-dd hh24:mi:ss'),
   repeat_interval => 'FREQ=HOURLY; interval=8',
   end_date        => NULL,
   enabled         => TRUE,
   comments        => 'Refresh the MVs of the EOSCMS account as defined in REFRESHAllMVs procedure'
   );
END;

BEGIN
DBMS_SCHEDULER.STOP_JOB ('refreshMV_eoscms_job');
END;

BEGIN
DBMS_SCHEDULER.set_attribute(
name        => 'refreshMV_eoscms_job',
attribute => 'start_date',
value => to_date('2016-03-10 17:00:00','yyyy-mm-dd hh24:mi:ss')
);
END;

BEGIN
  DBMS_SCHEDULER.DROP_JOB ('refreshMV_eoscms_job', force=>true);
END;

----------------------------------------------------------
----------------------------------------------------------

BEGIN
 -- Job defined entirely by the CREATE JOB procedure.
 DBMS_SCHEDULER.create_job (
   job_name        => 'refreshMV_eoscms_job_stat0',
   job_type        => 'PLSQL_BLOCK',
   job_action      => 'BEGIN REFRESHSTAT0MVs; END;',
   start_date      => to_date('2014-03-08 12:30:00','yyyy-mm-dd hh24:mi:ss'),
   repeat_interval => 'FREQ=DAILY; INTERVAL=1;',
   end_date        => NULL,
   enabled         => TRUE,
   comments        => 'Refresh the MVs of the EOSCMS account as defined in REFRESHSTAT0MVs procedure'
   );
END;


BEGIN
DBMS_SCHEDULER.DROP_JOB ('refreshMV_eoscms_job_stat0', force=>true);
END;

BEGIN
DBMS_SCHEDULER.STOP_JOB ('refreshMV_eoscms_job_stat0');
END;

BEGIN
DBMS_SCHEDULER.set_attribute(
name        => 'refreshMV_eoscms_job_stat0',
attribute => 'start_date',
value => to_date('2016-03-10 17:20:00','yyyy-mm-dd hh24:mi:ss')
);
END;


----------------------------------------------------------
----------------------------------------------------------

BEGIN
 -- Job defined entirely by the CREATE JOB procedure.
 DBMS_SCHEDULER.create_job (
   job_name        => 'refreshMV_eoscms_job_stat1',
   job_type        => 'PLSQL_BLOCK',
   job_action      => 'BEGIN REFRESHSTAT1MVs; END;',
   start_date      => to_date('2014-03-08 9:30:00','yyyy-mm-dd hh24:mi:ss'),
   repeat_interval => 'FREQ=DAILY; INTERVAL=1;',
   end_date        => NULL,
   enabled         => TRUE,
   comments        => 'Refresh the MVs of the EOSCMS account as defined in REFRESHSTAT0MVs procedure'
   );
END;


BEGIN
DBMS_SCHEDULER.DROP_JOB ('refreshMV_eoscms_job_stat1', force=>true);
END;

BEGIN
DBMS_SCHEDULER.STOP_JOB ('refreshMV_eoscms_job_stat1');
END;

BEGIN
DBMS_SCHEDULER.set_attribute(
name        => 'refreshMV_eoscms_job_stat1',
attribute => 'start_date',
value => to_date('2016-03-10 17:30:00','yyyy-mm-dd hh24:mi:ss')
);
END;

BEGIN
DBMS_SCHEDULER.set_attribute(
name        => 'refreshMV_eoscms_job_stat1',
attribute => 'repeat_interval',
value => 'FREQ=DAILY; INTERVAL=1;'
);
END;

----------------------------------------------------------
----------------------------------------------------------

BEGIN
 -- Job defined entirely by the CREATE JOB procedure.
 DBMS_SCHEDULER.create_job (
   job_name        => 'refreshMV_eoscms_job_stat2',
   job_type        => 'PLSQL_BLOCK',
   job_action      => 'BEGIN REFRESHSTAT2MVs; END;',
   start_date      => to_date('2014-03-08 12:00:00','yyyy-mm-dd hh24:mi:ss'),
   repeat_interval => 'FREQ=HOURLY; INTERVAL=8;',
   end_date        => NULL,
   enabled         => TRUE,
   comments        => 'Refresh the MVs of the EOSCMS account as defined in REFRESHSTAT0MVs procedure'
   );
END;


BEGIN
DBMS_SCHEDULER.DROP_JOB ('refreshMV_eoscms_job_stat2');
END;

BEGIN
DBMS_SCHEDULER.STOP_JOB ('refreshMV_eoscms_job_stat2');
END;

BEGIN
DBMS_SCHEDULER.set_attribute(
name        => 'refreshMV_eoscms_job_stat2',
attribute => 'start_date',
value => to_date('2016-03-10 18:00:00','yyyy-mm-dd hh24:mi:ss')
);
END;

