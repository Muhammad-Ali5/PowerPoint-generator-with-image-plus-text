from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uvicorn
from io import BytesIO

# Import utilities
from .llm_utils import generate_slide_content
from .image_utils import generate_image
from .ppt_utils import create_presentation


app = FastAPI(title="PPT Generator API")

class GenerateRequest(BaseModel):
    topic: str
    slide_count: int

@app.post("/generate_ppt")
async def generate_ppt(request: GenerateRequest):
    try:
        # 1. Generate Content
        print(f"\n{'='*60}")
        print(f"Generating content for topic: {request.topic}...")
        print(f"Number of slides: {request.slide_count}")
        slides = generate_slide_content(request.topic, request.slide_count)
        
        if not slides:
            raise HTTPException(status_code=500, detail="Failed to generate slide content")

        print(f"✓ Generated {len(slides)} slides")
        
        # 2. Generate Images
        print(f"\n{'='*60}")
        print("Starting image generation...")
        for i, slide in enumerate(slides, 1):
            print(f"\n--- Slide {i}/{len(slides)}: {slide.get('title', 'No title')} ---")
            
            if "image_prompt" in slide:
                print(f"Image prompt: {slide['image_prompt'][:100]}...")
                print(f"Calling HuggingFace API...")
                
                img = generate_image(slide["image_prompt"])
                
                if img:
                    # Convert to bytes
                    img_byte_arr = BytesIO()
                    img.save(img_byte_arr, format='PNG')
                    slide["image_bytes"] = img_byte_arr.getvalue()
                    print(f"✓ Image generated successfully ({len(slide['image_bytes'])} bytes)")
                else:
                    print(f"✗ Failed to generate image for slide: {slide.get('title')}")
                    print(f"  Slide will have text only")
            else:
                print(f"✗ No image_prompt found in slide data")

        # 3. Create PPT
        print(f"\n{'='*60}")
        print("Assembling presentation...")
        ppt_path = create_presentation(slides, filename=f"{request.topic.replace(' ', '_')}.pptx")
        print(f"✓ Presentation saved to: {ppt_path}")
        print(f"{'='*60}\n")
        
        return FileResponse(ppt_path, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation", filename=os.path.basename(ppt_path))

    except Exception as e:
        print(f"\n{'='*60}")
        print(f"✗ ERROR: {e}")
        print(f"{'='*60}\n")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
