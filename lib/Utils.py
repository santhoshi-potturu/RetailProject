
from pyspark.sql import SparkSession
from lib.ConfigReader import get_pyspark_config

def get_spark_session(env):
    conf = get_pyspark_config(env)

    if env == "LOCAL":
        # 👇 These two lines fix the “no response / hanging” issue on Windows
        conf.set("spark.driver.bindAddress", "127.0.0.1")
        conf.set("spark.ui.showConsoleProgress", "false")

        return (
            SparkSession.builder
            .config(conf=conf)
            .config('spark.driver.extraJavaOptions', '-Dlog4j.configuration=file:log4j.properties')
            .master("local[2]")
            .getOrCreate()
        )
    else:
        return (
            SparkSession.builder
            .config(conf=conf)
            .enableHiveSupport()
            .getOrCreate()
        )