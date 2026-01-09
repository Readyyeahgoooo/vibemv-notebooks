# 📓 VibeFrame Colab Notebooks

Optimized Jupyter notebooks for running VibeFrame on Google Colab free tier.

## 📁 Available Notebooks

| Notebook | Description | Best For |
|----------|-------------|----------|
| `VibeFrame_Colab_Optimized.ipynb` | Full-featured notebook with memory optimization | Complete music video projects |
| `VibeFrame_Quick_Start.ipynb` | Simple quick-start guide | First-time users |

## 🚀 Quick Start

1. Open [Google Colab](https://colab.research.google.com)
2. Click **File → Open notebook**
3. Select **GitHub** tab
4. Enter: `Readyyeahgoooo/vibemv-notebooks`
5. Open the notebook you want to use
6. Click **Runtime → Run all** (or run cells one by one)

## 📋 Notebook Features

### VibeFrame_Colab_Optimized.ipynb
- ✅ Memory-efficient CogVideoX-2B generation
- ✅ Google Drive integration
- ✅ Automatic memory cleanup
- ✅ Progress tracking
- ✅ Smart transitions (optional)
- ✅ Final video assembly

### VibeFrame_Quick_Start.ipynb
- ✅ Simple setup
- ✅ Basic video generation
- ✅ Easy customization
- ✅ Minimal configuration

## 💾 Storage Location

All generated videos are saved to:
```
/content/drive/MyDrive/VibeFrame_Output/
├── clips/          # Individual video clips
└── vibemv_final_*.mp4  # Final assembled video
```

## ⚙️ Recommended Settings

For Google Colab Free Tier (T4 GPU):

| Setting | Value | Notes |
|---------|-------|-------|
| Model | CogVideoX-2B | 5B requires Pro |
| Resolution | 480x720 | Lower = faster |
| Steps | 20-25 | Higher = better quality |
| Frames | 49 | ~6 seconds at 8fps |
| FPS | 8 | Lower = longer videos |

## 🐛 Troubleshooting

### CUDA Out of Memory
```python
# Reduce these settings in the notebook:
num_inference_steps = 20  # Lower from 25
video_height = 360        # Lower from 480
video_width = 540         # Lower from 720
```

### Colab Disconnects
- Save clips to Drive frequently
- Use lower settings for longer runs
- Keep browser tab active

### Slow Generation
- Reduce `num_frames` to 32
- Lower `num_inference_steps` to 15
- Use 540x360 resolution

## 📚 Resources

- [Main Project](https://github.com/Readyyeahgoooo/vibemv-notebooks)
- [CogVideoX Documentation](https://huggingface.co/docs/diffusers/api/pipelines/cogvideox)
- [Diffusers Memory Optimization](https://huggingface.co/docs/diffusers/optimization/memory)

## 🤝 Contributing

Contributions welcome! Please open issues or pull requests on GitHub.

## 📝 License

MIT License - see main repository for details.
