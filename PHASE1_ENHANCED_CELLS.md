# VibeMV Enhanced - Phase 1: Quality & Consistency
# Replace your existing Colab cells with these enhanced versions

## Cell 1: Install Enhanced Dependencies
```python
# @title 📦 Install Enhanced Dependencies (3-4 minutes)
%%capture

# Core packages
!pip install -q torch torchvision diffusers transformers accelerate
!pip install -q imageio imageio-ffmpeg opencv-python pillow

# IP-Adapter for character consistency
!pip install -q ip-adapter
!pip install -q controlnet-aux

# Frame interpolation
!pip install -q cupy-cuda12x  # For GPU acceleration

print("✅ All enhanced dependencies installed!")
```

---

## Cell 2: Upload Timeline (Same as before)
```python
# @title 📤 Upload Your Timeline (VibeFrame2 or VibeMV)
from google.colab import files
import json

print('📁 Upload your timeline JSON...')
uploaded = files.upload()

timeline_file = list(uploaded.keys())[0]
with open(timeline_file, 'r') as f:
    timeline = json.load(f)

# Auto-detect format
first_scene = timeline['scenes'][0]
is_vibeframe = 'video_prompt' in first_scene or 'description' in first_scene

print(f"\n✅ Loaded {len(timeline['scenes'])} scenes")
print(f"   Duration: {timeline.get('audio_duration', 'N/A')} seconds\n")

for i, scene in enumerate(timeline['scenes'][:5]):
    if is_vibeframe:
        desc = scene.get('description', scene.get('video_prompt', ''))[:60]
        start = scene.get('start_time', 0)
        end = scene.get('end_time', 0)
        print(f"  {i+1}. {start:.1f}s-{end:.1f}s: {desc}...")
    else:
        prompt = scene.get('prompt', 'No prompt')[:60]
        print(f"  {i+1}. {prompt}...")

print(f"\n✅ Ready to generate!")
```

---

## Cell 3: Upload Character Reference (NEW!)
```python
# @title 🎭 Upload Character Reference Image (Optional but Recommended)
from google.colab import files
from PIL import Image
import torch

print('📸 Upload a reference image of your main character...')
print('   This ensures consistent character appearance across all scenes!')
print('   (Skip if you want different characters per scene)\n')

uploaded_ref = files.upload()

if uploaded_ref:
    ref_file = list(uploaded_ref.keys())[0]
    reference_image = Image.open(ref_file).convert('RGB')
    
    # Display preview
    from IPython.display import display
    print('\n✅ Character reference loaded:')
    display(reference_image.resize((256, 256)))
    
    use_character_ref = True
else:
    print('⚠️  No reference image - characters will vary per scene')
    reference_image = None
    use_character_ref = False
```

---

## Cell 4: Enhanced Image Generation
```python
# @title 🎨 Generate High-Quality Images with Character Consistency
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
from ip_adapter import IPAdapter
import os
import torch

os.makedirs('generated_images', exist_ok=True)

print('Loading Enhanced SDXL Pipeline...')

# Load SDXL with optimizations
pipe = StableDiffusionXLPipeline.from_pretrained(
    'stabilityai/stable-diffusion-xl-base-1.0',
    torch_dtype=torch.float16,
    variant='fp16',
    use_safetensors=True
).to('cuda')

# Use faster scheduler
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

# Enable memory optimizations
pipe.enable_vae_slicing()
pipe.enable_vae_tiling()

# Load IP-Adapter for character consistency
if use_character_ref:
    print('Loading IP-Adapter for character consistency...')
    ip_adapter = IPAdapter(pipe, image_encoder_path="h94/IP-Adapter", 
                           ip_ckpt="ip-adapter_sd15.bin")

# Enhanced negative prompt for quality
NEGATIVE_PROMPT = """
ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face,
out of frame, mutation, mutated, extra limbs, extra legs, extra arms,
disfigured, deformed, cross-eye, body out of frame, blurry, bad art,
bad anatomy, blurred, text, watermark, grainy, low quality, cut off
"""

scene_images = []
print(f"\n🎨 Generating {len(timeline['scenes'])} HIGH-QUALITY images...\n")
print("Settings: 1024x1024, 50 steps, character consistency enabled\n")

for i, scene in enumerate(timeline['scenes']):
    # Get prompt
    if 'video_prompt' in scene:
        prompt = scene['video_prompt']
        duration = scene['duration']
    elif 'prompt' in scene:
        prompt = scene['prompt']
        duration = scene.get('duration', 4.0)
    else:
        prompt = scene.get('description', 'A cinematic scene')
        duration = scene.get('duration', 4.0)
    
    print(f"Scene {i+1}/{len(timeline['scenes'])}: {prompt[:70]}...")
    
    # Generate with enhanced settings
    if use_character_ref:
        # With character consistency
        image = ip_adapter.generate(
            prompt=prompt,
            negative_prompt=NEGATIVE_PROMPT,
            pil_image=reference_image,
            num_inference_steps=50,
            guidance_scale=9.0,
            height=1024,
            width=1024,
            scale=0.8  # Character influence strength
        )[0]
    else:
        # Without character reference
        image = pipe(
            prompt=prompt,
            negative_prompt=NEGATIVE_PROMPT,
            num_inference_steps=50,
            guidance_scale=9.0,
            height=1024,
            width=1024
        ).images[0]
    
    # Save
    img_path = f"generated_images/scene_{i:03d}.png"
    image.save(img_path, quality=95)
    scene_images.append({'path': img_path, 'duration': duration})
    
    print(f"  ✅ Saved high-quality image ({duration:.1f}s)\n")
    
    # Memory cleanup every 5 scenes
    if (i + 1) % 5 == 0:
        torch.cuda.empty_cache()

# Final cleanup
del pipe
if use_character_ref:
    del ip_adapter
torch.cuda.empty_cache()

print(f"\n✅ Generated {len(scene_images)} high-quality images!")
print("   Resolution: 1024x1024 (4x better than before)")
print(f"   Character consistency: {'✅ Enabled' if use_character_ref else '❌ Disabled'}")
```

---

## Cell 5: Enhanced Video with Smooth Transitions
```python
# @title 🎥 Create Video with Smooth Transitions
import cv2
import numpy as np
import imageio
from PIL import Image

def apply_camera_motion(img, motion, progress):
    """Enhanced camera motion with more options"""
    h, w = img.shape[:2]
    
    motion = motion.lower()
    
    if 'zoom' in motion or 'close' in motion:
        # Zoom in effect
        scale = 1.0 + (0.3 * progress)
        new_h, new_w = int(h * scale), int(w * scale)
        zoomed = cv2.resize(img, (new_w, new_h))
        y1, x1 = (new_h - h) // 2, (new_w - w) // 2
        return zoomed[y1:y1+h, x1:x1+w]
    
    elif 'orbit' in motion or 'circle' in motion:
        # Orbital motion
        scale = 1.0 + (0.2 * np.sin(progress * np.pi))
        new_h, new_w = int(h * scale), int(w * scale)
        zoomed = cv2.resize(img, (new_w, new_h))
        y1, x1 = (new_h - h) // 2, (new_w - w) // 2
        return zoomed[y1:y1+h, x1:x1+w]
    
    elif 'pan' in motion:
        # Pan left/right
        shift = int(w * 0.2 * progress)
        M = np.float32([[1, 0, -shift], [0, 1, 0]])
        return cv2.warpAffine(img, M, (w, h))
    
    return img


def create_crossfade(img1, img2, num_frames=12):
    """Create smooth crossfade transition between scenes"""
    frames = []
    img1_pil = Image.fromarray(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    img2_pil = Image.fromarray(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    
    for i in range(num_frames):
        alpha = i / num_frames
        blended = Image.blend(img1_pil, img2_pil, alpha)
        frame = cv2.cvtColor(np.array(blended), cv2.COLOR_RGB2BGR)
        frames.append(frame)
    
    return frames


fps = 24
all_frames = []

print('🎥 Creating video with SMOOTH TRANSITIONS...\n')
print(f'Settings: {fps} FPS, crossfade transitions, camera motion\n')

for i, (scene_img, scene) in enumerate(zip(scene_images, timeline['scenes'])):
    print(f"Processing scene {i+1}/{len(scene_images)}...")
    
    # Load image
    img = cv2.imread(scene_img['path'])
    duration = scene_img['duration']
    
    # Get camera motion
    camera = scene.get('camera_angle', scene.get('camera', 'static'))
    
    # Calculate frames for this scene (leave room for transition)
    transition_frames = 12  # 0.5 seconds
    scene_frames = int(duration * fps) - (transition_frames if i < len(scene_images) - 1 else 0)
    
    # Generate frames with camera motion
    for frame_idx in range(scene_frames):
        progress = frame_idx / max(scene_frames - 1, 1)
        frame = apply_camera_motion(img.copy(), camera, progress)
        all_frames.append(frame)
    
    # Add crossfade transition to next scene
    if i < len(scene_images) - 1:
        next_img = cv2.imread(scene_images[i + 1]['path'])
        transition = create_crossfade(img, next_img, transition_frames)
        all_frames.extend(transition)
        print(f"  ✅ Added with smooth transition to next scene")
    else:
        print(f"  ✅ Final scene complete")

print(f"\n✅ Generated {len(all_frames)} smooth frames")
print(f"   Total duration: {len(all_frames) / fps:.1f} seconds")

# Export video
print('\n💾 Creating final video...')
rgb_frames = [cv2.cvtColor(f, cv2.COLOR_BGR2RGB) for f in all_frames]
imageio.mimsave('vibemv_enhanced_video.mp4', rgb_frames, fps=fps, quality=9)

print('\n✅ Enhanced video created!')
print('   Features: High quality, smooth transitions, character consistency')
files.download('vibemv_enhanced_video.mp4')
```

---

## What's Improved?

✅ **4x better resolution** (1024x1024 vs 512x512)
✅ **Character consistency** across all scenes
✅ **Better quality** with negative prompts
✅ **Smooth transitions** between scenes (crossfades)
✅ **50 inference steps** vs 30 (better detail)

**Replace your existing Colab cells with these!** 🎬
