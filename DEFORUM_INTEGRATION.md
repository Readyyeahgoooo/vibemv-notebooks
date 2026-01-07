# Deforum Keyframe Converter for VibeMV

Convert your VibeFrame2 timeline JSON into Deforum-compatible keyframe schedules for AUTOMATIC1111.

---

## What is Deforum?

Deforum is an extension for AUTOMATIC1111's Stable Diffusion WebUI that creates smooth animations by interpolating between keyframed prompts.

**Advantages:**
- 🎯 Precise control over scene transitions
- 📐 Mathematical keyframing (ease in/out, curves)
- 🎬 Smooth prompt morphing between scenes
- 💪 Powerful camera motion equations
- 🎨 Works with any SD model

---

## Installation

### Option 1: AUTOMATIC1111 Extension
```bash
# In your stable-diffusion-webui folder
git clone https://github.com/deforum-art/sd-webui-deforum extensions/deforum
```

Then restart WebUI and look for the "Deforum" tab.

### Option 2: Colab
Use the official Deforum Colab notebook:
https://colab.research.google.com/github/deforum-art/sd-webui-deforum/blob/main/Deforum_Stable_Diffusion.ipynb

---

## Converting VibeMV Timeline to Deforum

Here's a Python script to convert your timeline JSON:

```python
import json

def vibemv_to_deforum(timeline_file, output_file='deforum_schedule.txt'):
    """Convert VibeFrame2 timeline to Deforum keyframe schedule"""
    
    with open(timeline_file, 'r') as f:
        timeline = json.load(f)
    
    fps = 24
    prompts = []
    frame_number = 0
    
    for i, scene in enumerate(timeline['scenes']):
        # Get prompt and timing
        prompt = scene.get('video_prompt', scene.get('description', ''))
        start_frame = int(scene['start_time'] * fps)
        
        # Clean prompt for Deforum (remove quality tags that conflict)
        prompt = prompt.replace('high quality', '').replace('detailed', '')
        prompt = prompt.strip().rstrip(',').strip()
        
        # Add keyframe
        prompts.append(f"{start_frame}: {prompt}")
    
    # Write Deforum schedule
    schedule = "\\n".join(prompts)
    
    with open(output_file, 'w') as f:
        f.write("# VibeMV Deforum Schedule\\n")
        f.write("# Paste this into Deforum's 'Prompts' field\\n\\n")
        f.write(schedule)
    
    print(f"✅ Created {output_file}")
    print(f"   {len(prompts)} keyframes")
    print(f"\\nFirst 3 keyframes:")
    for p in prompts[:3]:
        print(f"  {p[:80]}...")
    
    return schedule

# Usage
schedule = vibemv_to_deforum('vibemv_timeline.json')
```

---

## Deforum Settings for Best Results

### Animation Settings
```
Max Frames: [calculate from timeline duration * fps]
FPS: 24
Interpolation: Film (for smoothest motion)
```

### Camera Motion (3D Mode)
```python
# Example for zoom + pan
translation_z = "0:(0), 100:(2), 200:(0)"  # Zoom rhythm
translation_x = "0:(0), 100:(1), 200:(-1)" # Pan motion
rotation_3d_y = "0:(0), 100:(5), 200:(0)"  # Gentle rotation
```

### Strength Schedule
```python
# Control how much each frame changes
strength_schedule = "0:(0.65)"  # Higher = more motion
```

---

## Advanced: Math Keyframing

Deforum supports mathematical expressions for smooth motion:

```python
# Sine wave camera motion
translation_z = "0: (2 * sin(t/20))"

# Ease in/out zoom
translation_z = "0: (lerp(0, 5, easeInOut(t/100)))"

# Beat-synced motion (165 BPM ≈ 0.36s per beat ≈ 8.7 frames)
translation_z = "0: (abs(sin(t * 3.14159 / 8.7)))"
```

---

## Complete Workflow

1. **Generate Schedule**
   ```bash
   python vibemv_to_deforum.py vibemv_timeline.json
   ```

2. **Open Deforum**
   - Launch AUTOMATIC1111 WebUI
   - Click "Deforum" tab

3. **Paste Schedule**
   - Copy contents of `deforum_schedule.txt`
   - Paste into "Prompts" field

4. **Configure**
   - Set max frames (duration * 24)
   - Choose 2D or 3D mode
   - Set camera motion equations

5. **Generate**
   - Click "Generate"
   - Wait for animation
   - Download result

---

## Tips for VibeMV + Deforum

**Character Consistency:**
```
Use LoRA or Textual Inversion for your character
Add to all prompts: "<lora:character:0.8>"
```

**Scene Transitions:**
```python
# Smooth crossfade between scenes
strength_schedule = "0:(0.5), 100:(0.7), 120:(0.5)"
```

**Audio Sync:**
Use the beat times from your timeline to create rhythmic camera motion.

---

## Example Output

Input (VibeMV timeline):
```json
{
  "scenes": [
    {"start_time": 0, "description": "Dark pier at night"},
    {"start_time": 4.1, "description": "Rain begins to fall"}
  ]
}
```

Output (Deforum schedule):
```
0: Dark pier at night, cinematic
98: Rain begins to fall, atmospheric
```

---

## Resources

- [Deforum GitHub](https://github.com/deforum-art/sd-webui-deforum)
- [Deforum Discord](https://discord.gg/deforum)
- [Math Functions Guide](https://github.com/deforum-art/sd-webui-deforum/wiki/Math-Functions)
- [Video Tutorial](https://www.youtube.com/results?search_query=deforum+stable+diffusion+tutorial)

---

## Next: Hybrid Approach

Combine Deforum's precise control with VibeMV's workflow:
1. Use VibeMV for timeline creation
2. Convert to Deforum for generation
3. Use SVD/AnimateDiff for final quality boost
