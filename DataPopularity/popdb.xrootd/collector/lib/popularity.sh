#!/bin/bash
clear
declare -a QUERY=("MV_xrdmon_rates_x_H" "MV_xrdmon_procTime_x_H" "MV_XRD_stat0" "MV_XRD_stat0_pre" "V_XRD_LFC_aggr1" "MV_XRD_DS_stat0_aggr1" "MV_DS" "MV_XRD_DS_stat0_aggr2" "MV_DataTier" "MV_XRD_DS_stat0_aggr3" "MV_XRD_DS_stat0_aggr4" "MV_DSName" "MV_block_stat0_aggr_180_days" "MV_block_stat0_aggr_365_days" "MV_block_stat0_last_access" "MV_XRD_stat2" "V_XRD_stat2_aggr1")

nQUERY=${#QUERY[@]}

if [ $# -lt 4 ] 
then
    echo "Usage: $0 -s <query_num> -m <MM> [-d <(dd )+|(dd,)+>]"
    for (( i=1; i<${nQUERY}+1; i++ ));
    do
  	echo "       "$i") "${QUERY[$i-1]}
    done
    echo "Examples: $0 -s 3 -m 04             (script #3 on all days in April)"
    echo "          $0 -s 3 -m 04 -d 21 22    (script #3 on days 21 and 22 in April individually)"
    echo "          $0 -s 3 -m 04 -d 21,22,23 (script #3 on days 21,22,23 in April as a whole)" 
    exit -1
fi

while [[ $# > 0 ]]
do
key="$1"

case $key in
    -s|--script)
    SCRIPT="${QUERY[$2-1]}.pig"
    SCRIPTNUM="$2"
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

if [[ $DAYS == *","* ]]; then
   DAYS_LIST=$DAYS
   DAYS=999
fi

for DAY in $DAYS
do
   # Process a full month
   if [ $DAY -eq 0 ]; then
      INPUTDIR="/user/wdtmon/xrootd/cms/2015/$MONTH/*/aaa"
      OUTPUTDIR="/user/mmeoni/result/2015/$MONTH/aaa"
      SIZE="$(echo `hadoop fs -du -s /user/wdtmon/xrootd/cms/2015/$MONTH/*/aaa | cut -d' ' -f1-2` | sed 's/ /+/g' | bc)"
      SIZE=`echo "scale=2;$SIZE / 1024 / 1024 / 1024" | bc -l`
      SIZE=`echo $SIZE G`
   else 
   # Process a list of days as a whole
      if [ $DAY -eq 999 ]; then
         INPUTDIR="/user/wdtmon/xrootd/cms/2015/$MONTH/{$DAYS_LIST}/aaa"
         OUTPUTDIR="/user/mmeoni/result/2015/$MONTH/${DAYS_LIST//,/-}/aaa"
         SIZE="$(echo `hadoop fs -du -s /user/wdtmon/xrootd/cms/2015/$MONTH/{$DAYS_LIST}/aaa | cut -d' ' -f1-2` | sed 's/ /+/g' | bc)"
         SIZE=`echo "scale=2;$SIZE / 1024 / 1024 / 1024" | bc -l`
         SIZE=`echo $SIZE G`
      else
   # Process a list of days individually
         INPUTDIR="/user/wdtmon/xrootd/cms/2015/$MONTH/$DAY/aaa"
         OUTPUTDIR="/user/mmeoni/result/2015/$MONTH/$DAY/aaa"
         SIZE="$(echo `hadoop fs -du -h -s /user/wdtmon/xrootd/cms/2015/$MONTH/$DAY/aaa | cut -d' ' -f1-2`)"
      fi
   fi
   echo "Input size is "$SIZE
   START_TIME=$(date +"%s")

   hdfs dfs -rm -r $OUTPUTDIR

   echo "Executing pig -f $SCRIPT -param input=$INPUTDIR -param output=$OUTPUTDIR....."
   pig -f "$SCRIPT" -param input="$INPUTDIR" -param output="$OUTPUTDIR" 2>&1 | grep -v "is deprecated. Instead, use" | tee output.log

   # Pig return code is always 0!!?!!
   # if [ $? -eq 0 ]; then

   # extract number of parallel tasks
   PARALLEL="$(echo `cat output.log | grep "JobControlCompiler - Setting Parallelism to" | head -1 | rev | cut -d" " -f1 | rev`)"
   rm output.log

   # using this instead
   rc=`hdfs dfs -ls $OUTPUTDIR`
   if [ ! -z "$rc" ]; then
      ELAPSED_TIME=$(($(date +"%s") - $START_TIME))
      echo "`date +%Y"/"%m"/"%d" "%H":"%M":"%S`","$SCRIPTNUM","$SCRIPT","$INPUTDIR","$SIZE","$ELAPSED_TIME","$(($ELAPSED_TIME / 60))m:$(($ELAPSED_TIME % 60))s","$PARALLEL" >> pigjobs.log
   else
      echo "`date +%Y"/"%m"/"%d" "%H":"%M":"%S`","$SCRIPTNUM","$SCRIPT","$INPUTDIR","$SIZE","$ELAPSED_TIME","ERROR" >> pigjobs.log
   fi

   hdfs dfs -cat $OUTPUTDIR/part-r-00000 | head
done

exit 0
