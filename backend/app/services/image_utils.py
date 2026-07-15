from io import BytesIO

from PIL import Image, UnidentifiedImageError

MIME_MAP = {
    "JPEG": "image/jpeg",
    "PNG": "image/png",
    "WEBP": "image/webp",
    "GIF": "image/gif",
}


def is_valid_image(image_bytes: bytes) -> bool:
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            img.verify()
        return True
    except (UnidentifiedImageError, OSError, ValueError):
        return False


def detect_mime(image_bytes: bytes) -> str:
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            return MIME_MAP.get(img.format or "", "image/jpeg")
    except (UnidentifiedImageError, OSError, ValueError):
        return "image/jpeg"
