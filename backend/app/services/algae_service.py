import cv2
import numpy as np

def segment_bloom(image_bytes: bytes) -> tuple[bytes, int]:
    """
    Perform Otsu segmentation and colorize bloom areas in red.
    Args: image_bytes: Raw image file bytes.
    Returns: tuple: (Processed PNG bytes, Count of detected contours)
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Could not decode image. Unsupported format.")

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Otsu Thresholding
    _, mask = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find Contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create semi-transparent red overlay + green contours
    overlay = img_rgb.copy()
    cv2.drawContours(overlay, contours, -1, (255, 0, 0), -1)
    result = cv2.addWeighted(img_rgb, 0.5, overlay, 0.5, 0)
    cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

    # Encode back to PNG for response
    result_bgr = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    success, buffer = cv2.imencode(".png", result_bgr)
    if not success:
        raise RuntimeError("Failed to encode result image.")

    return buffer.tobytes(), len(contours)
