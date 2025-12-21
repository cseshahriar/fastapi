# response status code
from ast import alias
from typing import Annotated
from fastapi import FastAPI, Query, status, HTTPException
from pydantic import AfterValidator


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


# Multi search terms(List)
@app.get("/products")
async def get_multi_search_products(
    search: Annotated[list[str] | None, Query()] = None
):
    if search:
        filter_products = []
        for product in products:
            for s in search:
                if s.lower() in product["title"].lower():
                    filter_products.append(product)
        return filter_products
    return products


# Adding metadata
@app.get("/product-items", status_code=status.HTTP_200_OK)
async def get_product_items(
    search: Annotated[
        str | None,
        Query(
            # alias="q",
            # title="Search Product",
            # description="Search by product title",
            # min_length=3,
            # max_length=20,
            # example="backpack",
            deprecated=True
        )
    ] = None
):
    if search:
        search_lower = search.lower()
        filter_products = []
        for product in products:
            if search_lower in product["title"].lower():
                filter_products.append(product)
        if not filter_products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No products found matching the search criteria."
            )
        return filter_products
    return products


# Custom validation
def check_valid_search(id: str):
    if not id.startswith("prod-"):
        raise ValueError("Id must with 'prod-'.")
    return id


@app.get("/products-list")
async def product_item_list(
    id: Annotated[str | None, AfterValidator(check_valid_search)] = None
):
    if id:
        return {"id": id, 'message': "Valid id"}
    return {"message": "No id provided"}
