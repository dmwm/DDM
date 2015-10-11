-- This first part is copy&paste of MV_XRD_stat2

A = LOAD '$input' using JsonLoader('unique_id:chararray,file_lfn:chararray,file_size:chararray,start_time:chararray,end_time:chararray,read_bytes:chararray,read_operations:chararray,read_min:chararray,read_max:chararray,read_average:chararray,read_sigma:chararray,read_single_bytes:chararray,read_single_operations:chararray,read_single_min:chararray,read_single_max:chararray,read_single_average:chararray,read_single_sigma:chararray,read_vector_bytes:chararray,read_vector_operations:chararray,read_vector_min:chararray,read_vector_max:chararray,read_vector_average:chararray,read_vector_sigma:chararray,read_vector_count_min:chararray,read_vector_count_max:chararray,read_vector_count_average:chararray,read_vector_count_sigma:chararray,write_bytes:chararray,write_operations:chararray,write_min:chararray,write_max:chararray,write_average:chararray,write_sigma:chararray,read_bytes_at_close:chararray,write_bytes_at_close:chararray,user_dn:chararray,user_vo:chararray,user_role:chararray,user_fqan:chararray,client_domain:chararray,client_host:chararray,server_username:chararray,user_protocol:chararray,app_info:chararray,server_domain:chararray,server_host:chararray,server_site:chararray');

Aview = FOREACH A GENERATE (((long) end_time) * 1000) as cts, (LAST_INDEX_OF(file_lfn, '/store/') == -1 ? 'XXXXX' : SUBSTRING(file_lfn, LAST_INDEX_OF(file_lfn, '/store/'), 999)) as file_lfn, (long)read_bytes_at_close as readBytes;
Aview1 = FOREACH Aview GENERATE CONCAT ( (chararray)GetYear(ToDate(cts)), CONCAT('/', CONCAT( (chararray)GetMonth(ToDate(cts)), CONCAT('/', (chararray)GetDay(ToDate(cts)) ) ) ) ) as ctsYYMMDD, file_lfn, SUBSTRING(file_lfn, 0, LAST_INDEX_OF(file_lfn, '/')) as dirName, readBytes, 1 as Nentries;
AviewWhere = FILTER Aview1 BY file_lfn != 'XXXXX';

groupby = GROUP AviewWhere BY (ctsYYMMDD, dirName);

MV_XRD_stat2 = FOREACH groupby GENERATE FLATTEN(group), SUM(AviewWhere.readBytes) as readBytes;

-- End of MV_XRD_stat2

aggr1 = GROUP MV_XRD_stat2 BY (dirName);
select = FOREACH aggr1 GENERATE FLATTEN(group), MIN(MV_XRD_stat2.ctsYYMMDD) as min_tday, MAX(MV_XRD_stat2.ctsYYMMDD) as max_tday, SUM(MV_XRD_stat2.readBytes)/1000/1000 as readBytes, COUNT(MV_XRD_stat2.dirName) as read_acc;
result = ORDER select BY $3 ASC;

STORE result into '$output' USING PigStorage(',');
