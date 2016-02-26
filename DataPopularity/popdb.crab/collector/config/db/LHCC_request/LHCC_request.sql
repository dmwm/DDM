alter session set NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS';


--drop MATERIALIZED VIEW MV_LHCC_report_1;
commit ;

CREATE MATERIALIZED VIEW MV_LHCC_report_1
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select  filename, inputcollection,
 count(*) as numAccesses, sum(CPUTIME) as totCPU
from raw_file 
where fileexitflag=1 and InputCollection != 'unknown'
and finishedtimestamp > '2013-01-01' and finishedtimestamp < '2013-06-30'
group by filename, inputcollection
;

commit ;


--drop MATERIALIZED VIEW MV_LHCC_report_2;
commit ;

CREATE MATERIALIZED VIEW MV_LHCC_report_2
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
AS
select  filename, inputcollection,
 count(*) as numAccesses, sum(CPUTIME) as totCPU
from raw_file 
where fileexitflag=1 and InputCollection != 'unknown'
and finishedtimestamp > '2013-07-01' and finishedtimestamp < '2013-12-31'
group by filename, inputcollection
;

commit ;

-----------------------------------------

select numaccesses, count(*) from MV_LHCC_report_1
where 
substr(inputcollection,instr(inputcollection,'/',-1)+1)='AOD' 
--or 
--substr(inputcollection,instr(inputcollection,'/',-1)+1)='AODSIM' 
group by numaccesses 
order by numaccesses
;