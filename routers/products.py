from fastapi import APIRouter, HTTPException, Depends,UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
import schemas, models
from schemas import ProductCreateForm
from routers.utils import upload_to_s3

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=schemas.ProductOut)
def create_product(form_data: schemas.ProductCreateForm = Depends(), db: Session = Depends(get_db),image: UploadFile = File()):
    payload = form_data.to_schema()
    category = db.query(models.Category).get(payload.category_id)
    if not category:
        raise HTTPException(status_code=400, detail="Category does not exist")
    

    print("---------------------------",image.filename)
    
    

    file_url=upload_to_s3(image)
    print("File uploaded to S3 at URL:", file_url)    

    product = models.Product(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        category_id=payload.category_id,
        total_units=payload.total_units,
        product_image=file_url,
        remaining_units=payload.remaining_units if payload.remaining_units is not None else payload.total_units,
        quantity=payload.quantity
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": schemas.CategoryOut(
            id=category.id, name=category.name, description=category.description
        ),
        "quantity": product.quantity,
        "stock_status": "Out of Stock" if product.remaining_units == 0 else "Available"
    }


@router.get("/", response_model=list[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    result = []
    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "category": schemas.CategoryOut(
                id=p.category.id,
                name=p.category.name,
                description=p.category.description
            ),
            "quantity": p.quantity,
            "stock_status": "Out of Stock" if p.remaining_units == 0 else "Available"
        })
    return result