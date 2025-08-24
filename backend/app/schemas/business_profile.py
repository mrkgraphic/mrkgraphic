from pydantic import BaseModel, EmailStr, HttpUrl, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class BusinessTypeEnum(str, Enum):
    LLC = "LLC"
    CORPORATION = "Corporation"
    PARTNERSHIP = "Partnership"
    SOLE_PROPRIETORSHIP = "Sole Proprietorship"
    NON_PROFIT = "Non-Profit"


class BusinessModelEnum(str, Enum):
    B2B = "B2B"
    B2C = "B2C"
    B2B2C = "B2B2C"
    MARKETPLACE = "Marketplace"
    SUBSCRIPTION = "Subscription"
    FREEMIUM = "Freemium"


# Base schemas
class BusinessProfileBase(BaseModel):
    business_name: str
    business_description: Optional[str] = None
    industry: Optional[str] = None
    business_type: Optional[BusinessTypeEnum] = None
    founded_year: Optional[int] = None
    employee_count: Optional[int] = None
    annual_revenue: Optional[float] = None
    
    # Contact Information
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[HttpUrl] = None
    
    # Address Information
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = "United States"
    
    # Social Media
    linkedin_url: Optional[HttpUrl] = None
    twitter_url: Optional[HttpUrl] = None
    facebook_url: Optional[HttpUrl] = None
    instagram_url: Optional[HttpUrl] = None
    
    # Business Details
    services_offered: Optional[List[str]] = []
    target_market: Optional[str] = None
    unique_selling_proposition: Optional[str] = None
    business_model: Optional[BusinessModelEnum] = None
    
    # SEO and Marketing
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    keywords: Optional[List[str]] = []
    
    @validator('founded_year')
    def validate_founded_year(cls, v):
        if v is not None and (v < 1800 or v > datetime.now().year):
            raise ValueError('Founded year must be between 1800 and current year')
        return v

    @validator('employee_count')
    def validate_employee_count(cls, v):
        if v is not None and v < 0:
            raise ValueError('Employee count must be non-negative')
        return v


class BusinessProfileCreate(BusinessProfileBase):
    pass


class BusinessProfileUpdate(BaseModel):
    business_name: Optional[str] = None
    business_description: Optional[str] = None
    industry: Optional[str] = None
    business_type: Optional[BusinessTypeEnum] = None
    founded_year: Optional[int] = None
    employee_count: Optional[int] = None
    annual_revenue: Optional[float] = None
    
    # Contact Information
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[HttpUrl] = None
    
    # Address Information
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    
    # Social Media
    linkedin_url: Optional[HttpUrl] = None
    twitter_url: Optional[HttpUrl] = None
    facebook_url: Optional[HttpUrl] = None
    instagram_url: Optional[HttpUrl] = None
    
    # Business Details
    services_offered: Optional[List[str]] = None
    target_market: Optional[str] = None
    unique_selling_proposition: Optional[str] = None
    business_model: Optional[BusinessModelEnum] = None
    
    # SEO and Marketing
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    keywords: Optional[List[str]] = None
    
    # Status
    is_published: Optional[bool] = None


class BusinessProfile(BusinessProfileBase):
    id: int
    owner_id: int
    profile_slug: Optional[str] = None
    is_published: bool = False
    is_featured: bool = False
    logo_url: Optional[str] = None
    banner_image_url: Optional[str] = None
    additional_images: Optional[List[str]] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class BusinessProfilePublic(BaseModel):
    id: int
    business_name: str
    business_description: Optional[str] = None
    industry: Optional[str] = None
    business_type: Optional[str] = None
    founded_year: Optional[int] = None
    employee_count: Optional[int] = None
    
    # Contact Information
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    
    # Address Information
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    
    # Social Media
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    
    # Business Details
    services_offered: Optional[List[str]] = []
    target_market: Optional[str] = None
    unique_selling_proposition: Optional[str] = None
    business_model: Optional[str] = None
    
    # Media
    logo_url: Optional[str] = None
    banner_image_url: Optional[str] = None
    
    profile_slug: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


# Review schemas
class BusinessReviewBase(BaseModel):
    reviewer_name: str
    reviewer_email: Optional[EmailStr] = None
    rating: int
    review_text: Optional[str] = None

    @validator('rating')
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v


class BusinessReviewCreate(BusinessReviewBase):
    pass


class BusinessReview(BusinessReviewBase):
    id: int
    business_id: int
    is_verified: bool = False
    is_published: bool = True
    created_at: datetime

    class Config:
        orm_mode = True


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        orm_mode = True