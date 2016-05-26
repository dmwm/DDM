"""
@copyright: European Organization for Nuclear Research (CERN)
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

TiB = 2**40
TB = 10**12

groupPledges = {
 'T1_DE_KIT_Disk'       :{'AnalysisOps':  720*TB},
 'T1_ES_PIC_Disk'       :{'AnalysisOps': 1080*TB},
 'T1_FR_CCIN2P3_Disk'   :{'AnalysisOps': 1900*TB},
 'T1_IT_CNAF_Disk'      :{'AnalysisOps': 1800*TB},
 'T1_RU_JINR_Disk'      :{'AnalysisOps': 1800*TB},
 'T1_UK_RAL_Disk'       :{'AnalysisOps':  600*TB},
 'T1_US_FNAL_Disk'      :{'AnalysisOps': 4800*TB},
 'T2_AT_Vienna'	        :{'AnalysisOps':  340*TB},
 'T2_BE_IIHE'	        :{'AnalysisOps':  900*TB},
 'T2_BE_UCL'	        :{'AnalysisOps':  700*TB},
 'T2_BR_SPRACE'	        :{'AnalysisOps': 1000*TB},
 'T2_BR_UERJ'           :{'AnalysisOps':  350*TB},
 'T2_CH_CERN'	        :{'AnalysisOps': 1400*TB},
 'T2_CH_CSCS'	        :{'AnalysisOps':  625*TB},
 'T2_CN_Beijing'	:{'AnalysisOps':  220*TB},
 'T2_DE_DESY'	        :{'AnalysisOps': 1100*TB},
 'T2_DE_RWTH'	        :{'AnalysisOps':  550*TB},
 'T2_EE_Estonia'	:{'AnalysisOps':  700*TB},
 'T2_ES_CIEMAT'	        :{'AnalysisOps':  600*TB},
 'T2_ES_IFCA'	        :{'AnalysisOps':  550*TB},
 'T2_FI_HIP'	        :{'AnalysisOps':  680*TB},
 'T2_FR_CCIN2P3'	:{'AnalysisOps':  300*TB},
 'T2_FR_GRIF_IRFU'	:{'AnalysisOps':  300*TB},
 'T2_FR_GRIF_LLR'	:{'AnalysisOps':  300*TB},
 'T2_FR_IPHC'	        :{'AnalysisOps':  500*TB},
 'T2_GR_Ioannina'       :{'AnalysisOps':  120*TB},
 'T2_HU_Budapest'	:{'AnalysisOps':  300*TB},
 'T2_IN_TIFR'	        :{'AnalysisOps':  750*TB},
 'T2_IT_Bari'	        :{'AnalysisOps':  560*TB},
 'T2_IT_Legnaro'	:{'AnalysisOps':  820*TB},
 'T2_IT_Pisa'	        :{'AnalysisOps':  650*TB},
 'T2_IT_Rome'	        :{'AnalysisOps':  550*TB},
 'T2_KR_KNU'	        :{'AnalysisOps':  500*TB},
 'T2_MY_UPM_BIRUNI'     :{'AnalysisOps':   10*TB},
 'T2_PK_NCP'            :{'AnalysisOps':   90*TB},
 'T2_PL_Swierk'         :{'AnalysisOps':  150*TB},
 'T2_PL_Warsaw'         :{'AnalysisOps':   90*TB},
 'T2_PT_NCG_Lisbon'	:{'AnalysisOps':  100*TB},
 'T2_RU_IHEP'	        :{'AnalysisOps':  200*TB},
 'T2_RU_INR'	        :{'AnalysisOps':  200*TB},
 'T2_RU_ITEP'	        :{'AnalysisOps':  200*TB},
 'T2_RU_JINR'	        :{'AnalysisOps':  200*TB},
 'T2_RU_PNPI'           :{'AnalysisOps':  200*TB},
 'T2_RU_RRC_KI'         :{'AnalysisOps':  200*TB},
 'T2_RU_SINP'           :{'AnalysisOps':  200*TB},
 'T2_TH_CUNSTDA'        :{'AnalysisOps':   60*TB},
 'T2_TR_METU'	        :{'AnalysisOps':  210*TB},
 'T2_UA_KIPT'	        :{'AnalysisOps':  425*TB},
 'T2_UK_London_Brunel'	:{'AnalysisOps':  300*TB},
 'T2_UK_London_IC'	:{'AnalysisOps':  300*TB},
 'T2_UK_SGrid_Bristol'  :{'AnalysisOps':  120*TB},
 'T2_UK_SGrid_RALPP'	:{'AnalysisOps':  500*TB},
 'T2_US_Caltech'	:{'AnalysisOps': 1025*TB},
 'T2_US_Florida'	:{'AnalysisOps': 1025*TB},
 'T2_US_MIT'	        :{'AnalysisOps': 1025*TB},
 'T2_US_Nebraska'	:{'AnalysisOps': 1025*TB},
 'T2_US_Purdue'	        :{'AnalysisOps': 1325*TB},
 'T2_US_UCSD'	        :{'AnalysisOps': 1025*TB},
 'T2_US_Wisconsin'	:{'AnalysisOps': 1025*TB},
}

