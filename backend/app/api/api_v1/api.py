from fastapi import APIRouter

from app.api.api_v1.endpoints import business_profiles, auth, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(business_profiles.router, prefix="/business-profiles", tags=["business-profiles"])