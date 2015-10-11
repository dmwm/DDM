-- This first part is copy&paste of MV_XRD_stat0_pre

A = LOAD '$input' using JsonLoader('unique_id:chararray,file_lfn:chararray,file_size:chararray,start_time:chararray,end_time:chararray,read_bytes:chararray,read_operations:chararray,read_min:chararray,read_max:chararray,read_average:chararray,read_sigma:chararray,read_single_bytes:chararray,read_single_operations:chararray,read_single_min:chararray,read_single_max:chararray,read_single_average:chararray,read_single_sigma:chararray,read_vector_bytes:chararray,read_vector_operations:chararray,read_vector_min:chararray,read_vector_max:chararray,read_vector_average:chararray,read_vector_sigma:chararray,read_vector_count_min:chararray,read_vector_count_max:chararray,read_vector_count_average:chararray,read_vector_count_sigma:chararray,write_bytes:chararray,write_operations:chararray,write_min:chararray,write_max:chararray,write_average:chararray,write_sigma:chararray,read_bytes_at_close:chararray,write_bytes_at_close:chararray,user_dn:chararray,user_vo:chararray,user_role:chararray,user_fqan:chararray,client_domain:chararray,client_host:chararray,server_username:chararray,user_protocol:chararray,app_info:chararray,server_domain:chararray,server_host:chararray,server_site:chararray');

B = LOAD '/user/mmeoni/CMS_file2DS.csv' using PigStorage(',') as (storename:chararray, blockname:chararray, dsname:chararray, fullname:chararray);

Aview = FOREACH A GENERATE (((long) start_time) * 1000) as ots, (((long) end_time) * 1000) as cts, (LAST_INDEX_OF(file_lfn, '/store/') == -1 ? 'XXXXX' : SUBSTRING(file_lfn, LAST_INDEX_OF(file_lfn, '/store/'), 999)) as file_lfn, client_host, server_username, ((long)end_time - (long)start_time) as procTime, (long)read_bytes_at_close as readBytes, server_domain;
Aview1 = FOREACH Aview GENERATE CONCAT ( (chararray)GetYear(ToDate(cts)), CONCAT('/', CONCAT( (chararray)GetMonth(ToDate(cts)), CONCAT('/', (chararray)GetDay(ToDate(cts)) ) ) ) ) as ctsYYMMDD, cts, file_lfn, client_host, server_username, procTime, readBytes, server_domain;
AviewWhere = FILTER Aview1 BY procTime > 0 AND file_lfn != 'XXXXX';

Bview = FOREACH B GENERATE REPLACE(storename, '\\"', '') as fullname;

view = JOIN AviewWhere BY file_lfn, Bview BY fullname;
groupby = GROUP view BY (ctsYYMMDD, client_host, server_username, fullname);

MV_XRD_stat0_pre = FOREACH groupby GENERATE FLATTEN(group), COUNT(view.client_host) as numAccesses, SUM(view.procTime) as procTime, SUM(view.readBytes) as readBytes;

-- This first part is copy&paste of MV_XRD_stat0_pre

select = FOREACH MV_XRD_stat0_pre GENERATE GetWeek(ToDate(ctsYYMMDD, 'yyyy/MM/dd')) as week, 'T2_CH_CERN' as sitename, fullname as collName;
aggr   = GROUP select BY (sitename, collName);
result = FOREACH aggr GENERATE MAX(select.week) as TDAY, FLATTEN(group);

STORE result into '$output' USING PigStorage(',');
