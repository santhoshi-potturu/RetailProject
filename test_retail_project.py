import pytest
from lib.ConfigReader import get_app_config
from lib.DataReader import read_customers
from lib.DataReader import read_orders
from lib.DataManipulation import count_orders_state, filter_closed_orders, filter_orders_generic

@pytest.mark.skip()
def test_read_customers_df(spark):
    customers_count = read_customers(spark, "LOCAL").count()
    assert customers_count == 12435

@pytest.mark.skip()
def test_read_orders_df(spark):
    orders_count = read_orders(spark, "LOCAL").count()
    assert orders_count == 68884

@pytest.mark.transformation()
def test_filter_closed_orders_df(spark):
    orders_df = read_orders(spark, "LOCAL")
    closed_orders_count = filter_closed_orders(orders_df).count()
    assert closed_orders_count == 7556

@pytest.mark.skip("work in progress")
def test_read_config():
    config = get_app_config("LOCAL")
    assert config["orders.file.path"] == "data/orders.csv"

@pytest.mark.transformation()
def test_count_orders_state(spark, expected_result):
    cust_df = read_customers(spark, "LOCAL")
    actual_result = count_orders_state(cust_df)

    # Ensure consistent order before comparing
    actual_result = actual_result.orderBy("state")
    expected_result = expected_result.orderBy("state")
    # collecting both datasets
    assert actual_result.collect() == expected_result.collect()

@pytest.mark.parametrize(
        "status, count",
        [("CLOSED", 7556),
         ("PENDING_PAYMENT", 15030),
         ("COMPLETE", 22899)]
)

@pytest.mark.latest()
def test_filter_orders_generic(spark, status, count):
    orders_df = read_orders(spark,"LOCAL")
    filtered_count = filter_orders_generic(orders_df,status).count()
    assert filtered_count == count