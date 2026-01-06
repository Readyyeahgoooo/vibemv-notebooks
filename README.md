---
title: VibeMV Studio
emoji: 🎬
colorFrom: purple
colorTo: pink
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# 🎬 VibeMV Studio - AI Music Video Generator

An AI-powered music video creation studio that combines prompt-driven scene generation, 3D model integration, and timeline-based editing.

## 🌟 Features

- **🎨 Prompt-to-Scene**: Generate scenes from text descriptions
- **🖼️ Image Reference**: Upload reference images or AI-generated 3D renders
- **🎬 Timeline Editor**: Visual timeline for scene arrangement
- **🎵 Audio Sync**: Automatic beat detection for scene timing
- **🔄 3D Integration**: Support for external 3D platforms (Meshy, Hexagen, Hyper3D)
- **🎥 Camera Control**: Multiple camera motion presets

## 🚀 Quick Start

1. Upload your audio file
2. Click "Analyze Audio" for automatic beat detection
3. Add scenes with text prompts or reference images
4. Set camera motion for each scene
5. Arrange scenes on the timeline
6. Export timeline as JSON

## 🛠️ Supported 3D Platforms

VibeMV supports importing 3D model renders from:
- [Meshy AI](https://www.meshy.ai/)
- [Hexagen](https://hexagen.ai/)
- [Hyper3D](https://hyper3d.ai/)

Simply render your 3D model from different angles and upload as reference images.

## 🔑 API Keys (Optional)

For enhanced functionality, you can provide:
- **OpenRouter API Key**: For creative scene descriptions
- **HuggingFace Token**: For higher rate limits

## ⚠️ Current Status

This is an MVP framework. The timeline editor and audio analysis are fully functional. Video generation capabilities will be added with GPU infrastructure.

## 📝 License

MIT License
