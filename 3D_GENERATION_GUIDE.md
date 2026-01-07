# VibeMV 3D Model Generation Guide - Google Colab

This guide shows you how to generate 3D models from your VibeMV scenes using free Google Colab GPU.

---

## Overview

We'll use **TripoSR** for image-to-3D conversion. It's the most compatible with free Colab's T4 GPU.

**Workflow:**
```
VibeMV Scenes → Generate Images → TripoSR → 3D Models → View/Export
```

---

## Step-by-Step Setup

### Step 1: Prepare Your VibeMV Timeline

1. Go to https://huggingface.co/spaces/Westcoastrenmen/Vibemv
2. Create your timeline with scenes
3. Click "Export JSON"
4. Save the `vibemv_timeline.json` file

### Step 2: Open the 3D Generation Colab Notebook

1. Open the notebook: `VibeMV_3D_Generator.ipynb` (I'll create this for you)
2. **Important**: Click "Runtime" → "Change runtime type"
3. Select "T4 GPU"
4. Click "Save"

### Step 3: Run the Setup Cells

Execute these cells in order:

#### Cell 1: Install Dependencies
```python
# This installs TripoSR and required packages
# Takes ~2-3 minutes
```

#### Cell 2: Upload Timeline
```python
# Upload your vibemv_timeline.json
# Or it will auto-load if you clicked from VibeMV
```

#### Cell 3: Generate Images from Prompts
```python
# Uses Stable Diffusion XL on GPU
# Generates one image per scene
# ~10-15 seconds per image
```

### Step 4: Generate 3D Models

#### Cell 4: Run TripoSR
```python  
# Converts each image to 3D model
# Creates .obj and .glb files
# ~30-60 seconds per model
```

### Step 5: View and Download

#### Cell 5: Preview 3D Models
```python
# Shows interactive 3D viewer in Colab
# Rotate and inspect your models
```

#### Cell 6: Download Models
```python
# Downloads all 3D models as ZIP
# Includes .obj, .glb, and textures
```

---

## What You Get

For each scene in your timeline:
- **Image** (PNG) - The generated scene
- **3D Model** (.obj) - Textured 3D mesh
- **GLTF** (.glb) - Web-compatible 3D format
- **Textures** - Color/normal maps

---

## Using 3D Models

### Option 1: Import to Blender
1. Download the ZIP
2. Open Blender
3. File → Import → Wavefront (.obj)
4. Select your model
5. Animate, light, render!

### Option 2: Web Viewer
1. Use the .glb files
2. View in https://gltf-viewer.donmccurdy.com/
3. Or embed in web pages with Three.js

### Option 3: Back to VibeMV
1. Render your 3D model from different angles in Blender
2. Export as images
3. Use as reference images in VibeMV

---

## Advanced: Other 3D Projects

### Hunyuan3D (Requires more VRAM)

**Setup:**
```python
!git clone https://github.com/Tencent-Hunyuan/Hunyuan3D-2
!cd Hunyuan3D-2 && pip install -r requirements.txt
```

**Note:** Hunyuan3D needs ~16GB VRAM. Works on Colab Pro with A100.

### TRELLIS (Experimental)

**Setup:**
```python
!git clone https://github.com/microsoft/TRELLIS  
!cd TRELLIS && pip install -e .
```

**Note:** TRELLIS is cutting-edge but may be unstable.

---

## Common Issues

### "Out of Memory"
- **Solution**: Reduce image resolution to 256x256
- Or use Colab Pro for more VRAM

### "Model Loading Fails"
- **Solution**: Clear runtime and restart
- Make sure GPU is enabled

### "Generation Too Slow"
- **Solution**: Process fewer scenes at once
- Or upgrade to Colab Pro for faster GPU

---

## Cost Comparison

| Option | GPU | Time per Model | Quality | Cost |
|--------|-----|---------------|---------|------|
| **Colab Free** | T4 | ~60s | Good | Free |
| **Colab Pro** | A100 | ~20s | Excellent | $10/month |
| **Local GPU** | Your GPU | Varies | Varies | Free (after hardware) |

---

## Next Steps

1. **Try the basic TripoSR workflow** (easiest)
2. Once comfortable, experiment with Hunyuan3D (better quality)
3. Import 3D models to Blender for animation
4. Render from multiple angles
5. Use in VibeMV as reference images

---

## Need Help?

- Check Colab notebook comments
- Visit project GitHub pages
- Ask in VibeMV Space discussions
