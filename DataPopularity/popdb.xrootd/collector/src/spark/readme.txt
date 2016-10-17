# cd target
# spark-submit  --driver-class-path '/usr/lib/hive/lib/*' --driver-java-options '-Dspark.executor.extraClassPath=/usr/lib/hive/lib/*' --master yarn-client --class ch.cern.awg.DatasetPopularity popularity-0.3.0-SNAPSHOT-jar-with-dependencies.jar /user/wdtmon/xrootd/cms/2015/*/*/eos spark-DS/2015 DatasetPopularity 0 > output-popularity-20160508-002 2>&1 &
