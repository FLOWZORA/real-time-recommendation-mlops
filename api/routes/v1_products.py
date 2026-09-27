from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import func

from api.database import get_db
from api.models.product import Product, Category
from api.schemas.product import ProductCreate, ProductUpdate, ProductResponse, CategoryResponse
from api.security.permissions import get_auth_context, require_role, AuthContext
from features.catalog_data import get_product_image

router = APIRouter(prefix="/v1/products", tags=["Products"])

@router.get("", response_model=List[ProductResponse])
def list_products(
    response: Response,
    category_id: Optional[str] = None,
    category_name: Optional[str] = None,
    search: Optional[str] = None,
    in_stock: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    ctx: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
):
    query = db.query(Product)
    if ctx.organization_id:
        query = query.filter(Product.organization_id == ctx.organization_id)

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if category_name:
        query = query.join(Category).filter(Category.name.ilike(f"%{category_name}%"))

    if search:
        query = query.filter(Product.title.ilike(f"%{search}%"))

    if in_stock is not None:
        query = query.filter(Product.in_stock == in_stock)

    total_count = query.count()
    response.headers["X-Total-Count"] = str(total_count)

    products = query.order_by(Product.item_id_numeric.asc()).offset(skip).limit(limit).all()
    return products

@router.get("/categories", response_model=List[CategoryResponse])
def list_categories(
    ctx: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
):
    query = db.query(Category)
    if ctx.organization_id:
        query = query.filter(Category.organization_id == ctx.organization_id)
    return query.all()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: str,
    ctx: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
):
    # Support lookup either by UUID or by item_id_numeric
    query = db.query(Product)
    if ctx.organization_id:
        query = query.filter(Product.organization_id == ctx.organization_id)

    if product_id.isdigit():
        prod = query.filter(Product.item_id_numeric == int(product_id)).first()
    else:
        prod = query.filter(Product.id == product_id).first()

    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    req: ProductCreate,
    ctx: AuthContext = Depends(require_role(["STORE_ADMIN"])),
    db: Session = Depends(get_db),
):
    # Find next available item_id_numeric if not provided
    if req.item_id_numeric is None:
        max_id = db.query(func.max(Product.item_id_numeric)).filter(
            Product.organization_id == ctx.organization_id
        ).scalar()
        item_num = (max_id + 1) if max_id is not None else 0
    else:
        item_num = req.item_id_numeric

    product = Product(
        organization_id=ctx.organization_id,
        item_id_numeric=item_num,
        category_id=req.category_id,
        title=req.title,
        description=req.description,
        price=req.price,
        rating=req.rating or 5.0,
        badge=req.badge,
        image_url=req.image_url or get_product_image(item_num, req.title, ""),
        in_stock=req.in_stock if req.in_stock is not None else True,
        popularity_score=0,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    req: ProductUpdate,
    ctx: AuthContext = Depends(require_role(["STORE_ADMIN"])),
    db: Session = Depends(get_db),
):
    query = db.query(Product).filter(Product.organization_id == ctx.organization_id)
    if product_id.isdigit():
        prod = query.filter(Product.item_id_numeric == int(product_id)).first()
    else:
        prod = query.filter(Product.id == product_id).first()

    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = req.dict(exclude_unset=True)
    for k, v in update_data.items():
        setattr(prod, k, v)

    db.commit()
    db.refresh(prod)
    return prod

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: str,
    ctx: AuthContext = Depends(require_role(["STORE_ADMIN"])),
    db: Session = Depends(get_db),
):
    query = db.query(Product).filter(Product.organization_id == ctx.organization_id)
    if product_id.isdigit():
        prod = query.filter(Product.item_id_numeric == int(product_id)).first()
    else:
        prod = query.filter(Product.id == product_id).first()

    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(prod)
    db.commit()
    return None
