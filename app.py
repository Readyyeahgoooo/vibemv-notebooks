"""
VibeMV Studio - AI Music Video Generator
Main Gradio Application (Simplified to avoid schema errors)
"""

import gradio as gr
import os
import json
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state for scenes
scenes_state = []

def analyze_audio(audio_file):
    """Analyze audio file and detect beats for timeline."""
    if not audio_file:
        return "❌ Please upload an audio file first."
    
    try:
        import librosa
        
        # Load audio
        y, sr = librosa.load(audio_file)
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Detect beats
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        
        # Create suggested scene timestamps
        scene_times = []
        min_interval = 4.0
        last_time = 0
        
        for beat_time in beat_times:
            if beat_time - last_time >= min_interval:
                scene_times.append(float(beat_time))
                last_time = beat_time
        
        if duration - last_time > 2.0:
            scene_times.append(float(duration))
        
        analysis_text = f"""✅ **Audio Analysis Complete!**

📊 **Audio Info:**
- Duration: {duration:.2f} seconds
- Tempo: {tempo:.1f} BPM
- Detected beats: {len(beat_times)}

🎬 **Suggested Scene Cuts:**
- Number of scenes: {len(scene_times)}
- Timestamps: {', '.join([f'{t:.1f}s' for t in scene_times[:10]])}{'...' if len(scene_times) > 10 else ''}

Click "Add Scene" to start building your music video!
"""
        
        global scenes_state
        scenes_state = []
        
        return analysis_text
        
    except Exception as e:
        logger.error(f"Audio analysis failed: {e}")
        return f"❌ Audio analysis failed: {str(e)}"

def add_scene(prompt, start_time, duration, camera_motion):
    """Add a new scene to the timeline."""
    global scenes_state
    
    scene = {
        "id": len(scenes_state) + 1,
        "prompt": prompt or "Scene description",
        "start_time": float(start_time) if start_time else 0.0,
        "duration": float(duration) if duration else 4.0,
        "camera_motion": camera_motion
    }
    
    scenes_state.append(scene)
    
    # Create timeline visualization
    timeline_text = "📽️ **Current Timeline:**\n\n"
    for s in scenes_state:
        timeline_text += f"**Scene {s['id']}** ({s['start_time']:.1f}s - {s['start_time'] + s['duration']:.1f}s)\n"
        timeline_text += f"  - Prompt: {s['prompt'][:50]}...\n"
        timeline_text += f"  - Camera: {s['camera_motion']}\n\n"
    
    return timeline_text, f"✅ Added Scene {scene['id']}"

def export_timeline():
    """Export the current timeline as JSON."""
    global scenes_state
    
    timeline_data = {
        "version": "1.0",
        "scenes": scenes_state
    }
    
    return json.dumps(timeline_data, indent=2)

def clear_timeline():
    """Clear all scenes."""
    global scenes_state
    scenes_state = []
    return "", "✅ Timeline cleared", ""

# Create Gradio Interface
with gr.Blocks(title="VibeMV Studio", theme=gr.themes.Soft()) as app:
    
    gr.Markdown("# 🎬 VibeMV Studio - AI Music Video Generator")
    gr.Markdown("Create professional music videos with AI-powered scene generation")
    
    with gr.Row():
        # Left Column
        with gr.Column(scale=1):
            gr.Markdown("## 📤 Step 1: Upload Audio")
            audio_input = gr.Audio(label="Music File", type="filepath")
            analyze_btn = gr.Button("🔍 Analyze Audio", variant="primary")
            
            audio_analysis = gr.Textbox(label="Analysis Results", lines=8)
            
            gr.Markdown("## 🎨 Step 2: Add Scenes")
            
            scene_prompt = gr.Textbox(
                label="Scene Description",
                placeholder="E.g., A cartoon bear running through a university campus...",
                lines=2
            )
            
            with gr.Row():
                start_time = gr.Number(label="Start Time (s)", value=0.0)
                duration = gr.Number(label="Duration (s)", value=4.0)
            
            camera_motion = gr.Dropdown(
                choices=["static", "orbit", "zoom_in", "zoom_out", "pan_left", "pan_right", "flythrough"],
                value="orbit",
                label="Camera Motion"
            )
            
            add_scene_btn = gr.Button("➕ Add Scene to Timeline", variant="primary")
            scene_status = gr.Textbox(label="Status", lines=1)
            
            gr.Markdown("## 🎬 Step 3: Export")
            
            with gr.Row():
                export_btn = gr.Button("💾 Export Timeline JSON", variant="primary")
                clear_btn = gr.Button("🗑️ Clear Timeline", variant="secondary")
        
        # Right Column
        with gr.Column(scale=1):
            gr.Markdown("## 📽️ Timeline")
            
            timeline_display = gr.Textbox(
                label="Scene Timeline",
                lines=15,
                placeholder="Add scenes to see them here..."
            )
            
            gr.Markdown("## 💾 Export JSON")
            
            timeline_json = gr.Textbox(
                label="Timeline JSON",
                lines=10,
                placeholder="Click 'Export Timeline JSON' to generate..."
            )
    
    # Info Section
    with gr.Accordion("ℹ️ About VibeMV Studio", open=False):
        gr.Markdown("""
        ### 🌟 Features
        - **Prompt-Driven**: Describe scenes with text
        - **Timeline Editor**: Visual scene arrangement
        - **Audio Sync**: Automatic beat detection
        - **Camera Control**: Multiple camera motion presets
        
        ### 📝 Workflow
        1. Upload audio → Analyze for beat detection
        2. Add scenes with prompts and camera motions
        3. Arrange on timeline
        4. Export as JSON for further processing
        
        ### ⚠️ Current Status
        This is an MVP framework. Video generation will be added in future updates.
        
        ### 🔮 Coming Soon
        - Reference image upload for 3D integration
        - Video generation with Stable Video Diffusion
        - Frame interpolation for smooth playback
        """)
    
    # Event Handlers
    analyze_btn.click(
        fn=analyze_audio,
        inputs=[audio_input],
        outputs=[audio_analysis]
    )
    
    add_scene_btn.click(
        fn=add_scene,
        inputs=[scene_prompt, start_time, duration, camera_motion],
        outputs=[timeline_display, scene_status]
    )
    
    export_btn.click(
        fn=export_timeline,
        outputs=[timeline_json]
    )
    
    clear_btn.click(
        fn=clear_timeline,
        outputs=[timeline_display, scene_status, timeline_json]
    )

if __name__ == "__main__":
    logger.info("Starting VibeMV Studio...")
    app.launch()
