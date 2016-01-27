
create or replace
PROCEDURE corruptedFileREFRESH  IS
BEGIN


merge into T_CORRUPTEDFILES D
using (
select trunc(FinishedTimeStamp) as TDAY, sitename, sum(fileexitflag) as sumFlag, count(*) as nAcc, filename, jobexecexitcode as jobexitcode
from raw_file                                                                                                                                                                                   
    where                                                                                                                                                                                                                                                                     
    trunc(finishedtimestamp) = trunc(systimestamp - interval '1' day)     
    and                                                                                                                                                                                                                                                                       
    (fileexitflag=0 or fileexitflag=1)                                                                                                                                                                                                                                        
    group by trunc(FinishedTimeStamp), sitename, filename, jobexecexitcode  
) S
ON (S.TDAY = D.TDAY and S.sitename = D.sitename and S.filename = D.filename and S.jobexitcode = D.jobexitcode)
WHEN NOT MATCHED THEN INSERT 
(D.TDAY, D.sitename, D.sumflag , D.nacc, D.filename, D.jobexitcode)
VALUES
(S.TDAY, S.sitename, S.sumflag , S.nacc, S.filename, S.jobexitcode)
;

delete from  T_CORRUPTEDFILES where TDAY < trunc(systimestamp - interval '15' day) ;

END;

