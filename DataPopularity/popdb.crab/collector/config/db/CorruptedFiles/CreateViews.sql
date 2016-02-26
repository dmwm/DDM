
-------------------------------------------------------
-- Report statistics about each file in each site (Detail Stats)
-------------------------------------------------------

create or replace view v_corruptedFilesDetail
as
select sitename, nAcc, ndays, filename 
from  MV_CorruptedFiles                                                                                                                                                                                                                    
where ndays >2 or nacc > 4
order by nAcc desc, sitename, filename;   

select sitename, nAcc, ndays , nacc/ndays , filename from v_corruptedFilesDetail
where ndays>3;


-------------------------------------------------------
-- Report statistics about each dataset in each site

-- Summary of the corrupted files found per site, aggregated per dataset.
-- A file is defined corrupded if ALWAYS failed in job accesses in the last 15 days.
-- Only CMSSW errors 8020 and 8021 are accounted for the job failures.
-- The table provides for each site and dataset the number of failing files, with the max and min number of failures and distinct days of failures. 
-- Only files with at least 5 failures or 3 distinct days of failures are summarized in the table.
-------------------------------------------------------


create or replace view v_corruptedFilesDSSummary 
as
select sitename, count(*) as files, 
max(nacc) as maxacc, min(nacc) as minacc,
max(ndays) as maxdays, min(ndays) as mindays,
SUBSTR(filename,1,INSTR(filename,'/',1,6)) as path
from MV_CorruptedFiles 
where ndays >2 or nacc > 4
group by sitename, SUBSTR(filename,1,INSTR(filename,'/',1,6))
order by mindays desc, sitename;

select * from v_corruptedFilesDSSummary ;

-------------------------------------------------------
-- Report statistics about each site

-- Summary of the corrupted files found per site.
-- A file is defined corrupded if ALWAYS failed in job accesses in the last 15 days.
-- Only CMSSW errors 8020 and 8021 are accounted for the job failures.
-- The table provides for each site the number of failing files with the max and min number of failures and distinct days of failures. 
-- Only files with at least 5 failures or 3 distinct days of failures are summarized in the table.
-------------------------------------------------------

create or replace view v_corruptedFilesSiteSummary 
as
select sitename, count(*) as files,
max(nacc) as maxacc, min(nacc) as minacc,
max(ndays) as maxdays, min(ndays) as mindays
from MV_CorruptedFiles
where ndays >2 or nacc > 4
group by sitename
order by mindays desc;

select * from  v_corruptedFilesSiteSummary ;

