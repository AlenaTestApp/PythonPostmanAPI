import random
import pytest
import requests
from config.config import *


def test_check_products_status_code():
    res = requests.get(f"{BASE_URL}/products")
    assert res.status_code == 200


def test_json_format():
    res = requests.get(f"{BASE_URL}/products")
    products = res.json()
    for product in products:
        assert "id" in product
        assert "car_type" in product
        assert "make" in product
        assert "year" in product
        assert "discount" in product
        assert "stock" in product


def test_get_product_by_id():
    prod_id = 100
    res = requests.get(f"{BASE_URL}/products/{prod_id}")
    assert res.status_code == 200
    product_id = res.json()["id"]
    assert prod_id == product_id


def test_get_product_by_wrong_id():
    prod_id = 1000
    res = requests.get(f"{BASE_URL}/products/{prod_id}")
    assert res.status_code == 404


def test_get_product_number():
    res = requests.get(f"{BASE_URL}/products")
    assert len(res.json()) == 200


@pytest.fixture()
def product_details():
    prod_id = random.randint(1, 200)
    res = requests.get(f"{BASE_URL}/products/{prod_id}")
    prod_details = res.json()
    prod_dict = {
        "id": prod_details["id"],
        "car_type": prod_details["car_type"],
        "make": prod_details["make"],
        "year": prod_details["year"],
        "discount": prod_details["discount"],
        "stock": prod_details["stock"]
    }

    return prod_dict


def test_product_details(product_details):
    prod_details = product_details
    prod_id = prod_details["id"]
    res = requests.get(f"{BASE_URL}/products/{prod_id}")
    assert res.status_code == 200
    assert res.json()["car_type"] == prod_details["car_type"]
    assert res.json()["make"] == prod_details["make"]
    assert res.json()["year"] == prod_details["year"]
    assert res.json()["discount"] == prod_details["discount"]
    assert res.json()["stock"] == prod_details["stock"]

