import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def normalize_signature_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # Threshold with OTSU (binary inverted)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Morph to close gaps in strokes
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Get bounding box
    coords = cv2.findNonZero(morph)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        cropped = morph[y:y+h, x:x+w]
    else:
        cropped = morph

    # Make square canvas
    max_dim = max(cropped.shape)
    square = np.ones((max_dim, max_dim), dtype=np.uint8) * 0
    x_offset = (max_dim - cropped.shape[1]) // 2
    y_offset = (max_dim - cropped.shape[0]) // 2
    square[y_offset:y_offset+cropped.shape[0], x_offset:x_offset+cropped.shape[1]] = cropped

    resized = cv2.resize(square, (300, 300))
    return resized




def preprocess_for_contours(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh


def extract_largest_contour(thresh_img):
    contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        return max(contours, key=cv2.contourArea)
    return None


def match(path1, path2):
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)

    # === Normalize before comparison ===
    gray1 = normalize_signature_image(img1)
    gray2 = normalize_signature_image(img2)

    cv2.imwrite("normalized1.png", gray1)
    cv2.imwrite("normalized2.png", gray2)

# 🔬 SSIM comparison + debug difference image
    ssim_score, diff = ssim(gray1, gray2, full=True)
    diff = (diff * 255).astype("uint8")
    cv2.imwrite("ssim_diff.png", diff)

    # === SSIM Calculation ===
    similarity = ssim(gray1, gray2) * 100
    similarity = float(f"{similarity:.2f}")

    if similarity >= 90:
        return similarity

    if similarity < 75:
        return similarity

    # Borderline (75-90), use contour for boosting or penalizing
    thresh1 = preprocess_for_contours(img1)
    thresh2 = preprocess_for_contours(img2)

    contour1 = extract_largest_contour(thresh1)
    contour2 = extract_largest_contour(thresh2)

    if contour1 is not None and contour2 is not None:
        shape_score = cv2.matchShapes(contour1, contour2, cv2.CONTOURS_MATCH_I1, 0.0)
    print(f"Contour Shape Score: {shape_score}")

    # 🔍 Debugging output
    cv2.drawContours(img1, [contour1], -1, (0, 255, 0), 2)
    cv2.drawContours(img2, [contour2], -1, (0, 255, 0), 2)
    cv2.imwrite("contour1_debug.png", img1)
    cv2.imwrite("contour2_debug.png", img2)

    # if shape_score < 0.1:
    #     similarity += 10
    # elif shape_score > 1.0:
    #     similarity -= 10

    return float(f"{similarity:.2f}")
