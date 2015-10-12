B = LOAD '/user/mmeoni/CMS_file2DS.csv' using PigStorage(',') as (storename:chararray, blockname:chararray, dsname:chararray, fullname:chararray);

Bview = FOREACH B GENERATE REPLACE(blockname, '\\"', '') as blockname, dsname;

result = DISTINCT Bview;

STORE result into '$output' USING PigStorage(',');
