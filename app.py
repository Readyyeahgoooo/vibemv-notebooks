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
    
    st.header("💾 3. Export & Generate")
    
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
    
    st.markdown("---")
    
    st.header("🎬 4. Generate Video")
    
    hf_token = st.text_input(
        "HuggingFace Token (Optional - for higher rate limits)",
        type="password",
        help="Get your token at https://huggingface.co/settings/tokens"
    )
    
    if st.button("🚀 Generate Video", type="primary", disabled=not st.session_state.scenes or not audio_file):
        if not st.session_state.scenes:
            st.error("❌ Please add scenes first!")
        elif not audio_file:
            st.error("❌ Please upload audio first!")
        else:
            with st.spinner("🎬 Generating video... This may take a few minutes"):
                try:
                    import tempfile
                    from vibemv.video_generator import VideoGenerator
                    from vibemv.compositor import VideoCompositor
                    
                    # Save audio temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_audio:
                        tmp_audio.write(audio_file.read())
                        audio_path = tmp_audio.name
                    
                    # Initialize generator
                    generator = VideoGenerator(hf_token=hf_token if hf_token else None)
                    compositor = VideoCompositor()
                    
                    # Generate frames for each scene
                    all_scene_frames = []
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, scene in enumerate(st.session_state.scenes):
                        status_text.text(f"Generating scene {idx + 1}/{len(st.session_state.scenes)}...")
                        progress_bar.progress((idx) / len(st.session_state.scenes))
                        
                        frames = generator.generate_scene_frames(scene, fps=24)
                        all_scene_frames.append(frames)
                    
                    status_text.text("Compositing video...")
                    progress_bar.progress(0.9)
                    
                    # Create video
                    output_path = tempfile.mktemp(suffix='.mp4')
                    success = compositor.create_video(all_scene_frames, audio_path, output_path, fps=24)
                    
                    if success:
                        progress_bar.progress(1.0)
                        status_text.text("✅ Video generation complete!")
                        
                        # Provide download
                        with open(output_path, 'rb') as video_file:
                            st.download_button(
                                label="📥 Download Video",
                                data=video_file.read(),
                                file_name="vibemv_output.mp4",
                                mime="video/mp4"
                            )
                        
                        st.success("🎉 Your music video is ready!")
                        
                        # Clean up
                        Path(output_path).unlink()
                        Path(audio_path).unlink()
                    else:
                        st.error("❌ Video generation failed. Check logs.")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    logger.error(f"Video generation error: {e}")
    
    
    if not st.session_state.scenes:
        st.info("ℹ️ Add scenes to your timeline to enable video generation")
    elif not audio_file:
        st.info("ℹ️ Upload audio to enable video generation")


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
