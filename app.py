"""
VibeMV Studio - AI Music Video Generator
Streamlit Version (No dependency conflicts!)
"""

import streamlit as st
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize session state
if 'scenes' not in st.session_state:
    st.session_state.scenes = []

def analyze_audio(audio_file):
    """Analyze audio and detect beats."""
    try:
        import librosa
        import tempfile
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name
        
        y, sr = librosa.load(tmp_path)
        duration = librosa.get_duration(y=y, sr=sr)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        
        # Calculate scene suggestions
        scene_times = []
        min_interval = 4.0
        last_time = 0
        
        for beat_time in beat_times:
            if beat_time - last_time >= min_interval:
                scene_times.append(float(beat_time))
                last_time = beat_time
        
        if duration - last_time > 2.0:
            scene_times.append(float(duration))
        
        # Clean up temp file
        Path(tmp_path).unlink()
        
        return {
            'duration': float(duration),
            'tempo': float(tempo),
            'beats': len(beat_times),
            'scene_times': scene_times
        }
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return None

def add_scene(prompt, start, duration, camera):
    """Add scene to timeline."""
    scene = {
        "id": len(st.session_state.scenes) + 1,
        "prompt": prompt or "Scene",
        "start_time": float(start),
        "duration": float(duration),
        "camera": camera
    }
    st.session_state.scenes.append(scene)

def export_timeline():
    """Export timeline as JSON."""
    return json.dumps({
        "version": "1.0",
        "scenes": st.session_state.scenes
    }, indent=2)

def clear_timeline():
    """Clear all scenes."""
    st.session_state.scenes = []

# Page config
st.set_page_config(
    page_title="VibeMV Studio",
    page_icon="🎬",
    layout="wide"
)

# Header
st.title("🎬 VibeMV Studio")
st.markdown("*AI Music Video Timeline Generator*")

# Main layout
col1, col2 = st.columns(2)

with col1:
    st.header("📤 1. Upload Audio")
    audio_file = st.file_uploader("Choose audio file", type=['mp3', 'wav', 'flac', 'ogg'])
    
    if audio_file and st.button("🔍 Analyze Audio", type="primary"):
        with st.spinner("Analyzing audio..."):
            result = analyze_audio(audio_file)
            
            if result:
                st.success("✅ Audio Analysis Complete!")
                st.write(f"**Duration:** {result['duration']:.2f}s | **Tempo:** {result['tempo']:.1f} BPM | **Beats:** {result['beats']}")
                st.write(f"**Suggested scenes:** {len(result['scene_times'])}")
                st.write(f"**Timestamps:** {', '.join([f'{t:.1f}s' for t in result['scene_times'][:8]])}...")
            else:
                st.error("❌ Analysis failed")
    
    st.header("🎨 2. Add Scenes")
    
    prompt = st.text_area("Scene Description", placeholder="E.g., A cartoon bear running through campus...", height=80)
    
    col_start, col_dur = st.columns(2)
    with col_start:
        start = st.number_input("Start Time (s)", min_value=0.0, value=0.0, step=0.1)
    with col_dur:
        duration = st.number_input("Duration (s)", min_value=0.1, value=4.0, step=0.1)
    
    camera = st.selectbox(
        "Camera Motion",
        ["static", "orbit", "zoom_in", "zoom_out", "pan_left", "pan_right", "flythrough"]
    )
    
    if st.button("➕ Add Scene to Timeline", type="primary"):
        add_scene(prompt, start, duration, camera)
        st.success(f"✅ Added Scene {len(st.session_state.scenes)}")
    
    st.header("💾 3. Export")
    
    col_export, col_clear = st.columns(2)
    with col_export:
        if st.button("📥 Export JSON"):
            json_data = export_timeline()
            st.download_button(
                label="💾 Download Timeline",
                data=json_data,
                file_name="vibemv_timeline.json",
                mime="application/json"
            )
    with col_clear:
        if st.button("🗑️ Clear Timeline"):
            clear_timeline()
            st.rerun()

with col2:
    st.header("📽️ Timeline")
    
    if st.session_state.scenes:
        for scene in st.session_state.scenes:
            with st.expander(f"Scene {scene['id']}: {scene['start_time']:.1f}s - {scene['start_time']+scene['duration']:.1f}s"):
                st.write(f"**Prompt:** {scene['prompt']}")
                st.write(f"**Camera:** {scene['camera']}")
                st.write(f"**Duration:** {scene['duration']:.1f}s")
    else:
        st.info("No scenes yet. Add scenes to see them here!")
    
    st.header("📄 JSON Preview")
    
    if st.session_state.scenes:
        json_preview = export_timeline()
        st.code(json_preview, language='json')
    else:
        st.info("Timeline JSON will appear here after adding scenes")

# Info section
with st.expander("ℹ️ About VibeMV Studio"):
    st.markdown("""
    ### 🌟 Features
    - **Audio Beat Detection**: Automatic scene timing from music
    - **Timeline Editor**: Visual scene arrangement
    - **Camera Presets**: Multiple motion options
    - **JSON Export**: Save and reuse timelines
    
    ### 📝 Workflow
    1. Upload audio → Analyze for beats
    2. Add scenes with prompts + camera motions
    3. Review timeline
    4. Export as JSON
    
    ### 🔮 Future Features
    - Video generation with Stable Video Diffusion
    - 3D model integration
    - Frame interpolation
    """)
