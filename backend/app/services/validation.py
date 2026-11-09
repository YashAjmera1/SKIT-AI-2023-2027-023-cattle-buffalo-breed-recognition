"""
Sprint 4 & Security Hardening: File format verification, magic byte checks,
decompression bomb prevention, and sanitize image handling.
Lead: Kunal Rana (Backend & Database Lead)
"""

import io
from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.config import ALLOWED_CONTENT_TYPES, MAX_UPLOAD_BYTES

# Security: Defend against decompression bombs / memory exhaustion attacks
Image.MAX_IMAGE_PIXELS = 25_000_000


def _validate_image_magic_bytes(data: bytes) -> bool:
    """Verifies actual binary header bytes to prevent disguised executable payloads."""
    if len(data) < 12:
        return False

    # JPEG magic bytes: FF D8 FF
    if data[:3] == b"\xff\xd8\xff":
        return True

    # PNG magic bytes: 89 50 4E 47 0D 0A 1A 0A
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return True

    # WEBP magic bytes: RIFF....WEBP
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return True

    return False


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

    # Security: Verify binary magic bytes signature
    if not _validate_image_magic_bytes(data):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "File header failed cryptographic magic-byte verification (corrupt or disguised binary).",
        )

    try:
        image = Image.open(io.BytesIO(data))
        image.verify()  # detects malformed/corrupted files
        image = Image.open(io.BytesIO(data)).convert("RGB")  # reopen in RGB color space
    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "File is not a valid decodable image.")

    return data, image
