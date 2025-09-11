import requests
import random
import os
import sqlite3
from config.config import BASE_URL

DB = os.path.join(os.path.dirname(__file__), "automation.db")
with sqlite3.connect(DB) as con:
    con.execute("DELETE FROM products")
    con.execute("DELETE FROM sqlite_sequence WHERE name='products';")
    con.commit()


# cars
makes = ["Toyota", "BMW", "Ford", "Infinity", "Tesla", "Audi", "Mercedes", "Kia"]
car_type = ["Sedan", "SUV", "Coupe", "Truck", "Crossover", "Hatchback", "Van"]


def generate_price(year):
    if year <= 2010:
        return round(random.uniform(3000, 10000))
    elif 2010 < year <= 2020:
        return round(random.uniform(11000, 35000))
    else:
        return round(random.uniform(30000, 80000))


for _ in range(200):  # 200 cars
    year = random.randint(2000, 2025)
    product = {
        "car_type": random.choice(car_type),
        "make": random.choice(makes),
        "year": year,
        "price": generate_price(year),
        "discount": random.randint(3, 30),
        "stock": random.randint(0, 20),
    }
    res = requests.post(f"{BASE_URL}/products", json=product)
products = requests.get(f"{BASE_URL}/products")
print(f"Number of cars: {len(products.json())}")


