from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import Response
from app.services.algae_service import segment_bloom

router = APIRouter()

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "tiff", "tif"}
MAX_SIZE_MB = 10

@router.post(
    "/segment",
    response_class=Response,
    responses={
        200: {"content": {"image/png": {}}, "description": "Processed image (PNG)"},
        413: {"description": "File too large"},
        415: {"description": "Unsupported extension"},
        422: {"description": "Unreadable image"},
    },
)
async def segment(image: UploadFile = File(..., description="Image to segment")):
    """
    Receives an image and returns the processed PNG directly in the body.
    Response Headers:
    - X-Contours-Count: Number of detected blooms
    - X-Original-Filename: Original filename sent
    """
    # 1. Validate extension
    ext = image.filename.rsplit(".", 1)[-1].lower() if "." in image.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"Extension '{ext}' not supported. Accepted: {sorted(ALLOWED_EXTENSIONS)}",
        )

    # 2. Read and validate file size
    image_bytes = await image.read()
    size_mb = len(image_bytes) / (1024 * 1024)
    if size_mb > MAX_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({size_mb:.1f} MB). Maximum allowed: {MAX_SIZE_MB} MB.",
        )

    # 3. Process image via service
    try:
        result_bytes, nb_contours = segment_bloom(image_bytes)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {e}")

    # 4. Return processed PNG with informative headers
    return Response(
        content=result_bytes,
        media_type="image/png",
        headers={
            "X-Contours-Count": str(nb_contours),
            "X-Original-Filename": image.filename,
        },
    )