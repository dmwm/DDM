--list me the sites in which victor is going to delete the same DS
create or replace view v_duplicatedRemovals
as
select s.cont, s.sitename, s.snacc, s.nblocks, t.Nsites from cms_cleaning_agent.MV_last_run s
inner join (
select count(distinct sitename) as Nsites, cont 
from cms_cleaning_agent.MV_last_run
group by cont
) t 
ON s.cont=t.cont 
order by s.cont
;

select * from v_duplicatedRemovals;