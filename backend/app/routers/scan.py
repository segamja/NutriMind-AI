from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.schemas import ScanResponse
from app.services.cnn_service import classify_food
from app.services.image_utils import detect_mime, is_valid_image
from app.services.openai_service import analyze_food_image

router = APIRouter(prefix="/api/scan", tags=["scan"])


def _is_image_content_type(content_type: str | None) -> bool:
    if not content_type:
        return False
    if content_type.startswith("image/"):
        return True
    return content_type == "application/octet-stream"


@router.post("", response_model=ScanResponse)
async def scan_food(image: UploadFile = File(...)):
    image_bytes = await image.read()
    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty image file")

    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image too large (max 10MB)")

    if not _is_image_content_type(image.content_type):
        if not is_valid_image(image_bytes):
            raise HTTPException(status_code=400, detail="Image file required")
    elif image.content_type == "application/octet-stream":
        if not is_valid_image(image_bytes):
            raise HTTPException(status_code=400, detail="Invalid image file")

    mime_type = detect_mime(image_bytes)

    try:
        cnn_result = classify_food(image_bytes)
        vision_result = analyze_food_image(image_bytes, cnn_result, mime_type)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")

    return ScanResponse(cnn=cnn_result, vision=vision_result)
