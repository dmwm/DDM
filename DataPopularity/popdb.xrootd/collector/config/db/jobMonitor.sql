-----------------------------------------
----- STATISTICS
-----------------------------------------

alter session set NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS';

-- Details of Scheduled jobs
select *
from user_scheduler_jobs;

select job_name, job_action, start_date, repeat_interval, enabled, restartable, state, last_start_date, NEXT_RUN_DATE, comments
from user_scheduler_jobs;

select job_name from user_scheduler_jobs;

--Statistics about Jobs already done
SELECT to_char(log_date, 'YY-MM-DD HH24:MI:SS') , job_name, status,
  to_char(req_start_date, 'YY-MM-DD HH24:MI:SS'), to_char(actual_start_date, 'YY-MM-DD HH24:MI:SS'), run_duration, cpu_used,
  additional_info ADDITIONAL_INFO 
  FROM user_scheduler_job_run_details 
  --where job_name not like '%xrdmon%'
  ORDER BY req_start_date desc;
    
select * from user_scheduler_job_log;

-- Log of scheduled jobs
 select log_date
 ,      job_name
 ,      status
 from user_scheduler_job_log ;


--Statistics about RUNNING Jobs
select job_name
,      session_id
,      running_instance
,      elapsed_time
,      cpu_used
from user_scheduler_running_jobs;
  
-- Full detail about RUNNING Jobs
select * from user_scheduler_running_jobs;
 

-- Detail of MV refresh per job running
select * from (
select unique_id, mvname, starttime, endtime, 24*60*round( endtime - starttime , 3) as duration_in_mins from T_MVREFRESH_LOG 
--where endtime >= starttime
where mvname not like 'MV_xrdmon%'
order by starttime desc)
where rownum <60;
