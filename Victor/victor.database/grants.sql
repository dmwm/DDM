--- @copyright: European Organization for Nuclear Research (CERN)
--- @author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011-2012
--- @license: Licensed under the Apache License, Version 2.0 (the "License");
--- You may not use this file except in compliance with the License.
--- You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
-- Grant writes to the reader account
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

GRANT SELECT ON T_ACCOUNTING_RECORD TO CMS_CLEANING_AGENT_R;
GRANT SELECT ON T_RUN               TO CMS_CLEANING_AGENT_R;
GRANT SELECT ON T_RUN_SITE          TO CMS_CLEANING_AGENT_R;
GRANT SELECT ON T_CLEANED_DATASET   TO CMS_CLEANING_AGENT_R;
GRANT SELECT ON T_RUN_CONFIG        TO CMS_CLEANING_AGENT_R;
commit;
