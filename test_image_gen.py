"""
Quick test script to verify image generation is working
"""
from backend.image_utils import generate_image
from backend.llm_utils import generate_slide_content

print("="*60)
print("TEST 1: Testing LLM Content Generation")
print("="*60)

slides = generate_slide_content("Artificial Intelligence", 2)
print(f"\nGenerated {len(slides)} slides")

for i, slide in enumerate(slides, 1):
    print(f"\nSlide {i}:")
    print(f"  Title: {slide.get('title', 'NO TITLE')}")
    print(f"  Content points: {len(slide.get('content', []))}")
    print(f"  Has image_prompt: {'image_prompt' in slide}")
    if 'image_prompt' in slide:
        print(f"  Image prompt: {slide['image_prompt']}")

print("\n" + "="*60)
print("TEST 2: Testing Image Generation")
print("="*60)

if slides and 'image_prompt' in slides[0]:
    test_prompt = slides[0]['image_prompt']
    print(f"\nTrying to generate image with prompt:")
    print(f"  '{test_prompt}'")
    
    img = generate_image(test_prompt)
    
    if img:
        print(f"\n✓ SUCCESS! Image generated")
        print(f"  Size: {img.size}")
        print(f"  Format: {img.format}")
    else:
        print(f"\n✗ FAILED! Image generation returned None")
        print(f"  Check your HF_TOKEN in .env file")
else:
    print("\n✗ No image_prompt found in slides, cannot test image generation")

print("\n" + "="*60)
