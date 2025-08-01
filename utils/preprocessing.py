from PIL import Image, ImageEnhance

def enhance_image(image):
    """Simple enhancement: adjust contrast and sharpness."""
    enhancer = ImageEnhance.Contrast(image)
    img_enhanced = enhancer.enhance(1.8)
    enhancer = ImageEnhance.Sharpness(img_enhanced)
    img_enhanced = enhancer.enhance(2.0)
    return img_enhanced
