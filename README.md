# VibeMV Studio - AI Music Video Generator

An AI-powered music video creation studio that combines prompt-driven scene generation, 3D model integration, and timeline-based editing.

## 🌟 Features

- **🎨 Prompt-to-Scene**: Generate scenes from text descriptions
- **🖼️ Image Reference**: Upload reference images or AI-generated 3D renders
- **🎬 Timeline Editor**: Visual timeline for scene arrangement
- **🎵 Audio Sync**: Automatic beat detection for scene timing
- **🔄 3D Integration**: Support for external 3D platforms (Meshy, Hexagen, Hyper3D)
- **🎥 Video Generation**: AI-powered video synthesis with frame interpolation

## 🚀 Quick Start

1. Upload your audio file
2. Add scenes with text prompts or reference images
3. Arrange scenes on the timeline
4. Generate and export your music video

## 🛠️ Technology Stack

- **Image Generation**: Stable Diffusion XL, FLUX
- **Video Generation**: Stable Video Diffusion, CogVideoX
- **3D Reconstruction**: TripoSR (HuggingFace compatible)
- **Audio Analysis**: librosa for beat detection
- **UI Framework**: Gradio
- **APIs**: OpenRouter (LLM), HuggingFace Inference

## 📦 External 3D Platforms

VibeMV supports importing 3D model renders from:
- [Meshy AI](https://www.meshy.ai/)
- [Hexagen](https://hexagen.ai/)
- [Hyper3D](https://hyper3d.ai/)

Simply render your 3D model from different angles and upload as reference images.

## 🔑 API Keys

For enhanced functionality, provide:
- **OpenRouter API Key**: For creative scene descriptions
- **HuggingFace Token**: For higher rate limits

## 📝 License

MIT License
