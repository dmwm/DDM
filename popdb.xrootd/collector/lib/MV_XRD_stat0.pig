A = LOAD '$input' using PigStorage(',') as (lfn:chararray, ruid:long, rgid:long, td:chararray, host:chararray, fid:long, fsid:chararray, ots:long, otms:long, cts:long, ctms:long, rb:long, wb:long, sfwdb:long, sbwdb:long, sxlfwdb:long, sxlbwdb:long, nrc:long, nwc:long, nfwds:long, nbwds:long, nxlfwds:long, nxlbwds:long, rt:long, wt:long, osize:long, csize:long, secname:chararray, sechost:chararray, secvorg:chararray, secgrps:chararray, secrole:chararray, secapp:chararray);
B = LOAD '/user/mmeoni/CMS_file2DS.csv' using PigStorage(',') as (storename:chararray, blockname:chararray, dsname:chararray, fullname:chararray);

Aview = FOREACH A GENERATE lfn, CONCAT ( (chararray)GetYear(ToDate(ots * 1000)), CONCAT('/', CONCAT( (chararray)GetMonth(ToDate(ots * 1000)), CONCAT('/', (chararray)GetDay(ToDate(ots * 1000)) ) ) ) ) as ots, SUBSTRING(td, 0, INDEXOF(td, '.')) as username, nrc as numAccesses, rt as procTime, rb as readBytes;
AviewWhere = FILTER Aview BY numAccesses > 0;
Bview = FOREACH B GENERATE REPLACE(fullname, '\\"', '') as fullname, REPLACE(dsname, '\\"', '') as dsname;

view = JOIN AviewWhere BY lfn, Bview BY fullname;
groupby = GROUP view BY (ots, username, dsname);

result = FOREACH groupby GENERATE FLATTEN(group), SUM(view.numAccesses), SUM(view.procTime), SUM(view.readBytes);

STORE result into '$output' USING PigStorage(',');