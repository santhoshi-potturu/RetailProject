import pytest
from lib.Utils_old import get_spark_session

@pytest.fixture
def spark():
    spark_session = get_spark_session("LOCAL")
    yield spark_session
    spark_session.stop()

@pytest.fixture
def expected_result(spark):
    "returns expected data set"
    cust_schema = "state string, count int"
    return spark.read.format("csv").schema(cust_schema).option("header", True).load("data/test_result/cust_aggregate_state.csv")
