-- REGISTER /Users/me/commiter/piggybank/java/piggybank.jar ; 
-- DEFINE ISOToUnix org.apache.pig.piggybank.evaluation.datetime.convert.ISOToUnix();

data = LOAD '$input' using JsonLoader('unique_id:chararray,file_lfn:chararray,file_size:chararray,start_time:chararray,end_time:chararray,read_bytes:chararray,read_operations:chararray,read_min:chararray,read_max:chararray,read_average:chararray,read_sigma:chararray,read_single_bytes:chararray,read_single_operations:chararray,read_single_min:chararray,read_single_max:chararray,read_single_average:chararray,read_single_sigma:chararray,read_vector_bytes:chararray,read_vector_operations:chararray,read_vector_min:chararray,read_vector_max:chararray,read_vector_average:chararray,read_vector_sigma:chararray,read_vector_count_min:chararray,read_vector_count_max:chararray,read_vector_count_average:chararray,read_vector_count_sigma:chararray,write_bytes:chararray,write_operations:chararray,write_min:chararray,write_max:chararray,write_average:chararray,write_sigma:chararray,read_bytes_at_close:chararray,write_bytes_at_close:chararray,user_dn:chararray,user_vo:chararray,user_role:chararray,user_fqan:chararray,client_domain:chararray,client_host:chararray,server_username:chararray,user_protocol:chararray,app_info:chararray,server_domain:chararray,server_host:chararray,server_site:chararray');

view = FOREACH data GENERATE (((long) start_time) * 1000) as ots, (((long) end_time) * 1000) as cts, INDEXOF(file_lfn, '/replicate') as replica;
view1 = FOREACH view GENERATE GetYear(ToDate(ots)) as otsYY, GetMonth(ToDate(ots)) as otsMM, GetDay(ToDate(ots)) as otsDD, GetYear(ToDate(cts)) as ctsYY, GetMonth(ToDate(cts)) as ctsMM, GetDay(ToDate(cts)) as ctsDD, replica;
view2 = FOREACH view1 GENERATE CONCAT( (chararray)otsYY, CONCAT('/', CONCAT( (chararray)otsMM, CONCAT('/', (chararray)otsDD ) ) ) ) as ots, CONCAT( (chararray)ctsYY, CONCAT('/', CONCAT( (chararray)ctsMM, CONCAT('/', (chararray)ctsDD ) ) ) ) as cts, replica;

groupby = GROUP view2 BY (ots, cts, replica);
result = FOREACH groupby GENERATE FLATTEN(group), COUNT(view2.replica);

STORE result into '$output' USING PigStorage(',');
