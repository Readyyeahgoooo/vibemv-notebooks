"""
Video Composition Module
Stitch scene frames into final video with audio
"""

import logging
from typing import List
from PIL import Image
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


class VideoCompositor:
    """Compose final video from scene frames and audio."""
    
    def __init__(self):
        """Initialize video compositor."""
        pass
    
    def create_video(
        self,
        scenes_frames: List[List[Image.Image]],
        audio_path: str,
        output_path: str,
        fps: int = 24
    ) -> bool:
        """
        Create final video from scene frames and audio.
        
        Args:
            scenes_frames: List of frame lists (one per scene)
            audio_path: Path to audio file
            output_path: Output video path
            fps: Frames per second
            
        Returns:
            True if successful
        """
        try:
            from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips
            
            # Create temporary directory for frames
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_path = Path(tmpdir)
                
                # Create video clips for each scene
                scene_clips = []
                
                for scene_idx, frames in enumerate(scenes_frames):
                    logger.info(f"Processing scene {scene_idx + 1}/{len(scenes_frames)}")
                    
                    # Save frames temporarily
                    frame_paths = []
                    for frame_idx, frame in enumerate(frames):
                        frame_path = tmp_path / f"scene_{scene_idx}_frame_{frame_idx:04d}.png"
                        frame.save(frame_path)
                        frame_paths.append(str(frame_path))
                    
                    # Create clip from frames
                    clip = ImageSequenceClip(frame_paths, fps=fps)
                    scene_clips.append(clip)
                
                # Concatenate all scenes
                final_video = concatenate_videoclips(scene_clips, method="compose")
                
                # Add audio
                audio = AudioFileClip(audio_path)
                
                # Trim video to audio length or vice versa
                if final_video.duration > audio.duration:
                    final_video = final_video.subclip(0, audio.duration)
                else:
                    audio = audio.subclip(0, final_video.duration)
                
                final_video = final_video.set_audio(audio)
                
                # Write output
                logger.info(f"Writing video to {output_path}")
                final_video.write_videofile(
                    output_path,
                    fps=fps,
                    codec='libx264',
                    audio_codec='aac',
                    temp_audiofile=str(tmp_path / 'temp-audio.m4a'),
                    remove_temp=True,
                    verbose=False,
                    logger=None
                )
                
                # Clean up
                final_video.close()
                audio.close()
                for clip in scene_clips:
                    clip.close()
                
                logger.info("Video creation complete!")
                return True
                
        except Exception as e:
            logger.error(f"Video creation failed: {e}")
            return False
