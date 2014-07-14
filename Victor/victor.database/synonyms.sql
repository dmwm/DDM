-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
-- Create public synonyms for all tables
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

CREATE SYNONYM T_RUN_CONFIG for CMS_CLEANING_AGENT.T_RUN_CONFIG;
CREATE SYNONYM t_cleaned_dataset for CMS_CLEANING_AGENT.t_cleaned_dataset;
CREATE SYNONYM t_accounting_record for CMS_CLEANING_AGENT.t_accounting_record;
CREATE SYNONYM t_run_site for CMS_CLEANING_AGENT.t_run_site;
CREATE SYNONYM t_run for CMS_CLEANING_AGENT.t_run;

commit;
