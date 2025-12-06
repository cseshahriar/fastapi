# response status code
from fastapi import FastAPI, status, HTTPException
from enum import Enum

app = FastAPI()

# 100 to 199 for information and no body
# 200 - 299 for successful or every thing ok
# 201 created, create new record
# 204 for delete , no content
# 300 - 399 Redirection
# 304 not modify
# 400 - 499 "client error"
# 404 not found
# 400 generic errors from the client
# 500 - 599 server error

data = [
    {'id': 1, 'name': 'iphone17', 'price': 100},
    {'id': 2, 'name': 'iphone18', 'price': 100},
]


# GEt Request
# Read or Fetch ALL DAta
@app.get('/', status_code=status.HTTP_200_OK)
def home():
    ''' home '''
    return {"message": "Hello World"}


@app.get('/product', status_code=status.HTTP_200_OK)
async def all_products():
    ''' home '''
    return {"response": data}


# Read or fetch single product
@app.get("/product/{product_id}", status_code=status.HTTP_200_OK)
async def single_product(product_id: int):
    ''' get single product '''
    product = next((item for item in data if item["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"response": product}


# POST Request
# Create or Insert Data
@app.post("/product", status_code=status.HTTP_201_CREATED)
async def create_product(new_product: dict):
    ''' create product '''
    data.append(new_product)
    return {"response": new_product}


# PUT Request
# Update Complete Data
@app.post("/product/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(
    product_id: int, updated_product: dict
):
    ''' create product '''
    index = next(
        (i for i, item in enumerate(data) if item["id"] == product_id), None)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    # replace the whole object
    data[index] = updated_product
    return {"response": updated_product}


# Partial update
@app.patch("/product/{product_id}", status_code=status.HTTP_200_O)
async def patch_product(product_id: int, partial_data: dict):
    """Partial update for product"""
    product = next((item for item in data if item["id"] == product_id), None)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # update only given keys
    for key, value in partial_data.items():
        product[key] = value

    return {"response": product}


# Delete resource
@app.delete("/product/{product_id}")
async def delete_product(
    product_id: int, status_code=status.HTTP_204_NO_CONTENT
):
    """
    Docstring for delete_product

    :param product_id: Description
    :type product_id: int
    :param status_code: Description
    """
    index = next(
        (i for i, item in enumerate(data) if item["id"] == product_id), None)

    if index is None:
        raise HTTPException(status_code=404, detail="Product not found")

    deleted = data.pop(index)

    return {"message": "Product deleted", "deleted": deleted}
