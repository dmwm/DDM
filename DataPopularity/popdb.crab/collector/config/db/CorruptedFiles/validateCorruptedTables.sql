alter session set NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS';


select tday, count(*)
from T_CORRUPTEDFILES
group by tday 
order by tday
;

select sitename, count(*) as files, round(sum(nacc)/count(*),1) as average, max(nacc) as maximum,
SUBSTR(filename,1,INSTR(filename,'/',1,6)) as path
from MV_CorruptedFiles 
where sumflag=0
group by sitename, SUBSTR(filename,1,INSTR(filename,'/',1,6))
order by average desc, sitename;

select sitename, count(*) as files, round(sum(nacc)/count(*),1) as average, max(nacc) as maximum 
from MV_CorruptedFiles
where sumflag=0
group by sitename
order by average desc;


-------------------------------------

select sitename,  nacc,  sumflag, filename  from mv_corruptedfiles
where sumflag=0 
order by nacc, sitename, filename;

----------------------------------------

select * from (
select sitename, sum(nacc) as nacc, sum(sumflag) as sumflag, filename 
from MV_corruptedfiles_A 
group by sitename, filename
)
where sumflag=0
order by nacc , sitename, filename;

----------------------------------------

select sitename,  nacc,  sumflag, filename  from (
select sitename, sum(nacc) as nacc, sum(sumflag) as sumflag, filename 
from MV_corruptedfiles_A 
group by sitename, filename
)
where sumflag=0
MINUS
select b.sitename,  b.nacc,  b.sumflag, b.filename  
from mv_corruptedfiles b
where b.sumflag=0 
order by nacc, sitename, filename;

----------------------------------------

select * from T_corruptedfiles order by tday;

----------------------------------------

-- Comparison T_corruptedfiles Vs MV_corruptedfiles_A

-- all the comparisons provide the same results

select distinct tday, count(*) from T_corruptedfiles group by tday order by tday;

select distinct tday, count(*) from MV_corruptedfiles_A group by tday order by tday;


select b.sitename,  b.nacc,  b.sumflag, b.filename  
from v_corruptedfiles b
where b.sumflag=0
MINUS
select sitename,  nacc,  sumflag, filename  from (
select sitename, sum(nacc) as nacc, sum(sumflag) as sumflag, filename 
from MV_corruptedfiles_A 
group by sitename, filename
)
where sumflag=0 
order by nacc, sitename, filename;

----------------------------------------

-- Comparison T_corruptedfiles Vs MV_corruptedfiles

-- all comparisons match

select b.sitename,  b.nacc,  b.sumflag, b.filename  
from v_corruptedfiles b
where b.sumflag=0
minus
select sitename,  nacc,  sumflag, filename  from mV_corruptedfiles
where sumflag=0 
order by nacc, sitename, filename;
-------------------------------------------


select * from (
select sitename, sum(nacc) as nacc, sum(sumflag) as sumflag, filename 
from T_corruptedfiles 
group by sitename, filename
)
where sumflag=0
order by nacc , filename;

select * from V_corruptedfiles
where sumflag=0
order by nacc desc, filename;
----------------------------------------


select * from v_corruptedFilesDSSummary ;

select * from v_corruptedFilesSiteSummary ;

select * from v_corruptedFilesDetail;
where nacc order by nacc ;


select sitename, nAcc, ndays , nacc/ndays , filename from v_corruptedFilesDetail
where sitename = 'T2_FR_IPHC'and filename like '/store/mc/Fall11/G_Pt-800to1400_TuneZ2_7TeV_pythia6/AODSIM/%' ;


select sitename, count(*) as files, 
round(sum(nacc)/count(*),1) as meanAcc, max(nacc) as maxAcc, min(nacc) as minAcc,
round(sum(ndays)/count(*),1) as meanDay, max(ndays) as maxDay, min(ndays) as minDay,
SUBSTR(filename,1,INSTR(filename,'/',1,6)) as path
from MV_CorruptedFiles 
where nacc > 5 or ndays > 3
--sitename = 'T2_FR_IPHC'and filename like '/store/mc/Fall11/G_Pt-800to1400_TuneZ2_7TeV_pythia6/AODSIM/%' 
group by sitename, SUBSTR(filename,1,INSTR(filename,'/',1,6))
order by meanAcc desc, sitename;

select * from  v_corruptedFilesDetail 
where nacc>5 or ndays > 3;


select jobexecexitcode, count(*) from raw_file                                                                                                                                                                                   
    where                                                                                                                                                                                                                                                                     
    trunc(finishedtimestamp) > trunc(systimestamp - interval '15' day) 
    and                                                                                                                                                                                                                                                                       
    fileexitflag=0  group by jobexecexitcode
;

select count(*) 
from  MV_CorruptedFiles_test ;

select count(*) from v_corruptedFilesDetail;

select * from (
select sitename, count(distinct tday) as ndays, sum(nacc) as nacc, sum(sumflag) as sumflag, filename 
from T_corruptedfiles group by sitename, filename
) where sumflag=0 
;

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
or JobExitCode = 8028 )
group by sitename, filename;

select r.sitename, r.ndays, r.nacc, r.filename from v_files_with_openProblem r
inner join v_files_with_sumflag0 s
on r.sitename = s.sitename and r.filename = s.filename
;

select * from MV_corruptedfiles
order by nacc desc;

select count(*) from MV_CORRUPTEDFILES_test where sitename like 'T2%';
