-- MV for last_run
drop MATERIALIZED VIEW MV_last_run;
CREATE MATERIALIZED VIEW MV_last_run
COMPRESS
PCTFREE 0
BUILD IMMEDIATE
ENABLE QUERY REWRITE
AS
select cont, sitename, count(*) as nblocks,
sum(nacc) as snacc, sum(cputime) as scputime, sum(dssize) as sdssize
from cms_cleaning_agent.T_cleaned_dataset 
where 
runid in (select max(runid) from cms_cleaning_agent.T_cleaned_dataset)
--runid=5055
group by cont, sitename;

--exec DBMS_MVIEW.REFRESH('MV_last_run','C');
grant select on MV_last_run to CMS_CLEANING_AGENT_R;
