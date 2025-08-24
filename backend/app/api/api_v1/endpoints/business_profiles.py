from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
import slugify

from app.db.database import get_db
from app.models.business_profile import BusinessProfile, User, BusinessReview
from app.schemas.business_profile import (
    BusinessProfileCreate,
    BusinessProfileUpdate,
    BusinessProfile as BusinessProfileSchema,
    BusinessProfilePublic,
    BusinessReviewCreate,
    BusinessReview as BusinessReviewSchema,
)
from app.core.auth import get_current_user
from app.utils.file_upload import upload_file

router = APIRouter()


@router.post("/", response_model=BusinessProfileSchema)
async def create_business_profile(
    profile_data: BusinessProfileCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new business profile"""
    
    # Generate profile slug
    profile_slug = slugify.slugify(profile_data.business_name, to_lower=True)
    
    # Check if slug already exists and make it unique
    result = await db.execute(select(BusinessProfile).where(BusinessProfile.profile_slug == profile_slug))
    if result.scalars().first():
        counter = 1
        while True:
            new_slug = f"{profile_slug}-{counter}"
            result = await db.execute(select(BusinessProfile).where(BusinessProfile.profile_slug == new_slug))
            if not result.scalars().first():
                profile_slug = new_slug
                break
            counter += 1
    
    # Create business profile
    db_profile = BusinessProfile(
        owner_id=current_user.id,
        profile_slug=profile_slug,
        **profile_data.dict()
    )
    
    db.add(db_profile)
    await db.commit()
    await db.refresh(db_profile)
    
    return db_profile


@router.get("/", response_model=List[BusinessProfileSchema])
async def get_user_business_profiles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's business profiles"""
    
    result = await db.execute(
        select(BusinessProfile)
        .where(BusinessProfile.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .order_by(BusinessProfile.created_at.desc())
    )
    
    profiles = result.scalars().all()
    return profiles


@router.get("/public", response_model=List[BusinessProfilePublic])
async def get_public_business_profiles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    industry: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get published business profiles (public endpoint)"""
    
    query = select(BusinessProfile).where(BusinessProfile.is_published == True)
    
    if industry:
        query = query.where(BusinessProfile.industry.ilike(f"%{industry}%"))
    
    if city:
        query = query.where(BusinessProfile.city.ilike(f"%{city}%"))
    
    if search:
        query = query.where(
            BusinessProfile.business_name.ilike(f"%{search}%") |
            BusinessProfile.business_description.ilike(f"%{search}%")
        )
    
    query = query.offset(skip).limit(limit).order_by(BusinessProfile.created_at.desc())
    
    result = await db.execute(query)
    profiles = result.scalars().all()
    
    return profiles


@router.get("/{profile_id}", response_model=BusinessProfileSchema)
async def get_business_profile(
    profile_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific business profile by ID (owner only)"""
    
    result = await db.execute(
        select(BusinessProfile)
        .where(
            BusinessProfile.id == profile_id,
            BusinessProfile.owner_id == current_user.id
        )
    )
    
    profile = result.scalars().first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found"
        )
    
    return profile


@router.get("/public/{profile_slug}", response_model=BusinessProfilePublic)
async def get_public_business_profile(
    profile_slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a business profile by slug (public endpoint)"""
    
    result = await db.execute(
        select(BusinessProfile)
        .options(selectinload(BusinessProfile.reviews))
        .where(
            BusinessProfile.profile_slug == profile_slug,
            BusinessProfile.is_published == True
        )
    )
    
    profile = result.scalars().first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found"
        )
    
    return profile


@router.put("/{profile_id}", response_model=BusinessProfileSchema)
async def update_business_profile(
    profile_id: int,
    profile_update: BusinessProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a business profile"""
    
    # Check if profile exists and belongs to current user
    result = await db.execute(
        select(BusinessProfile)
        .where(
            BusinessProfile.id == profile_id,
            BusinessProfile.owner_id == current_user.id
        )
    )
    
    profile = result.scalars().first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found"
        )
    
    # Update profile
    update_data = profile_update.dict(exclude_unset=True)
    
    # Update slug if business name changed
    if "business_name" in update_data:
        new_slug = slugify.slugify(update_data["business_name"], to_lower=True)
        # Check if slug already exists
        slug_result = await db.execute(
            select(BusinessProfile)
            .where(
                BusinessProfile.profile_slug == new_slug,
                BusinessProfile.id != profile_id
            )
        )
        if not slug_result.scalars().first():
            update_data["profile_slug"] = new_slug
    
    if update_data:
        await db.execute(
            update(BusinessProfile)
            .where(BusinessProfile.id == profile_id)
            .values(**update_data)
        )
        await db.commit()
        await db.refresh(profile)
    
    return profile


@router.delete("/{profile_id}")
async def delete_business_profile(
    profile_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a business profile"""
    
    # Check if profile exists and belongs to current user
    result = await db.execute(
        select(BusinessProfile)
        .where(
            BusinessProfile.id == profile_id,
            BusinessProfile.owner_id == current_user.id
        )
    )
    
    profile = result.scalars().first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found"
        )
    
    await db.execute(delete(BusinessProfile).where(BusinessProfile.id == profile_id))
    await db.commit()
    
    return {"message": "Business profile deleted successfully"}


@router.post("/{profile_id}/upload-logo")
async def upload_logo(
    profile_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload logo for business profile"""
    
    # Check if profile exists and belongs to current user
    result = await db.execute(
        select(BusinessProfile)
        .where(
            BusinessProfile.id == profile_id,
            BusinessProfile.owner_id == current_user.id
        )
    )
    
    profile = result.scalars().first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found"
        )
    
    # Upload file
    file_url = await upload_file(file, "logos")
    
    # Update profile with logo URL
    await db.execute(
        update(BusinessProfile)
        .where(BusinessProfile.id == profile_id)
        .values(logo_url=file_url)
    )
    await db.commit()
    
    return {"logo_url": file_url}


@router.post("/{profile_id}/reviews", response_model=BusinessReviewSchema)
async def create_review(
    profile_id: int,
    review_data: BusinessReviewCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a review for a business profile (public endpoint)"""
    
    # Check if profile exists and is published
    result = await db.execute(
        select(BusinessProfile)
        .where(
            BusinessProfile.id == profile_id,
            BusinessProfile.is_published == True
        )
    )
    
    profile = result.scalars().first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found"
        )
    
    # Create review
    db_review = BusinessReview(
        business_id=profile_id,
        **review_data.dict()
    )
    
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    
    return db_review


@router.get("/{profile_id}/reviews", response_model=List[BusinessReviewSchema])
async def get_profile_reviews(
    profile_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Get reviews for a business profile"""
    
    result = await db.execute(
        select(BusinessReview)
        .where(
            BusinessReview.business_id == profile_id,
            BusinessReview.is_published == True
        )
        .offset(skip)
        .limit(limit)
        .order_by(BusinessReview.created_at.desc())
    )
    
    reviews = result.scalars().all()
    return reviews