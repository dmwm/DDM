#!/bin/bash
clear
declare -a QUERY=("MV_xrdmon_rates_x_H" "MV_XRD_stat0" "MV_xrdmon_procTime_x_H")
nQUERY=${#QUERY[@]}

if [ $# -lt 1 ]
then
    echo "Usage: $0 <query_num>"
    for (( i=1; i<${nQUERY}+1; i++ ));
    do
        echo "       "$i") "${QUERY[$i-1]}
    done
    exit -1
fi

for PERIOD in 01 02 03 04 05
do
   INPUTDIR="/project/awg/eos/processed/cms/2015/$PERIOD/*"
   OUTPUTDIR="/user/mmeoni/result/$PERIOD"
   SCRIPT="${QUERY[$1-1]}.pig"
   SIZE="$(echo `hadoop fs -du -h -s /project/awg/eos/processed/cms/2015/$PERIOD | cut -d' ' -f1-2`)"
   echo "Input size is "$SIZE
   START_TIME=$(date +"%s")

   hdfs dfs -rm -r $OUTPUTDIR

   echo "Executing pig -f $SCRIPT -param input=$INPUTDIR -param output=$OUTPUTDIR....."
   pig -f "$SCRIPT" -param input="$INPUTDIR" -param output="$OUTPUTDIR" 2>&1 | grep -v "is deprecated. Instead, use"

   if [ $? -eq 0 ]; then
      ELAPSED_TIME=$(($(date +"%s") - $START_TIME))
      echo "`date +%Y"/"%m"/"%d" "%H":"%M":"%S`","$SCRIPT","$INPUTDIR","$SIZE","$(($ELAPSED_TIME / 60))m:$(($ELAPSED_TIME % 60))s" >> pigjobs.log
   else
      echo "`date +%Y"/"%m"/"%d" "%H":"%M":"%S`","$SCRIPT","$INPUTDIR","$SIZE","ERROR" >> pigjobs.log
   fi
done

exit 0
