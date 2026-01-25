"""Script to create demo data for the AI Agents application."""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, init_db
from app.tables import Project, CodeFile

def create_demo_data():
    """Create sample project and code files for demo."""
    init_db()
    db = SessionLocal()

    try:
        # Create demo project
        project = Project(
            name="E-Commerce API",
            description="A sample e-commerce API with product management and discount calculation",
            repository_url="https://bitbucket.org/demo/ecommerce-api"
        )
        db.add(project)
        db.commit()
        db.refresh(project)

        print(f"Created project: {project.name} (ID: {project.id})")

        # Create sample code files
        code_files = [
            {
                "file_path": "services/discount.py",
                "language": "python",
                "content": """def calculate_discount(price, discount_percentage):
    if discount_percentage > 100:
        discount_percentage = 100

    discount = price * discount_percentage / 100
    final_price = price - discount

    if final_price < 0:
        return 0

    return final_price


def apply_coupon(price, coupon_code):
    coupons = {
        "SAVE10": 10,
        "SAVE20": 20,
        "WELCOME": 15
    }
    
    discount = coupons.get(coupon_code, 0)
    return calculate_discount(price, discount)
"""
            },
            {
                "file_path": "api/products.py",
                "language": "python",
                "content": """from fastapi import APIRouter, HTTPException
from typing import List
from models import Product

router = APIRouter(prefix="/api/products", tags=["products"])

products_db = [
    {"id": 1, "name": "Laptop", "price": 999.99, "stock": 10},
    {"id": 2, "name": "Mouse", "price": 29.99, "stock": 50},
    {"id": 3, "name": "Keyboard", "price": 79.99, "stock": 30}
]

@router.get("/", response_model=List[Product])
def get_products():
    return products_db

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=Product)
def create_product(product: Product):
    new_id = max(p["id"] for p in products_db) + 1
    product_dict = product.dict()
    product_dict["id"] = new_id
    products_db.append(product_dict)
    return product_dict
"""
            },
            {
                "file_path": "models/product.py",
                "language": "python",
                "content": """from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    stock: int

    class Config:
        schema_extra = {
            "example": {
                "name": "Laptop",
                "price": 999.99,
                "stock": 10
            }
        }
"""
            },
            {
                "file_path": "utils/validators.py",
                "language": "python",
                "content": """def validate_email(email):
    if "@" not in email:
        return False
    return True

def validate_phone(phone):
    if len(phone) < 10:
        return False
    return True

def validate_price(price):
    return price > 0
"""
            }
        ]

        for file_data in code_files:
            code_file = CodeFile(
                project_id=project.id,
                file_path=file_data["file_path"],
                content=file_data["content"],
                language=file_data["language"]
            )
            db.add(code_file)
            print(f"Created file: {file_data['file_path']}")

        db.commit()
        print("\nDemo data created successfully!")
        print(f"\nYou can now:")
        print(f"1. Start the backend: cd backend && uvicorn app.main:app --reload")
        print(f"2. Start the frontend: cd frontend && npm install && npm run dev")
        print(f"3. Visit http://localhost:5173 and use project ID {project.id}")

    except Exception as e:
        print(f"Error creating demo data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_demo_data()
