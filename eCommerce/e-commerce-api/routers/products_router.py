from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
from database import get_db
from schemas import ProductResponse, ProductCreate, ProductUpdate
from services import ProductService
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/products", tags=["Products"])

# Define the images directory path
IMAGES_DIR = Path(__file__).parent.parent / "images"


@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of products with optional filtering"""
    logger.info(f"Products list request - skip: {skip}, limit: {limit}, category: {category}, search: {search}")
    try:
        product_service = ProductService(db)
        products = product_service.get_products(
            skip=skip,
            limit=limit,
            category=category,
            search=search
        )
        logger.info(f"Returning {len(products)} products")
        return products
    except Exception as e:
        logger.error(f"Error fetching products list: {str(e)}", exc_info=True)
        raise


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    logger.info(f"Product detail request for ID: {product_id}")
    try:
        product_service = ProductService(db)
        product = product_service.get_product_by_id(product_id)

        if not product:
            logger.warning(f"Product not found: ID {product_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        logger.info(f"Product found: {product.name} (ID: {product_id})")
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product ID {product_id}: {str(e)}", exc_info=True)
        raise


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    """Create a new product (admin only in production)"""
    logger.info(f"Create product request: {product_data.name}")
    try:
        product_service = ProductService(db)
        product = product_service.create_product(product_data)
        logger.info(f"Product created successfully: {product.name} (ID: {product.id})")
        return product
    except Exception as e:
        logger.error(f"Error creating product {product_data.name}: {str(e)}", exc_info=True)
        raise


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update a product (admin only in production)"""
    logger.info(f"Update product request for ID: {product_id}")
    try:
        product_service = ProductService(db)
        product = product_service.update_product(product_id, product_data)

        if not product:
            logger.warning(f"Cannot update - product not found: ID {product_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        logger.info(f"Product updated successfully: {product.name} (ID: {product_id})")
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating product ID {product_id}: {str(e)}", exc_info=True)
        raise


@router.get("/images/{image_filename}")
def get_product_image(image_filename: str):
    """Serve product images as binary data"""
    logger.info(f"Image request for: {image_filename}")

    # Construct the full image path
    image_path = IMAGES_DIR / image_filename

    # Check if the file exists
    if not image_path.exists() or not image_path.is_file():
        logger.warning(f"Image not found: {image_filename}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image not found: {image_filename}"
        )

    # Security check: ensure the resolved path is still within IMAGES_DIR
    try:
        image_path.resolve().relative_to(IMAGES_DIR.resolve())
    except ValueError:
        logger.error(f"Path traversal attempt detected: {image_filename}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    logger.info(f"Serving image: {image_filename}")
    return FileResponse(
        path=image_path,
        media_type="image/jpeg",
        headers={"Cache-Control": "public, max-age=86400"}  # Cache for 24 hours
    )
