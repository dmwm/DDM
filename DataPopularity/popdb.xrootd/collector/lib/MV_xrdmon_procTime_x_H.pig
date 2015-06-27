data = LOAD '$input' using PigStorage(',') as (lfn:chararray, ruid:int, rgid:int, td:chararray, host:chararray, fid:int, fsid:chararray, ots:long, otms:int, cts:long, ctms:int, rb:int, wb:int, sfwdb:int, sbwdb:int, sxlfwdb:int, sxlbwdb:int, nrc:int, nwc:int, nfwds:int, nbwds:int, nxlfwds:int, nxlbwds:int, rt:int, wt:int, osize:int, csize:int, secname:chararray, sechost:chararray, secvorg:chararray, secgrps:chararray, secrole:chararray, secapp:chararray);

view = FOREACH data GENERATE GetYear(ToDate(ots * 1000)) as otsYY, GetMonth(ToDate(ots * 1000)) as otsMM, GetDay(ToDate(ots * 1000)) as otsDD, lfn, rb, (cts - ots) as procTime, (rb / (cts - ots)) as readRate, host, FLOOR(LOG10(cts - ots)) as decade;

result = FILTER view BY procTime > 0;

STORE result into '$output' USING PigStorage(',');