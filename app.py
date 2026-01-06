"""
VibeMV Studio - AI Music Video Generator
Compatible with Gradio 4.x (managed by HF Spaces)
"""

import gradio as gr
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scenes_state = []

def analyze_audio(audio_file):
    """Analyze audio and detect beats."""
    if not audio_file:
        return "❌ Please upload an audio file first."
    
    try:
        import librosa
        
        y, sr = librosa.load(audio_file)
        duration = librosa.get_duration(y=y, sr=sr)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        
        scene_times = []
        min_interval = 4.0
        last_time = 0
        
        for beat_time in beat_times:
            if beat_time - last_time >= min_interval:
                scene_times.append(float(beat_time))
                last_time = beat_time
        
        if duration - last_time > 2.0:
            scene_times.append(float(duration))
        
        return f"""✅ Audio Analysis Complete!

Duration: {duration:.2f}s | Tempo: {tempo:.1f} BPM | Beats: {len(beat_times)}

Suggested {len(scene_times)} scenes at: {', '.join([f'{t:.1f}s' for t in scene_times[:8]])}...

Add scenes below!"""
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

def add_scene(prompt, start, duration, camera):
    """Add scene to timeline."""
    global scenes_state
    
    scene = {
        "id": len(scenes_state) + 1,
        "prompt": prompt or "Scene",
        "start_time": float(start or 0),
        "duration": float(duration or 4),
        "camera": camera
    }
    scenes_state.append(scene)
    
    timeline = "📽️ Timeline:\n\n"
    for s in scenes_state:
        timeline += f"Scene {s['id']}: {s['start_time']:.1f}-{s['start_time']+s['duration']:.1f}s | {s['prompt'][:40]} | {s['camera']}\n"
    
    return timeline, f"✅ Added Scene {scene['id']}"

def export_json():
    """Export timeline."""
    return json.dumps({"version": "1.0", "scenes": scenes_state}, indent=2)

def clear_all():
    """Clear timeline."""
    global scenes_state
    scenes_state = []
    return "", "✅ Cleared", ""

# Build UI
with gr.Blocks(title="VibeMV Studio") as demo:
    gr.Markdown("# 🎬 VibeMV Studio")
    gr.Markdown("AI Music Video Timeline Generator")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 1. Upload Audio")
            audio = gr.Audio(label="Music File", type="filepath")
            analyze_btn = gr.Button("Analyze Audio", variant="primary")
            analysis_out = gr.Textbox(label="Results", lines=6)
            
            gr.Markdown("### 2. Add Scenes")
            prompt = gr.Textbox(label="Scene Description", placeholder="Describe the scene...")
            
            with gr.Row():
                start = gr.Number(label="Start (s)", value=0)
                dur = gr.Number(label="Duration (s)", value=4)
            
            camera = gr.Dropdown(
                ["static", "orbit", "zoom_in", "zoom_out", "pan_left", "pan_right"],
                value="orbit",
                label="Camera"
            )
            
            add_btn = gr.Button("Add Scene", variant="primary")
            status = gr.Textbox(label="Status", lines=1)
            
            gr.Markdown("### 3. Export")
            with gr.Row():
                export_btn = gr.Button("Export JSON")
                clear_btn = gr.Button("Clear")
        
        with gr.Column():
            gr.Markdown("### Timeline")
            timeline = gr.Textbox(label="Scenes", lines=12, placeholder="Add scenes...")
            
            gr.Markdown("### JSON Export")
            json_out = gr.Textbox(label="Timeline JSON", lines=10)
    
    # Events
    analyze_btn.click(analyze_audio, inputs=[audio], outputs=[analysis_out])
    add_btn.click(add_scene, inputs=[prompt, start, dur, camera], outputs=[timeline, status])
    export_btn.click(export_json, outputs=[json_out])
    clear_btn.click(clear_all, outputs=[timeline, status, json_out])

if __name__ == "__main__":
    demo.launch()
