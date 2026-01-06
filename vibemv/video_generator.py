"""
VibeMV Video Generator
Completely free video generation using HuggingFace Inference API and CPU processing
"""

import io
import time
import logging
from typing import List, Dict, Any, Optional
from PIL import Image, ImageOps
import numpy as np
import requests

logger = logging.getLogger(__name__)


class VideoGenerator:
    """Generate videos from timeline using free APIs and CPU processing."""
    
    def __init__(self, hf_token: Optional[str] = None):
        """
        Initialize video generator.
        
        Args:
            hf_token: HuggingFace token for Inference API (optional but recommended)
        """
        self.hf_token = hf_token
        self.api_url = "https://api-inference.huggingface.co/models"
        
        # Free models to use (in order of preference)
        self.image_models = [
            "black-forest-labs/FLUX.1-schnell",  # Fastest
            "stabilityai/stable-diffusion-xl-base-1.0",  # Fallback
        ]
        
        self.max_retries = 3
        self.retry_delay = 2.0
    
    def generate_scene_image(self, prompt: str, width: int = 512, height: int = 512) -> Optional[Image.Image]:
        """
        Generate an image for a scene using HF Inference API.
        
        Args:
            prompt: Text description of the scene
            width: Image width
            height: Image height
            
        Returns:
            PIL Image or None if failed
        """
        for model in self.image_models:
            logger.info(f"Trying model: {model}")
            
            for attempt in range(self.max_retries):
                try:
                    headers = {}
                    if self.hf_token:
                        headers["Authorization"] = f"Bearer {self.hf_token}"
                    
                    # API payload
                    payload = {
                        "inputs": prompt,
                        "parameters": {
                            "width": width,
                            "height": height,
                        }
                    }
                    
                    response = requests.post(
                        f"{self.api_url}/{model}",
                        headers=headers,
                        json=payload,
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        image = Image.open(io.BytesIO(response.content))
                        logger.info(f"Successfully generated image with {model}")
                        return image
                    elif response.status_code == 503:
                        # Model loading
                        logger.warning(f"Model {model} is loading, waiting...")
                        time.sleep(self.retry_delay * (attempt + 1))
                        continue
                    elif response.status_code == 429:
                        # Rate limit
                        logger.warning(f"Rate limit hit, trying next model")
                        break
                    else:
                        logger.warning(f"Failed with status {response.status_code}: {response.text}")
                        break
                        
                except Exception as e:
                    logger.error(f"Error generating image: {e}")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue
                    break
        
        logger.error("All models failed to generate image")
        return None
    
    def apply_camera_motion(
        self,
        image: Image.Image,
        motion: str,
        progress: float
    ) -> Image.Image:
        """
        Apply camera motion effect to an image.
        
        Args:
            image: Input image
            motion: Camera motion type (static, zoom_in, zoom_out, pan_left, pan_right, orbit)
            progress: Motion progress (0.0 to 1.0)
            
        Returns:
            Transformed image
        """
        width, height = image.size
        
        if motion == "static":
            return image
        
        elif motion == "zoom_in":
            # Progressive zoom in
            scale = 1.0 + (0.3 * progress)  # Zoom up to 1.3x
            new_width = int(width * scale)
            new_height = int(height * scale)
            zoomed = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            # Center crop
            left = (new_width - width) // 2
            top = (new_height - height) // 2
            return zoomed.crop((left, top, left + width, top + height))
        
        elif motion == "zoom_out":
            # Progressive zoom out
            scale = 1.3 - (0.3 * progress)  # Zoom from 1.3x to 1.0x
            new_width = int(width * scale)
            new_height = int(height * scale)
            if scale < 1.0:
                # Pad instead of crop
                zoomed = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                result = Image.new('RGB', (width, height), (0, 0, 0))
                left = (width - new_width) // 2
                top = (height - new_height) // 2
                result.paste(zoomed, (left, top))
                return result
            else:
                zoomed = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                left = (new_width - width) // 2
                top = (new_height - height) // 2
                return zoomed.crop((left, top, left + width, top + height))
        
        elif motion == "pan_left":
            # Pan from right to left
            shift = int(width * 0.2 * progress)
            return ImageOps.crop(image, (shift, 0, 0, 0))
        
        elif motion == "pan_right":
            # Pan from left to right
            shift = int(width * 0.2 * progress)
            return ImageOps.crop(image, (0, 0, shift, 0))
        
        elif motion == "orbit":
            # Simulate orbit with zoom + slight rotation
            scale = 1.0 + (0.2 * np.sin(progress * np.pi))
            new_width = int(width * scale)
            new_height = int(height * scale)
            zoomed = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            left = (new_width - width) // 2
            top = (new_height - height) // 2
            return zoomed.crop((left, top, left + width, top + height))
        
        elif motion == "flythrough":
            # Dramatic zoom in
            scale = 1.0 + (0.5 * progress)
            new_width = int(width * scale)
            new_height = int(height * scale)
            zoomed = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            left = (new_width - width) // 2
            top = (new_height - height) // 2
            return zoomed.crop((left, top, left + width, top + height))
        
        return image
    
    def interpolate_frames(
        self,
        frame1: Image.Image,
        frame2: Image.Image,
        num_frames: int = 8
    ) -> List[Image.Image]:
        """
        Simple linear frame interpolation between two images.
        
        Args:
            frame1: Start frame
            frame2: End frame
            num_frames: Number of intermediate frames to generate
            
        Returns:
            List of interpolated frames including start and end
        """
        frames = [frame1]
        
        # Convert to numpy for blending
        arr1 = np.array(frame1).astype(float)
        arr2 = np.array(frame2).astype(float)
        
        for i in range(1, num_frames - 1):
            alpha = i / (num_frames - 1)
            blended = ((1 - alpha) * arr1 + alpha * arr2).astype(np.uint8)
            frames.append(Image.fromarray(blended))
        
        frames.append(frame2)
        return frames
    
    def generate_scene_frames(
        self,
        scene: Dict[str, Any],
        fps: int = 24
    ) -> List[Image.Image]:
        """
        Generate all frames for a single scene.
        
        Args:
            scene: Scene dictionary with prompt, duration, camera motion
            fps: Frames per second
            
        Returns:
            List of PIL Images for the scene
        """
        # Generate base image
        base_image = self.generate_scene_image(scene['prompt'])
        
        if base_image is None:
            # Create fallback black frame with text
            base_image = Image.new('RGB', (512, 512), (0, 0, 0))
        
        # Calculate number of frames
        duration = scene['duration']
        num_frames = int(duration * fps)
        
        # Generate frames with camera motion
        frames = []
        for i in range(num_frames):
            progress = i / max(num_frames - 1, 1)
            frame = self.apply_camera_motion(base_image, scene['camera'], progress)
            frames.append(frame)
        
        return frames
