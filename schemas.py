"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime

# Example schemas (kept for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Reverb Music Academy schemas

LessonInstrument = Literal["Guitar", "Kanto", "Piano", "Drums"]

class Booking(BaseModel):
    """
    Lesson bookings for Reverb Music Academy
    Collection name: "booking"
    """
    name: str = Field(..., min_length=2, max_length=100, description="Student full name")
    email: EmailStr = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, max_length=30, description="Contact phone number")
    instrument: LessonInstrument = Field(..., description="Instrument/discipline for the lesson")
    preferred_date: str = Field(..., description="Preferred date (YYYY-MM-DD)")
    preferred_time: str = Field(..., description="Preferred time (HH:MM)")
    message: Optional[str] = Field(None, max_length=1000, description="Additional notes or goals")
    teacher: Optional[str] = Field(None, max_length=100, description="Preferred teacher if any")
    source: Optional[str] = Field("website", description="Where the booking came from")
    status: Literal["pending", "confirmed", "cancelled"] = Field("pending", description="Booking status")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
