#!/bin/bash
clear
declare -a QUERY=("MV_xrdmon_rates_x_H_aaa" "MV_xrdmon_procTime_x_H_aaa" "MV_XRD_stat0_aaa")
nQUERY=${#QUERY[@]}

if [ $# -lt 4 ] 
then
    echo "Usage: $0 <query_num> MM[/YYYYMMDD]"
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
      INPUTDIR="/user/wdtmon/xrootd/cms/aaa/2015/$MONTH/*"
      OUTPUTDIR="/user/mmeoni/result/aaa/2015/$MONTH"
      SIZE="$(echo `hadoop fs -du -h -s /user/wdtmon/xrootd/cms/aaa/2015/$MONTH | cut -d' ' -f1-2`)"
   else
      INPUTDIR="/user/wdtmon/xrootd/cms/aaa/2015/$MONTH/$DAY/*"
      OUTPUTDIR="/user/mmeoni/result/aaa/2015/$MONTH/$DAY"
      SIZE="$(echo `hadoop fs -du -h -s /user/wdtmon/xrootd/cms/aaa/2015/$MONTH/$DAY | cut -d' ' -f1-2`)"
   fi
   echo "Input size is "$SIZE
   START_TIME=$(date +"%s")

   hdfs dfs -rm -r $OUTPUTDIR

   echo "Executing pig -f $SCRIPT -param input=$INPUTDIR -param output=$OUTPUTDIR....."
   pig -f "$SCRIPT" -param input="$INPUTDIR" -param output="$OUTPUTDIR" 2>&1 | grep -v "is deprecated. Instead, use"

   # Pif return code always 0!!?!!
   # if [ $? -eq 0 ]; then

   #using this instead
   if [ $DAY -eq 0 ]; then
      rc=`hdfs dfs -ls /user/mmeoni/result/aaa/2015/$MONTH`
   else
      rc=`hdfs dfs -ls /user/mmeoni/result/aaa/2015/$MONTH/$DAY`
   fi
   if [ ! -z "$rc" ]; then
      ELAPSED_TIME=$(($(date +"%s") - $START_TIME))
      echo "`date +%Y"/"%m"/"%d" "%H":"%M":"%S`","$SCRIPT","$INPUTDIR","$SIZE","$(($ELAPSED_TIME / 60))m:$(($ELAPSED_TIME % 60))s" >> pigjobs.log
   else
      echo "`date +%Y"/"%m"/"%d" "%H":"%M":"%S`","$SCRIPT","$INPUTDIR","$SIZE","ERROR" >> pigjobs.log
   fi
done

exit 0
