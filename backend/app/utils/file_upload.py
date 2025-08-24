import os
import uuid
from typing import Optional
from fastapi import HTTPException, UploadFile
import aiofiles
from PIL import Image
import io

from app.core.config import settings


ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_DOCUMENT_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt"}


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return os.path.splitext(filename)[1].lower()


def validate_image_file(file: UploadFile) -> bool:
    """Validate if file is an allowed image type"""
    if not file.filename:
        return False
    
    extension = get_file_extension(file.filename)
    return extension in ALLOWED_IMAGE_EXTENSIONS


def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename while preserving extension"""
    extension = get_file_extension(original_filename)
    unique_id = str(uuid.uuid4())
    return f"{unique_id}{extension}"


async def save_file(file: UploadFile, folder: str) -> str:
    """Save uploaded file to disk"""
    
    # Create upload directory if it doesn't exist
    upload_path = os.path.join(settings.UPLOAD_FOLDER, folder)
    os.makedirs(upload_path, exist_ok=True)
    
    # Generate unique filename
    filename = generate_unique_filename(file.filename or "file")
    file_path = os.path.join(upload_path, filename)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # Return URL path
    return f"/static/uploads/{folder}/{filename}"


async def compress_image(file_content: bytes, max_size: tuple = (1200, 1200), quality: int = 85) -> bytes:
    """Compress image to reduce file size"""
    try:
        # Open image
        image = Image.open(io.BytesIO(file_content))
        
        # Convert to RGB if necessary
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        
        # Resize if larger than max_size
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save compressed image
        output = io.BytesIO()
        image.save(output, format="JPEG", quality=quality, optimize=True)
        
        return output.getvalue()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")


async def upload_file(file: UploadFile, folder: str, compress: bool = True) -> str:
    """Upload and optionally compress file"""
    
    # Validate file size
    if file.size and file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    # Validate file type for images
    if folder in ["logos", "banners", "images"] and not validate_image_file(file):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only images are allowed (jpg, jpeg, png, gif, webp)"
        )
    
    # Read file content
    file_content = await file.read()
    
    # Compress image if requested and it's an image
    if compress and folder in ["logos", "banners", "images"]:
        file_content = await compress_image(file_content)
    
    # Create upload directory
    upload_path = os.path.join(settings.UPLOAD_FOLDER, folder)
    os.makedirs(upload_path, exist_ok=True)
    
    # Generate unique filename
    filename = generate_unique_filename(file.filename or "file")
    file_path = os.path.join(upload_path, filename)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(file_content)
    
    # Return URL path
    return f"/static/uploads/{folder}/{filename}"


async def delete_file(file_path: str) -> bool:
    """Delete a file from disk"""
    try:
        if file_path.startswith("/static/"):
            # Convert URL path to file system path
            relative_path = file_path[8:]  # Remove '/static/'
            full_path = os.path.join("static", relative_path)
            
            if os.path.exists(full_path):
                os.remove(full_path)
                return True
        return False
    except Exception:
        return False