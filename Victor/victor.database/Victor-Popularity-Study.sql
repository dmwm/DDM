alter session set NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS';


select * from T_RUN;

select distinct (total) , sitename  from cms_cleaning_agent.T_Accounting_record;


select * from  cms_cleaning_agent.T_Accounting_record, t_run
where sitename like 'T2_IT_Bari^higgs' and t_run.runid=T_Accounting_record.runid
order by rundate desc;

select cont from (
select distinct cont from cms_cleaning_agent.T_cleaned_dataset 
where (runid = 5028 ) and sitename = 'T2_IT_Bari^higgs'
minus
select distinct cont from cms_cleaning_agent.T_cleaned_dataset 
where ( runid =5048) and sitename = 'T2_IT_Bari^higgs'
)
intersect
select  distinct(collname) from CMS_POPULARITY_SYSTEM.MV_DS_stat0 where sitename = 'T2_IT_Bari' and tday > '2012-08-24';
;



select cont from (
select distinct cont from cms_cleaning_agent.T_cleaned_dataset 
where (runid = 5028 ) and sitename = 'T2_IT_Bari^higgs'
minus
select distinct cont from cms_cleaning_agent.T_cleaned_dataset 
where ( runid =5048) and sitename = 'T2_IT_Bari^higgs'
)
minus
select  distinct(collname) from CMS_POPULARITY_SYSTEM.MV_DS_stat0 where sitename = 'T2_IT_Bari' and tday > '2012-08-24';
;


select * from cms_cleaning_agent.T_cleaned_dataset;




select cont, sitename, runid,
sum(nacc), sum(cputime), sum(dssize) as dssize
from cms_cleaning_agent.T_cleaned_dataset 
group by cont, sitename, runid 
order by runid desc , dssize desc;


select cont, sitename, rundate,
sum(t.nacc), sum(t.cputime), sum(t.dssize) as dssize
from 
cms_cleaning_agent.T_cleaned_dataset t,
cms_cleaning_agent.T_run r 
where t.runid=r.runid and cont = '/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM'
group by cont, sitename, rundate
order by rundate desc , dssize desc;



-- In how many sites victor is going to delete the same DS?
select Nsites, count(*) as entries from 
(
select count(distinct sitename) as Nsites, cont 
from cms_cleaning_agent.MV_last_run 
group by cont
) group by Nsites
order by entries desc;


select * from v_duplicatedremovals;

-- Find in popularity the overall (and by site) accesses in the last 3 weeks of the datasets victor is going to delete 

select collname, sitename, trunc(tday,'WW') as tday, 
sum(numaccesses) as numaccesses, sum(totcpu) as totcpu, sum(numusers) as numusers
from CMS_POPULARITY_SYSTEM.MV_DS_stat0_aggr1 where
collname in (select distinct cont from v_duplicatedremovals where nsites=3) 
and sitename like 'T2%' 
and tday > '2012-08-18'
and tday < '2012-08-23'
group by collname, sitename, trunc(tday,'WW')
order by collname, tday desc, numaccesses, sitename
;

--Comment: there are case in which in a site we decide to cancel blocks unpopular for the site, but not for the rest of the WLCG. 
-- this can be dangerous without a dynamic palcement, so, it woudl be better to not remove blocks for DS that have some popularity in the last 30 days???


-- Let's now work on DS removed from a single site
select distinct cont from v_duplicatedremovals where nsites=1 order by cont;

select collname, sitename, trunc(tday,'WW') as tday, 
sum(numaccesses) as numaccesses, sum(totcpu) as totcpu, sum(numusers) as numusers
from CMS_POPULARITY_SYSTEM.MV_DS_stat0_aggr1 where
collname in (select distinct cont from v_duplicatedremovals where nsites=1)
and sitename like 'T2%' 
and tday > '2012-08-18'
and tday < '2012-08-23'
group by collname, sitename, trunc(tday,'WW')
order by collname, tday desc, numaccesses, sitename
;


-- How many ds removed by victor are not in any other site
select count( distinct cont), nsites from v_duplicatedremovals
where
cont not in 
(select distinct collname
from CMS_POPULARITY_SYSTEM.MV_DS_stat0_aggr1
where
sitename like 'T2%' 
and tday > '2012-07-23'
and tday < '2012-08-23'
) group by nsites
;

-------------------------------------------
-------------------------------------------
-------------------------------------------

create or replace view v_summary_pop 
as
select collname, sitename, 
sum(numaccesses) as numaccesses, sum(totcpu) as totcpu, sum(numusers) as numusers
from CMS_POPULARITY_SYSTEM.MV_DS_stat0_aggr1 where
sitename like 'T2%' 
and Tday > trunc(systimestamp - interval '30' day,'W') 
group by collname, sitename;


select * from  v_summary_pop;

-- view of the DS which blocks are identified by victor that have no
-- popularity at all (nacc=0) in the specific site -- including also the other blocks --

create or replace view v_victords_fullyunpop
as
select t.cont, regexp_replace(t.sitename, '(.*)\^(.*)','\1') as sitename, t.sitename as sitegroup,
t.snacc, t.nblocks
from v_duplicatedremovals t
left JOIN v_summary_pop s
ON t.cont=s.collname and regexp_replace(t.sitename, '(.*)\^(.*)','\1')=s.sitename
WHERE s.numaccesses is null 
order by cont, sitename
;


select count(distinct cont) from v_victords_fullyunpop; -- where sitename like 'T2_CH%';

select * from v_victords_fullyunpop;

-- view of the popularity in other sites of the DS that are identified in victor as to be removed
create or replace view v_pop_of_victords
as
select s.cont as collname, t.sitename as otherSite, numaccesses, totcpu, numusers,
 s.sitename as asitename, sitegroup, snacc, nblocks from v_summary_pop t
right join
v_victords_fullyunpop s
ON
collname = cont
and t.sitename != s.sitename
order by collname, numaccesses desc;


---Number of other popular sites 
select Nsitespop, count(*) entries from (
select collname, count(distinct othersite) as NsitesPop, count(distinct sitegroup) 
from v_pop_of_victords
group by collname
) group by Nsitespop order by nsitespop
;

--let's search for the collections, sites with 10

select * from (
select collname, count(distinct othersite) as NsitesPop, count(distinct sitegroup) 
from v_pop_of_victords
group by collname
)
where NsitesPop = 4;


--COLLNAME                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         NSITESPOP              COUNT(DISTINCTSITEGROUP) 
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------- ------------------------ 
--/QCD_Pt-300to470_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM                                                                                                                                                                                                                                                                                                                                                                                                                                       10                     1                        
--/WWJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM   


select othersite, numaccesses, round(totcpu/3600), numusers, sitegroup
from v_pop_of_victords where
collname='/WToLNu_1jEnh2_2jEnh35_3jEnh40_4jEnh50_7TeV-sherpa/Fall11-PU_S6_START42_V14B-v1/AODSIM'
--collname = '/WH_ZH_TTH_HToTauTau_M-120_8TeV-pythia6-tauola/Summer12-PU_S7_START52_V9-v2/AODSIM'
--collname = '/QCD_Pt-300to470_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM'
--or
--collname = '/WWJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM'
;

--------------------------------------------------------------------------------
--- TESTS
select * from v_pop_of_victords;

select * from v_pop_of_victords where asitename = 'T2_CH_CSCS';
select * from v_summary_pop where sitename = 'T2_BR_SPRACE' and collname = '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12-E8TeV4BX50ns-v1/AODSIM';

select * from CMS_POPULARITY_SYSTEM.MV_DS_stat0_aggr1
 where sitename = 'T2_BR_SPRACE' and collname = '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12-E8TeV4BX50ns-v1/AODSIM';
--------------------------------------------------------------------------------

select collname, count(distinct othersite) as NsitesPop, count(distinct sitegroup) 
from v_pop_of_victords
group by collname
;

-------------------------------------------------
--- Find the last week of activity of a dataset
create or replace view v_lastweek_pop 
as
select collname, sitename, max(trunc(tday,'W')) as lastWeek
from 
CMS_POPULARITY_SYSTEM.MV_DS_stat0_aggr1
group by collname, sitename;

select * from v_lastweek_pop;


create or replace view v_lastpop_of_victords
as
select s.cont as collname, sitegroup, snacc, nblocks, lastweek from v_lastweek_pop t
right join
v_victords_fullyunpop s
ON
collname = cont
and t.sitename = s.sitename
where snacc=0
order by collname, s.sitename desc;

select lastweek, count from v_lastpop_of_victords;





















select max(Tday), collname
from (
select t.tday, t.sitename as sitename, t.collname, t.numaccesses, s.sitename as bsitename from CMS_POPULARITY_SYSTEM.MV_DS_stat0_aggr1  t ,  v_victords_fullyunpop s
where collname = cont and t.sitename != s.sitename
and collname != 'unknown'
and t.sitename != 'unknown'
) group by collname 
order by max(Tday) desc;

select * from CMS_POPULARITY_SYSTEM.MV_DS_stat0_aggr1;


drop table T_accounting_record_test;
create table  T_accounting_record_test
as (select * from t_accounting_record);



update T_accounting_record t 
set total = (select total from T_accounting_record_bkp u
where u.runid = 3167 and u.sitename=t.sitename
) where t.runid<=3147;


select * from t_accounting_record t, t_accounting_record_test u
where t.runid=u.runid and t.sitename=u.sitename and t.total!=u.total;

select * from t_accounting_record_bkp where sitename like 'T2_US_Vanderbilt^heavy ions';


select count( distinct total )-1  as acount , sitename 
from t_accounting_record_bkp
group by sitename
order by acount desc, sitename
;

select count (distinct sitename) from t_accounting_record_bkp;

select count(*) from (
select distinct(total), sitename from t_accounting_record_test
order by sitename
);

select * from (select distinct(total) as atotal, sitename as asitename from t_accounting_record_bkp) t
left join (select * from (select distinct(total) as btotal, sitename as bsitename from t_accounting_record_test) u )
ON asitename = bsitename and atotal = btotal
where btotal is null ;

select distinct(total), sitename from t_accounting_record_test
order by sitename;


-------------------------------------------
select * from T_Cleaned_dataset where 
cont like '%Fall10-START38_V12-v1/AODSIM%'
order by runid desc;


select distinct  cont, sitename from  T_Cleaned_dataset
where sitename like 'T2_BE_UCL%' and runid = (select max(runid) from T_Cleaned_dataset)
order by sitename;


select * from T_Cleaned_dataset where 
runid = (select max(runid) from T_Cleaned_dataset) and sitename like 'T2_BE_UCL^An%';

select distinct runid from T_Cleaned_dataset order by runid desc;

select * from 
(select count (distinct cont) prod_before_counts, sitename from T_Cleaned_dataset where 
(runid = 5055) and sitename like 'T2_%' group by  sitename) t, (
select count (distinct cont) prod_after_counts,  sitename from T_Cleaned_dataset where 
(runid = 5067) and sitename like 'T2_%' group by  sitename ) u 
where t.sitename=u.sitename
order by t.sitename;

select max(runid) from T_Cleaned_dataset;
------
--ONLY in DEVDB11

select * from t_cleaned_dataset where runid=5064; 

select conteggi, count(*) from
(
select round(count(nblock)/nblock/5,2)*500 as conteggi,  sitename , cont
from cms_cleaning_agent.t_cleaned_dataset where runid= (select max(runid) from cms_cleaning_agent.t_cleaned_dataset)
--and nblock is not null
group by sitename, cont, nblock
)
group by conteggi
order by conteggi
;

select * from cms_cleaning_agent.t_cleaned_dataset
where runid=5067;

