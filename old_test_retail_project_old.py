import pytest
from lib.ConfigReader import get_app_config
from lib.DataReader import read_customers

from lib.DataReader import read_orders
from lib.DataManipulation import filter_closed_orders



def test_read_customers_df(spark):
    customers_count = read_customers(spark, "LOCAL").count()
    assert customers_count == 12435


def test_read_orders_df(spark):
    orders_count = read_orders(spark, "LOCAL").count()
    assert orders_count == 68884


def test_filter_closed_orders_df(spark):
    orders_df = read_orders(spark, "LOCAL")
    closed_orders_count = filter_closed_orders(orders_df).count()
    assert closed_orders_count == 7556

def test_read_config():
    config = get_app_config("LOCAL")
    assert config["orders.file.path"] == "data/orders.csv"