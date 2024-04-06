from fastapi import APIRouter, Depends, status, Path, HTTPException
from typing import Annotated, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product
from .auth import get_current_user

router = APIRouter(
    tags=["Product"],
    prefix="/product"
)

class ProductData(BaseModel):
    name: str = Field(min_length=3,max_length=40, description="Name of the product. (3 to 40 characters)\n")
    description: str = Field(min_length=3,max_length=500, description="Description of the product. (3 to 500 characters)\n")
    price: int = Field(gt=0, description="Price of the product. (Greater than 0)\n")

class PaginationParams(BaseModel):
    limit:int = Field(10, description="Limit the number of products returned per page. Default is 10.\n")
    skip:int = Field(0, description="Skip the specified number of products.\n")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get("/",status_code=status.HTTP_200_OK)
def get_all_products(db: db_dependency, pagination: PaginationParams = Depends()):
    """
    Retrieve all products.\n
    Parameters:\n
    - pagination.limit (optional): Limit the number of products returned per page. Default is 10.\n
    - pagination.skip (optional): Skip the specified number of products.\n
    Returns:\n
    - Status code: 200 OK\n
    - Message: List of product objects.\n
    Raises:\n
    - HTTPException 401 (Unauthorized) if user is not authenticated.\n
    """
    return db.query(Product).offset(pagination.skip).limit(pagination.limit).all()

@router.get("/{product_id}",status_code=status.HTTP_200_OK)
def get_product_by_id(db:db_dependency, user:user_dependency ,product_id:int = Path(gt=0)):
    """
    Retrieve product by ID.\n
    Parameters:\n
    - product_id (required): The unique identifier of the product.\n
    Returns:\n
    - Status code: 200 OK\n
    - Message: Details of the product corresponding to the provided ID.\n
    Raises:\n
    - HTTPException 404 (Not Found) if the requested product does not exist.\n
    - HTTPException 401 (Unauthorized) if user is not authenticated.\n
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not Authenticated')
    product_data = db.query(Product).filter(Product.id==product_id).first()
    if product_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product Not Found")
    return product_data

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_product(db: db_dependency, user:user_dependency, product_data:ProductData):
    """
    Create a new product.\n
    Parameters:\n
    - product_data (required): The details of the product to create.\n
    Returns:\n
    - Status code: 201 Created\n
    - Message: Details of the newly created product.\n
    Raises:\n
    - HTTPException 401 (Unauthorized) if user is not authenticated.\n
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not Authenticated')
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()

@router.put("/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
def update_product(db:db_dependency, user:user_dependency, product_data:ProductData, product_id:int = Path(gt=0)):
    """
    Update product by ID.\n
    Parameters:\n
    - product_id (required): The unique identifier of the product to update.\n
    - product_data (required): The updated details of the product.\n
    Returns:\n
    - Status code: 204 No Content\n
    - Message: No content.\n
    Raises:\n
    - HTTPException 404 (Not Found) if the requested product does not exist.\n
    - HTTPException 401 (Unauthorized) if user is not authenticated.\n
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not Authenticated')
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Product Not Found')
    for attr, value in product_data.__dict__.items():
        setattr(product, attr, value)
    db.add(product)
    db.commit()

    db.refresh(product)
    return product

@router.delete("/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_product(db:db_dependency, user:user_dependency, product_id:int=Path(gt=0)):
    """
    Delete product by ID.\n
    Parameters:\n
    - product_id (required): The unique identifier of the product to delete.\n
    Returns:\n
    - Status code: 204 No Content\n
    - Message: No content.\n
    Raises:\n
    - HTTPException 404 (Not Found) if the requested product does not exist.\n
    - HTTPException 401 (Unauthorized) if user is not authenticated.\n
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not Authenticated')
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Product Not Found')
    
    db.query(Product).filter(Product.id==product_id).delete()
    db.commit()
