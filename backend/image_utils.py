import requests
import os
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
import time

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}

def generate_image_pollinations(prompt, width=1024, height=768, seed=42, model="flux"):
    """
    Generates an image using Pollinations.ai (free, no API key)
    Enhanced version with more parameters for better quality
    """
    try:
        # URL encode the prompt
        prompt_encoded = requests.utils.quote(prompt)
        url = f"https://pollinations.ai/p/{prompt_encoded}?width={width}&height={height}&seed={seed}&model={model}&nologo=true"
        
        print(f"  Pollinations URL: {url[:100]}...")
        response = requests.get(url, timeout=60)
        
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            return img
        else:
            print(f"  Pollinations error {response.status_code}")
            return None
    except Exception as e:
        print(f"  Pollinations error: {e}")
        return None

def generate_image(prompt, max_retries=2):
    """
    Generates an image from a text prompt.
    First tries HuggingFace, then falls back to Pollinations.ai
    Returns the image as a PIL Image object, or None if failed.
    """
    # Try HuggingFace first
    for attempt in range(max_retries):
        try:
            payload = {"inputs": prompt, "parameters": {"num_inference_steps": 4, "guidance_scale": 0}}
            response = requests.post(HF_API_URL, headers=HEADERS, json=payload, timeout=120)
            
            if response.status_code == 200:
                print("✓ Image generated via HuggingFace")
                return Image.open(BytesIO(response.content))
            elif response.status_code == 402:
                print("⚠ HuggingFace quota exceeded, switching to Pollinations.ai...")
                break  # Don't retry, go to fallback
            elif response.status_code == 503:
                if attempt < max_retries - 1:
                    time.sleep(3)
                    continue
            else:
                print(f"HuggingFace error {response.status_code}: {response.text[:100]}")
                break  # Go to fallback
        except Exception as e:
            print(f"HuggingFace connection error: {e}")
            break  # Go to fallback
    
    # Fallback to Pollinations.ai with enhanced parameters
    print("→ Using Pollinations.ai (free alternative)...")
    
    # Use flux model for best quality, 1024x768 for presentations
    img = generate_image_pollinations(
        prompt=prompt,
        width=1024,
        height=768,
        seed=42,  # Consistent seed for reproducibility
        model="flux"  # Best quality model
    )
    
    if img:
        print("✓ Image generated via Pollinations.ai")
    return img
