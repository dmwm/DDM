
insert into T_CORRUPTEDFILES 
(TDAY, sitename, sumflag , nacc, filename, jobexitcode)
select trunc(FinishedTimeStamp) as TDAY, sitename, sum(fileexitflag) as sumFlag, count(*) as nAcc, filename, jobexecexitcode from raw_file                                                                                                                                                                                   
    where                                                                                                                                                                                                                                                                     
     trunc(finishedtimestamp) > trunc(systimestamp - interval '16' day)   
    and
    trunc(finishedtimestamp) < trunc(systimestamp - interval '1' day)           
    and                                                                                                                                                                                                                                                                       
    (fileexitflag=0 or fileexitflag=1)       
    group by trunc(FinishedTimeStamp), sitename, filename, jobexecexitcode  
; 

select sumflag, nacc, jobexitcode, count(*) 
from T_CORRUPTEDFILES group by sumflag, nacc, jobexitcode 
order by  sumflag, nacc, jobexitcode;