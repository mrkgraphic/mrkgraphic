from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    business_profiles = relationship("BusinessProfile", back_populates="owner")


class BusinessProfile(Base):
    __tablename__ = "business_profiles"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Basic Information
    business_name = Column(String, nullable=False, index=True)
    business_description = Column(Text)
    industry = Column(String)
    business_type = Column(String)  # LLC, Corporation, Partnership, etc.
    founded_year = Column(Integer)
    employee_count = Column(Integer)
    annual_revenue = Column(Float)
    
    # Contact Information
    email = Column(String)
    phone = Column(String)
    website = Column(String)
    
    # Address Information
    street_address = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    country = Column(String, default="United States")
    
    # Social Media
    linkedin_url = Column(String)
    twitter_url = Column(String)
    facebook_url = Column(String)
    instagram_url = Column(String)
    
    # Business Details
    services_offered = Column(JSON)  # Array of services
    target_market = Column(Text)
    unique_selling_proposition = Column(Text)
    business_model = Column(String)
    
    # Media
    logo_url = Column(String)
    banner_image_url = Column(String)
    additional_images = Column(JSON)  # Array of image URLs
    
    # SEO and Marketing
    meta_title = Column(String)
    meta_description = Column(Text)
    keywords = Column(JSON)  # Array of keywords
    
    # Status and Visibility
    is_published = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    profile_slug = Column(String, unique=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="business_profiles")
    reviews = relationship("BusinessReview", back_populates="business")


class BusinessReview(Base):
    __tablename__ = "business_reviews"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business_profiles.id"), nullable=False)
    reviewer_name = Column(String, nullable=False)
    reviewer_email = Column(String)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    review_text = Column(Text)
    is_verified = Column(Boolean, default=False)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    business = relationship("BusinessProfile", back_populates="reviews")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_name = Column(String, nullable=False)  # Basic, Pro, Enterprise
    stripe_subscription_id = Column(String, unique=True)
    status = Column(String, nullable=False)  # active, canceled, past_due, etc.
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User")