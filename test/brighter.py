import os
from PIL import Image, ImageEnhance
import cv2
import numpy as np

# Set your folder path here (use '.' for the current folder)
FOLDER_PATH = "/home/daniel/Pictures/Bhutan/camera/"

# CONTROL PANEL: Choose your processing method
# Method 1: 'pillow' -> Quick, simple brightness boost (Good for evenly dark indoor/portrait photos)
# Method 2: 'opencv' -> Advanced landscape recovery (Good for high-contrast, shadowed daytime shots)
PROCESSING_METHOD = 'opencv'

# Tuning settings for Method 1 (Pillow)
PILLOW_BRIGHTNESS = 1.5

# Tuning settings for Method 2 (OpenCV Adaptive)
OPENCV_GAMMA = 0.55  # Lower = brighter shadows (try 0.4 to 0.6)
OPENCV_SATURATION_BOOST = 1.2  # Higher = more vivid colors in recovered shadows
OPENCV_SHARPENING = 1.25  # Higher = crisper edges and textures


def process_with_pillow(img_path, factor):
    """Method 1: Simple and fast brightness adjustment."""
    with Image.open(img_path) as img:
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(factor)


def process_with_opencv(image_path, gamma, saturation_boost, crispness):
    """Method 2: Advanced landscape shadow recovery with dynamic saturation and sharpening."""
    img = cv2.imread(image_path)
    if img is None:
        return None

    # --- STEP 1: SHADOW RECOVERY (HSV Space) ---
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    v_norm = v / 255.0
    shadow_mask = 1.0 - v_norm

    # Apply adaptive gamma map to protect highlights
    adaptive_gamma = gamma + (1.0 - gamma) * (1.0 - shadow_mask)
    v_corrected = np.power(v_norm, adaptive_gamma)

    # --- STEP 2: DYNAMIC COLOR PRESERVATION ---
    s_norm = s / 255.0
    adaptive_sat_boost = 1.0 + (saturation_boost - 1.0) * shadow_mask
    s_corrected = s_norm * adaptive_sat_boost

    v_final = np.clip(v_corrected * 255.0, 0, 255).astype(np.uint8)
    s_final = np.clip(s_corrected * 255.0, 0, 255).astype(np.uint8)

    enhanced_hsv = cv2.merge((h, s_final, v_final))
    result = cv2.cvtColor(enhanced_hsv, cv2.COLOR_HSV2BGR)

    # --- STEP 3: CRISP TEXTURE ENHANCEMENT ---
    blurred = cv2.GaussianBlur(result, (5, 5), 0)
    crisp_result = cv2.addWeighted(result, crispness, blurred, 1.0 - crispness, 0)

    return crisp_result


def batch_process(folder_path, method):
    output_folder = os.path.join(folder_path, f"fixed_{method}_photos")
    os.makedirs(output_folder, exist_ok=True)

    print(f"Starting batch processing using [{method.upper()}] method...\n")

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            save_path = os.path.join(output_folder, filename)
            print(f"Processing: {filename}")

            try:
                if method.lower() == 'pillow':
                    fixed_img = process_with_pillow(img_path, PILLOW_BRIGHTNESS)
                    fixed_img.save(save_path, quality=95)

                elif method.lower() == 'opencv':
                    fixed_img = process_with_opencv(
                        img_path,
                        gamma=OPENCV_GAMMA,
                        saturation_boost=OPENCV_SATURATION_BOOST,
                        crispness=OPENCV_SHARPENING
                    )
                    if fixed_img is not None:
                        cv2.imwrite(save_path, fixed_img)

                print(f"-> Saved to {output_folder}")
            except Exception as e:
                print(f"-> Error processing {filename}: {e}")


if __name__ == "__main__":
    # Dependencies required: pip install Pillow opencv-python numpy
    batch_process(FOLDER_PATH, PROCESSING_METHOD)
    print("\nAll done! Check your output folder.")
