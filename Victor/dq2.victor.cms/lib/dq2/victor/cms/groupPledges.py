"""
@copyright: European Organization for Nuclear Research (CERN)
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

TiB = 2**40

groupPledges = {
'T2_AT_Vienna':        { 'susy': 50*TiB, 'b-tagging': 50*TiB, 'AnalysisOps': 50*TiB},
'T2_BE_IIHE':          { 'top': 150*TiB, 'jets-met_hcal': 50*TiB, 'AnalysisOps': 250*TiB},
'T2_BE_UCL':           { 'tracker-dpg':100*TiB, 'exotica': 100*TiB, 'AnalysisOps': 100*TiB},
'T2_BR_SPRACE':        { 'AnalysisOps': 200*TiB, 'exotica': 125*TiB, 'heavy-ions': 100*TiB, 'susy': 150*TiB},
'T2_BR_UERJ':          { 'b-tagging':100*TiB, 'forward':100*TiB, 'AnalysisOps': 150*TiB},
'T2_CH_CSCS':          { 'b-physics': 100*TiB, 'AnalysisOps': 100*TiB}, 
'T2_CN_Beijing':       { 'b-physics': 125*TiB, 'AnalysisOps': 125*TiB},
'T2_DE_DESY':          { 'forward': 125*TiB, 'top': 175*TiB, 'jets-met_hcal': 100*TiB, 'SMP': 100*TiB, 'AnalysisOps': 250*TiB},
'T2_DE_RWTH':          { 'susy': 150*TiB, 'tracker-pog': 100*TiB, 'AnalysisOps': 200*TiB},
'T2_EE_Estonia':       { 'tau-pflow': 100*TiB, 'susy': 100*TiB, 'exotica': 100*TiB, 'AnalysisOps': 300*TiB},
'T2_ES_CIEMAT':        { 'SMP': 75*TiB, 'muon': 75*TiB, 'trigger': 75*TiB, 'AnalysisOps': 200*TiB},
'T2_ES_IFCA':          { 'higgs':100*TiB, 'top': 100*TiB, 'AnalysisOps': 200*TiB},
'T2_FI_HIP':           { 'b-physics': 75*TiB, 'jets-met_hcal': 75*TiB, 'AnalysisOps': 100*TiB},
'T2_FR_CCIN2P3':       { 'SMP': 100*TiB, 'tracker-dpg': 50*TiB, 'tau-pflow': 50*TiB, 'AnalysisOps': 100*TiB},
'T2_FR_GRIF_IRFU':     { 'exotica': 125*TiB, 'AnalysisOps': 100*TiB},
'T2_FR_GRIF_LLR':      { 'heavy-ions': 75*TiB, 'higgs': 100*TiB, 'e-gamma_ecal': 50*TiB, 'AnalysisOps': 150*TiB},
'T2_FR_IPHC':          { 'top': 75*TiB, 'b-tagging': 75*TiB, 'AnalysisOps': 150*TiB},
'T2_GR_Ioannia':       { 'AnalysisOps': 50*TiB},
'T2_HU_Budapest':      { 'AnalysisOps': 75*TiB, 'b2g': 75*TiB},
'T2_IN_TIFR':          { 'SMP': 125*TiB, 'AnalysisOps': 150*TiB},
'T2_IT_Bari':          { 'susy': 125*TiB, 'higgs': 125*TiB, 'AnalysisOps': 150*TiB}, 
'T2_IT_Legnaro':       { 'SMP': 125*TiB, 'muon': 125*TiB, 'AnalysisOps': 200*TiB},
'T2_IT_Pisa':          { 'tracker-pog': 125*TiB, 'tau-pflow': 125*TiB, 'AnalysisOps': 200*TiB},
'T2_IT_Rome':          { 'higgs': 150*TiB, 'e-gamma_ecal': 100*TiB, 'AnalysisOps': 200*TiB},
'T2_PL_Warsaw':        { 'jets-met_hcal': 75*TiB, 'AnalysisOps': 50*TiB},
'T2_KR_KNU':           { 'jets-met_hcal': 75*TiB, 'AnalysisOps': 50*TiB},
'T2_PT_NCG_Lisbon':    { 'SMP': 75*TiB, 'AnalysisOps': 50*TiB},
'T2_RU_ITEP':          { 'jets-met_hcal': 50*TiB, 'AnalysisOps': 100*TiB},
'T2_RU_JINR':          { 'exotica': 75*TiB, 'muon': 75*TiB, 'AnalysisOps': 100*TiB},
'T2_RU_SINP':          { 'heavy-ions': 100*TiB, 'AnalysisOps': 100*TiB},
'T2_TR_METU':          { 'exotica': 50*TiB, 'heavy-ions': 50*TiB, 'AnalysisOps': 50*TiB},
'T2_TW_Taiwan':        { 'AnalysisOps': 100*TiB},
'T2_UA_KIPT':          { 'b2g': 100*TiB, 'AnalysisOps': 100*TiB},
'T2_UK_London_Brunel': { 'b2g': 125*TiB, 'exotica': 125*TiB, 'AnalysisOps': 150*TiB},
'T2_UK_London_IC':     { 'susy': 150*TiB, 'e-gamma_ecal': 100*TiB, 'higgs': 100*TiB, 'trigger': 100*TiB, 'AnalysisOps': 250*TiB},
'T2_UK_SGrid_RALPP':   { 'exotica': 125*TiB, 'top': 125*TiB, 'AnalysisOps': 200*TiB},
'T2_US_Caltech':       { 'b2g': 100*TiB, 'SMP': 75*TiB, 'e-gamma_ecal': 150*TiB, 'AnalysisOps': 250*TiB},
'T2_US_Florida':       { 'susy': 125*TiB, 'muon': 75*TiB, 'tau-pflow': 75*TiB, 'higgs': 125*TiB, 'AnalysisOps': 275*TiB},
'T2_US_MIT':           { 'b2g': 100*TiB, 'higgs': 150*TiB, 'jets-met_hcal': 75*TiB, 'AnalysisOps': 250*TiB},
'T2_US_Nebraska':      { 'b2g': 100*TiB, 'b-tagging': 100*TiB, 'tracker-dpg': 100*TiB, 'top': 125*TiB, 'AnalysisOps': 250*TiB},
'T2_US_Purdue':        { 'b-physics': 125*TiB, 'exotica': 125*TiB, 'muon': 75*TiB, 'AnalysisOps': 250*TiB},
'T2_US_UCSD':          { 'tracker-pog': 100*TiB, 'susy': 150*TiB, 'e-gamma_ecal': 75*TiB, 'AnalysisOps': 250*TiB},
'T2_US_Vanderbilt':    { 'heavy-ions': 525*TiB},
'T2_US_Wisconsin':     { 'forward': 125*TiB, 'trigger': 75*TiB, 'SMP': 125*TiB, 'AnalysisOps': 250*TiB}
}

