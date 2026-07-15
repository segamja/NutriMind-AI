from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.schemas import ScanResponse
from app.services.cnn_service import classify_food
from app.services.openai_service import analyze_food_image

router = APIRouter(prefix="/api/scan", tags=["scan"])


@router.post("", response_model=ScanResponse)
async def scan_food(image: UploadFile = File(...)):
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Image file required")

    image_bytes = await image.read()
    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty image file")

    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image too large (max 10MB)")

    try:
        cnn_result = classify_food(image_bytes)
        vision_result = analyze_food_image(image_bytes, cnn_result)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")

    return ScanResponse(cnn=cnn_result, vision=vision_result)
