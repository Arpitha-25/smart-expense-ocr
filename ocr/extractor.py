from PIL import Image
import numpy as np

def load_image_for_llm(image_path):
    return Image.open(image_path)
