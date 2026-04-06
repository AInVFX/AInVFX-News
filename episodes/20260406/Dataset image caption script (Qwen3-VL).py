import os
from pathlib import Path
import torch
from transformers import Qwen3VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info

# ==========================================
# CONFIGURATION
# ==========================================
IMAGE_DIR = "/home/adrien/data/Innocence/4.InkRef/to_caption"  # Change this to your folder path
TRIGGER_WORD = "Suiboku"
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# Cap pixels to avoid OOM on 16GB VRAM
MAX_PIXELS = 1024 * 1024 

# ==========================================
# MODEL SETUP
# ==========================================
print("Loading model and processor...")
model = Qwen3VLForConditionalGeneration.from_pretrained(
    "prithivMLmods/Qwen3-VL-8B-Abliterated-Caption-it", 
    torch_dtype="auto", 
    device_map="auto"
)
processor = AutoProcessor.from_pretrained("prithivMLmods/Qwen3-VL-8B-Abliterated-Caption-it")

def get_dynamic_prompt(hint):
    """Generates a strict, concise prompt based on the filename hint."""
    return f"""You are an expert image describer. 
The primary subject(s) in this image: {hint}. (Note: if the word is plural, like 'females' or 'dogs', there are multiple subjects present).

Write a VERY CONCISE, single-paragraph description focusing only on the pose, anatomy, objects, lighting, and background. 
Keep it strictly under 40 words. Be direct. Example style: "A standing figure, arms loosely at sides, weight shifted to the left leg, three-quarter view, soft shadow on the right side of the face, simple white background."

CRITICAL RESTRICTIONS:
1. Do NOT mention the artistic medium, style, or technique. 
2. Absolutely NO words like 'ink', 'wash', 'brushstroke', 'drawing', 'sketch', 'painting', 'monochrome', 'art', 'canvas', or 'paper'. 
3. Treat the subjects/shapes as physically present in a real scene.

FORMATTING REQUIREMENTS:
1. Start your English description with a natural phrase incorporating the word {TRIGGER_WORD} without any quotes. (e.g., "In the style of {TRIGGER_WORD}, a...")
2. Immediately after the short English description, provide a highly accurate Chinese translation on a new line. Do not output anything else.
"""

def process_images(directory):
    image_paths = [p for p in Path(directory).iterdir() if p.suffix.lower() in VALID_EXTENSIONS]
    
    if not image_paths:
        print(f"No images found in {directory}")
        return

    print(f"Found {len(image_paths)} images. Starting captioning...")

    for img_path in image_paths:
        txt_path = img_path.with_suffix('.txt')
        
        # Skip if caption already exists
        if txt_path.exists():
            print(f"Skipping {img_path.name}, caption already exists.")
            continue
            
        # Parse the hint from the filename (e.g., '20260325_111213_scifi-soldier.jpg' -> 'scifi soldier')
        # Splitting by '_' and taking the last part before the extension, then replacing '-' with space.
        raw_hint = img_path.stem.split('_')[-1]
        clean_hint = raw_hint.replace('-', ' ')
            
        print(f"Processing {img_path.name} with hint: '{clean_hint}'...")

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": f"file://{img_path.absolute()}",
                        "max_pixels": MAX_PIXELS,
                    },
                    {"type": "text", "text": get_dynamic_prompt(clean_hint)},
                ],
            }
        ]

        # Process inputs
        text = processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        
        inputs = processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to("cuda")

        # Generate caption - max_new_tokens left at 256 to ensure the Chinese translation fits, 
        # but the prompt restricts the model from using them all.
        with torch.no_grad():
            generated_ids = model.generate(**inputs, max_new_tokens=256)
            
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        
        output_text = processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )[0]

        clean_caption = output_text.strip().replace("```", "")

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(clean_caption)
            
        print(f"Saved caption to {txt_path.name}\n")

if __name__ == "__main__":
    process_images(IMAGE_DIR)
    print("Captioning complete!")
