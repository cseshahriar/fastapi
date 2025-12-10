# response status code
from typing import Annotated
from fastapi import FastAPI, Query, status, HTTPException

app = FastAPI()

products = [
    {
        "id": 1,
        "title": "Ravan Backpack",
        "price": 109.95,
        "description": "Perfect for everyday use and forest walks."
    },
    {
        "id": 2,
        "title": "Slim Fit T-Shirts",
        "price": 22.3,
        "description": "Comfortable, slim-fitting casual shirts."
    },
    {
        "id": 3,
        "title": "Cotton Jacket",
        "price": 55.99,
        "description": "Great for outdoor activities and gifting."
    }
]


# Basic query parameter
@app.get("/products")
async def get_products(search: str | None = None):  # optional str or none
    if search:
        search_lower = search.lower()
        filter_products = []
        for product in products:
            if search_lower in product["title"].lower():
                filter_products.append(product)
        return filter_products
    return products


# Validation with annotated
@app.get("/product-list")
async def get_product_list(
    search:
        Annotated[str | None, Query(max_length=5, pattern="^[a-z]+$")] = None
):
    if search:
        search_lower = search.lower()
        filter_products = []
        for product in products:
            if search_lower in product["title"].lower():
                filter_products.append(product)
        return filter_products
    return products
