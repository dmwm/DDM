#!/bin/bash
clear
declare -a QUERY=("MV_xrdmon_rates_x_H" "MV_xrdmon_procTime_x_H" "MV_XRD_stat0" "MV_XRD_stat0_pre" "V_XRD_LFC_aggr1" "MV_XRD_DS_stat0_aggr1" "MV_DS" "MV_XRD_DS_stat0_aggr2" "MV_DataTier" "MV_XRD_DS_stat0_aggr3" "MV_XRD_DS_stat0_aggr4" "MV_DSName" "MV_block_stat0_aggr_180_days" "MV_block_stat0_aggr_365_days" "MV_block_stat0_last_access" "MV_XRD_stat2" "V_XRD_stat2_aggr1")

nQUERY=${#QUERY[@]}

if [ $# -lt 4 ] 
then
    echo "Usage: $0 -s <query_num> -m MM -d []"
    for (( i=1; i<${nQUERY}+1; i++ ));
    do
  	echo "       "$i") "${QUERY[$i-1]}
    done
    exit -1
fi

while [[ $# > 0 ]]
do
key="$1"

case $key in
    -s|--script)
    SCRIPT="${QUERY[$2-1]}.pig"
    shift
    ;;
    -m|--month)
    MONTH="$2"
    shift
    ;;
    -d|--day)
    shift
    DAYS="$@"
    break
    ;;
    *)
    echo "Error: undefined argument"
    exit 0
    ;;
esac
shift
done

if [ -z "$DAYS" ]; then
   DAYS=0
fi

for DAY in $DAYS
do
   if [ $DAY -eq 0 ]; then
      INPUTDIR="/user/wdtmon/xrootd/cms/2015/$MONTH/*/aaa"
      OUTPUTDIR="/user/mmeoni/result/2015/$MONTH/aaa"
      SIZE="$(echo `hadoop fs -du -h -s /user/wdtmon/xrootd/cms/2015/$MONTH/*/aaa | cut -d' ' -f1-2`)"
   else
      INPUTDIR="/user/wdtmon/xrootd/cms/2015/$MONTH/$DAY/aaa"
      OUTPUTDIR="/user/mmeoni/result/2015/$MONTH/$DAY/aaa"
      SIZE="$(echo `hadoop fs -du -h -s /user/wdtmon/xrootd/cms/2015/$MONTH/$DAY/aaa | cut -d' ' -f1-2`)"
   fi
   echo "Input size is "$SIZE
   START_TIME=$(date +"%s")

   hdfs dfs -rm -r $OUTPUTDIR

   echo "Executing pig -f $SCRIPT -param input=$INPUTDIR -param output=$OUTPUTDIR....."
   pig -f "$SCRIPT" -param input="$INPUTDIR" -param output="$OUTPUTDIR" 2>&1 | grep -v "is deprecated. Instead, use" | tee output.log

   # Pig return code is always 0!!?!!
   # if [ $? -eq 0 ]; then

   # extract number of parallel tasks
   PARALLEL="$(echo `cat output.log | grep "JobControlCompiler - Setting Parallelism to" | head -1 | rev | cut -c 1`)"
   rm output.log

   # using this instead
   rc=`hdfs dfs -ls $OUTPUTDIR`
   if [ ! -z "$rc" ]; then
      ELAPSED_TIME=$(($(date +"%s") - $START_TIME))
      echo "`date +%Y"/"%m"/"%d" "%H":"%M":"%S`","$SCRIPT","$INPUTDIR","$SIZE","$(($ELAPSED_TIME / 60))m:$(($ELAPSED_TIME % 60))s","$PARALLEL" >> pigjobs.log
   else
      echo "`date +%Y"/"%m"/"%d" "%H":"%M":"%S`","$SCRIPT","$INPUTDIR","$SIZE","ERROR" >> pigjobs.log
   fi

   hdfs dfs -cat $OUTPUTDIR/part-r-00000 | head
done

exit 0
