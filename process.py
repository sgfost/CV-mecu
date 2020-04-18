import sys
import os

# call the backend to count eggs, save results etc.
def count(image_path, backend):
    print(f"processing image {image_path} with method: {backend}")
