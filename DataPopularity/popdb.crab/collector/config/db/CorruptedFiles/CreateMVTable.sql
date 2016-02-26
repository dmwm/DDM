
--- Set of sql to create the MV that identifies corrupted files 
--- ALGO: identify the files that in the last 15 days had only failed accesses. Provide also the counter of the number of failed accesses, and failed days 
--- Only CMSSW errors 8020 and 8021 are accounted for the job failures.

create or replace view v_files_with_sumflag0
as
select sitename, filename from (
select sitename, sum(sumflag) as Tsumflag, filename
from T_corruptedfiles group by sitename, filename
) 
where tsumflag = 0;

create or replace view v_files_with_openProblem
as
select  sitename, count(distinct tday) as ndays, sum(nacc) as nacc, filename
from T_corruptedfiles
where (
  JobExitCode = 8020 
or JobExitCode = 8021 
-- or JobExitCode = 8028  -- removed the 8028 (remote file error) because this would be assigned to the local site and not to the remote site
)
group by sitename, filename;


drop MATERIALIZED VIEW MV_corruptedfiles;
CREATE 
MATERIALIZED VIEW MV_corruptedfiles
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select r.sitename, r.ndays, r.nacc, r.filename from v_files_with_openProblem r
inner join v_files_with_sumflag0 s
on r.sitename = s.sitename and r.filename = s.filename
;


