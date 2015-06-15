data = LOAD '$input' using PigStorage(',') as (lfn:chararray, ruid:int, rgid:int, td:chararray, host:chararray, fid:int, fsid:chararray, ots:long, otms:int, cts:long, ctms:int, rb:int, wb:int, sfwdb:int, sbwdb:int, sxlfwdb:int, sxlbwdb:int, nrc:int, nwc:int, nfwds:int, nbwds:int, nxlfwds:int, nxlbwds:int, rt:int, wt:int, osize:int, csize:int, secname:chararray, sechost:chararray, secvorg:chararray, secgrps:chararray, secrole:chararray, secapp:chararray);

view = FOREACH data GENERATE GetYear(ToDate(ots * 1000)) as otsYY, GetMonth(ToDate(ots * 1000)) as otsMM, GetDay(ToDate(ots * 1000)) as otsDD, GetHour(ToDate(ots * 1000)) as otsHH, GetYear(ToDate(cts * 1000)) as ctsYY, GetMonth(ToDate(cts * 1000)) as ctsMM, GetDay(ToDate(cts * 1000)) as ctsDD, GetHour(ToDate(cts * 1000)) as ctsHH, INDEXOF(lfn, '/replicate') as replica;

groupby = GROUP view BY (otsYY, otsMM, otsDD, otsHH, ctsYY, ctsMM, ctsDD, ctsHH, replica);

result = FOREACH groupby GENERATE FLATTEN(group), COUNT(view.replica);

STORE result into '$output' USING PigStorage(',');