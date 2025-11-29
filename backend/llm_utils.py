import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_slide_content(topic: str, slide_count: int):
    """
    Generates content for a PowerPoint presentation using Gemini.
    Returns a list of dictionaries, each representing a slide.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
    Create a detailed outline for a PowerPoint presentation on the topic: "{topic}".
    The presentation should have exactly {slide_count} slides.
    
    For each slide, provide:
    1. "title": A catchy title.
    2. "content": Bullet points (3-5 points) summarizing the key information.
    3. "image_prompt": A descriptive prompt to generate a relevant image for this slide.
    
    Output the result strictly as a JSON list of objects. 
    Example format:
    [
        {{
            "title": "Introduction to AI",
            "content": ["Definition of AI", "History of AI", "Types of AI"],
            "image_prompt": "A futuristic robot shaking hands with a human, digital art style"
        }}
    ]
    Do not include markdown formatting like ```json ... ```. Just the raw JSON string.
    """
    
    try:
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        
        print(f"LLM Raw Response (first 500 chars):\n{text_response[:500]}\n")
        
        # Clean up potential markdown code blocks if the model adds them
        if text_response.startswith("```json"):
            text_response = text_response[7:]
        if text_response.startswith("```"):
            text_response = text_response[3:]
        if text_response.endswith("```"):
            text_response = text_response[:-3]
        
        text_response = text_response.strip()
            
        slides = json.loads(text_response)
        
        print(f"Parsed {len(slides)} slides from LLM")
        for i, slide in enumerate(slides, 1):
            print(f"  Slide {i}: '{slide.get('title', 'NO TITLE')}'")
            print(f"    Has image_prompt: {'image_prompt' in slide}")
            if 'image_prompt' in slide:
                print(f"    Image prompt: {slide['image_prompt'][:80]}...")
        
        return slides
    except Exception as e:
        print(f"Error generating content: {e}")
        import traceback
        traceback.print_exc()
        return []
