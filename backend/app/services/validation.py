"""Sprint 4: file format checks and invalid image handling."""
import io
from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.config import ALLOWED_CONTENT_TYPES, MAX_UPLOAD_BYTES


async def read_and_validate_image(file: UploadFile | None) -> tuple[bytes, Image.Image]:
    if file is None or not file.filename:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No image file was provided.")

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Unsupported file type '{file.content_type}'. Allowed: JPEG, PNG, WEBP.",
        )

    data = await file.read()
    if len(data) == 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Uploaded file is empty.")
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            f"File too large. Maximum size is {MAX_UPLOAD_BYTES // (1024 * 1024)} MB.",
        )

    try:
        image = Image.open(io.BytesIO(data))
        image.verify()                      # detects corrupt files
        image = Image.open(io.BytesIO(data)).convert("RGB")  # reopen after verify()
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "File is not a valid image.")

    return data, image
