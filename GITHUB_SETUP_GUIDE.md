# Setting Up VibeMV Notebooks on Your GitHub

## Step-by-Step Guide

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `vibemv-notebooks`
3. Description: `VibeMV AI Video Generation Notebooks for Google Colab`
4. Set to **Public**
5. Do NOT initialize with README
6. Click **"Create repository"**

---

### Step 2: Push Notebooks to Your GitHub

Open Terminal and run these commands:

```bash
# Navigate to vibemv directory
cd /Users/puiyuenwong/.gemini/antigravity/scratch/vibemv

# Initialize git (if not already)
git init

# Add your GitHub as remote
git remote add github https://github.com/Readyyeahgoooo/vibemv-notebooks.git

# Add all notebook files
git add *.ipynb *.md
git commit -m "Add VibeMV Colab notebooks"

# Push to your GitHub
git push -u github main
```

**Note:** You'll need to enter your GitHub credentials when prompted.

---

### Step 3: Open in Colab

After pushing, use these links:

#### GPU Video Generation
```
https://colab.research.google.com/github/Readyyeahgoooo/vibemv-notebooks/blob/main/VibeMV_GPU_Extension.ipynb
```

#### 3D Model Generation
```
https://colab.research.google.com/github/Readyyeahgoooo/vibemv-notebooks/blob/main/VibeMV_3D_Generator.ipynb
```

---

## Alternative: Quick Upload Method

If you don't want to use command line:

1. Go to https://github.com/Readyyeahgoooo/vibemv-notebooks (after creating repo)
2. Click **"Add file"** → **"Upload files"**
3. Drag and drop these files:
   - `VibeMV_GPU_Extension.ipynb`
   - `VibeMV_3D_Generator.ipynb`
   - `COLAB_INTEGRATION.md`
   - `3D_GENERATION_GUIDE.md`
4. Click **"Commit changes"**

Then use the Colab links above!

---

## When I Update Notebooks

I'll update the files in your HuggingFace Space. You can:

1. Download updated notebooks from HuggingFace
2. Push to your GitHub
3. Colab will automatically use the latest version

Or I can give you a sync script!
