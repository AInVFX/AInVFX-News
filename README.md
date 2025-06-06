# 🎬 AInVFX-News

<div align="center">
  
  [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AInVFX)
  [![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@AInVFX)
  [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/ainvfx)
  
  **Sources & links related to AInVFX news episodes**
  
</div>

---

## 📅 Episode Archive

### 🎨 June 6, 2025 | Art Direct Every Pixel: NormalCrafter, Any-to-Bokeh, Uni3C & ATI Deep Dive

<details open>
<summary><b>📺 Episode Video & Contents</b></summary>

**🎥 Watch Episode:** [YouTube - ComfyUI Deep Dive Special](https://youtu.be/0cw2N3W7nKo)

> *Join Adrien Toupet for an in-depth exploration of four game-changing research papers that push art direction in video diffusion models. This special episode includes complete ComfyUI workflows and hands-on demonstrations.*

**🔥 TODAY'S HIGHLIGHTS:**
- NormalCrafter - Temporally consistent surface normals for relighting
- Any-to-Bokeh - One-step video bokeh with realistic depth-of-field
- Uni3C - Unified camera and human motion control
- ATI - Draw any trajectory and watch it come to life

#### 1. 🔦 **NormalCrafter: Temporally Consistent Surface Normals**

> *Solving the flickering problem in normal estimation*

| 🔗 **Links** | |
|:---|:---|
| 🌐 **Project Page** | [normalcrafter.github.io](https://normalcrafter.github.io/) |
| 💻 **GitHub** | [Binyr/NormalCrafter](https://github.com/Binyr/NormalCrafter) |
| 📄 **Paper** | [arXiv:2504.11427](https://arxiv.org/abs/2504.11427) |
| 🔧 **ComfyUI** | [AIWarper/ComfyUI-NormalCrafterWrapper](https://github.com/AIWarper/ComfyUI-NormalCrafterWrapper) |
| 📁 **Workflow** | [AInVFX_NormalCrafter.json](https://github.com/AInVFX/AInVFX-News/blob/main/episodes/20250606/AInVFX_NormalCrafter.json) |
| 🎬 **Test Asset** | [Basketball footage](https://github.com/AInVFX/AInVFX-News/blob/main/episodes/20250606/5192157-hd_1920_1080_30fps.mp4) |

**Key Features:**
- Semantic Feature Regularization (SFR) for object understanding
- Two-stage training: latent space → pixel space refinement
- Detail Transfer node for preserving high-frequency information
- Window-based processing for GPU memory efficiency

---

#### 2. 📸 **Any-to-Bokeh: Professional Depth-of-Field Effects**

> *One-step video bokeh without frame-by-frame processing*

| 🔗 **Links** | |
|:---|:---|
| 🌐 **Project Page** | [vivocameraresearch.github.io/any2bokeh](https://vivocameraresearch.github.io/any2bokeh/) |
| 💻 **GitHub** | [vivoCameraResearch/any-to-bokeh](https://github.com/vivoCameraResearch/any-to-bokeh) |
| 📄 **Paper** | [arXiv:2505.21593](https://arxiv.org/abs/2505.21593) |

**Key Innovations:**
- Multi-Plane Image (MPI) guidance for depth understanding
- Controllable focus point and blur strength
- Three-stage training strategy
- Built on Stable Video Diffusion

---

#### 3. 🎬 **Uni3C: Unified Camera & Human Motion Control**

> *Precise 3D-enhanced control for video generation*

| 🔗 **Links** | |
|:---|:---|
| 🌐 **Project Page** | [ewrfcas.github.io/Uni3C](https://ewrfcas.github.io/Uni3C/) |
| 💻 **GitHub** | [ewrfcas/Uni3C](https://github.com/ewrfcas/Uni3C) |
| 📄 **Paper** | [arXiv:2504.14899](https://arxiv.org/abs/2504.14899) |
| 🔧 **ComfyUI** | [kijai/ComfyUI-WanVideoWrapper](https://github.com/kijai/ComfyUI-WanVideoWrapper) |
| 🤗 **Model** | [Wan21_Uni3C_controlnet_fp16.safetensors](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Wan21_Uni3C_controlnet_fp16.safetensors) |
| 📁 **Workflow** | [AInVFX_Uni3C.json](https://github.com/AInVFX/AInVFX-News/blob/main/episodes/20250606/AInVFX_Uni3C.json) |
| 🖼️ **Test Image** | [Waterfall scene](https://github.com/AInVFX/AInVFX-News/blob/main/episodes/20250606/pexels-webbshow-2406455.jpg) |

**Technical Details:**
- PCDController: Plug-and-play point cloud control
- No joint training required
- GeoCalib for natural human positioning
- Compatible with frozen video models

---

#### 4. ✏️ **ATI: Any Trajectory Instruction**

> *Draw trajectories, create realistic motion*

| 🔗 **Links** | |
|:---|:---|
| 🌐 **Project Page** | [anytraj.github.io](https://anytraj.github.io/) |
| 💻 **GitHub** | [bytedance/ATI](https://github.com/bytedance/ATI) |
| 📄 **Paper** | [arXiv:2505.22944](https://arxiv.org/abs/2505.22944) |
| 🤗 **Model** | [Wan2_1-I2V-ATI-14B_fp8_e4m3fn.safetensors](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Wan2_1-I2V-ATI-14B_fp8_e4m3fn.safetensors) |
| 📁 **Workflows** | [ATI Basic](https://github.com/AInVFX/AInVFX-News/blob/main/episodes/20250606/AInVFX_ATI.json) • [ATI Final](https://github.com/AInVFX/AInVFX-News/blob/main/episodes/20250606/AInVFX_ATI_Final.json) |
| 🖼️ **Test Image** | [Pétanque scene](https://github.com/AInVFX/AInVFX-News/blob/main/episodes/20250606/elderly-friends-playing-petanque.jpg) |

**Control Parameters:**
- Temperature: Motion field focus (0-1000)
- TopK: Number of motion influences
- Start/End Percent: Diffusion stage control
- Supports object motion, deformation, and camera movement

</details>

---

### 🎬 May 28, 2025 | ILM's 50th, Cannes, TechX, SpatialScore, Jenga & AgenticSeek

<details open>
<summary><b>📺 Episode Video & Contents</b></summary>

**🎥 Watch Episode:** [YouTube | ILM's 50th, Cannes, TechX, SpatialScore, Jenga & AgenticSeek](https://youtu.be/ffyLCdJc9B8)

> *Join Adrien Toupet as we celebrate 50 years of Industrial Light & Magic, explore Jafar Panahi's inspiring Palme d'Or win at Cannes, and dive into the latest AI developments transforming the VFX industry.*

**🔥 TODAY'S HIGHLIGHTS:**
- ILM's 50th Anniversary - From that hot Van Nuys warehouse to 15 Oscars
- Cannes 2025 - Iranian director Jafar Panahi wins Palme d'Or for "It Was Just an Accident"
- Cinesite launches TechX - Their ethical GenAI exploration unit
- SpatialScore - New benchmark for testing AI's 3D spatial understanding
- Jenga - Making open source video models 4-10x faster on single GPUs
- agenticSeek - 100% local AI assistant

#### 1. 🎭 **ILM 50th Anniversary Celebration**

> *Five decades of revolutionary visual effects*

| 🔗 **Links** | |
|:---|:---|
| 📰 **Full Article** | [AInVFX Blog Post](https://www.ainvfx.com/blog/ilms-50th-cannes-techx-spatialscore-jenga-and-agenticseek/) |
| 🎬 **Documentary** | [Creating the Impossible](https://www.imdb.com/title/tt1657302/) |
| 📖 **ILM's Story** | [Audacious Start in Empty Warehouse](https://www.ilm.com/ilms-audacious-start-in-an-empty-warehouse-began-50-years-ago/) |
| 🚀 **Dykstraflex** | [The Revolutionary Camera System](https://www.lucasfilm.com/news/lucasfilm-originals-the-dykstraflex/) |
| 👤 **John Dykstra** | [Pioneer Profile](https://mrfeelgood.com/articles/wtf-is-john-dykstra) |
| 📚 **Wikipedia** | [ILM History](https://en.wikipedia.org/wiki/Industrial_Light_%26_Magic) |
| 🎤 **Rob Bredow** | [TED Talk - AI in Star Wars](https://www.youtube.com/watch?v=E3Yo7PULlPs) |
| 📹 **Vintage** | [Original 70s Footage](https://vimeo.com/5494280) |

---

#### 2. 🏆 **Cannes 2025: Jafar Panahi's Triumph**

> *"It Was Just an Accident" wins the Palme d'Or*

| 🔗 **Links** | |
|:---|:---|
| 🎙️ **Interview** | [Quentin Tarantino at Cannes](https://www.festival-cannes.com/en/medialibrary/interview-with-quentin-tarantino/) |
| 📺 **Announcement** | [FRANCE 24 Coverage](https://www.youtube.com/watch?v=bgFB_SH8AU8) |
| 🎬 **Film Clip** | [Official Preview](https://www.youtube.com/watch?v=Sxcrm1FGO9c) |

---

#### 3. 🚀 **Cinesite TechX: Ethical GenAI Initiative**

> *Pioneering responsible AI exploration in VFX*

| 🔗 **Links** | |
|:---|:---|
| 🌐 **TechX Portal** | [cinesite.com/techx](https://cinesite.com/techx/) |
| 🏢 **Company** | [Cinesite Official](https://cinesite.com/) |

---

#### 4. 📐 **SpatialScore: AI's 3D Understanding Benchmark**

> *Measuring how well AI comprehends spatial relationships*

| 🔗 **Links** | |
|:---|:---|
| 🌐 **Project Page** | [haoningwu3639.github.io/SpatialScore](https://haoningwu3639.github.io/SpatialScore/) |
| 📄 **Paper** | [arXiv:2505.17012](https://arxiv.org/abs/2505.17012) |
| 💻 **GitHub** | [haoningwu3639/SpatialScore](https://github.com/haoningwu3639/SpatialScore/) |

---

#### 5. ⚡ **Jenga: Supercharging Video Generation**

> *4-10x speed improvements for open source video models*

| 🔗 **Links** | |
|:---|:---|
| 🌐 **Project Page** | [julianjuaner.github.io/projects/jenga](https://julianjuaner.github.io/projects/jenga/) |
| 📄 **Paper** | [arXiv:2505.16864](https://arxiv.org/abs/2505.16864) |
| 💻 **GitHub** | [dvlab-research/Jenga](https://github.com/dvlab-research/Jenga/) |

---

#### 6. 🤖 **agenticSeek: 100% Local AI Assistant**

> *Privacy-first AI assistant running entirely on your machine*

| 🔗 **Links** | |
|:---|:---|
| 💻 **GitHub** | [Fosowl/agenticSeek](https://github.com/Fosowl/agenticSeek) |

</details>

---

## 📢 Stay Connected

<div align="center">
  
  **Follow AInVFX for more AI/VFX updates!**
  
  [![Website](https://img.shields.io/badge/Website-ainvfx.com-blue?style=social)](https://www.ainvfx.com)
  [![YouTube](https://img.shields.io/youtube/channel/subscribers/UCz3nVz4K5HKcXxJRkjhFTlA?style=social&label=Subscribe)](https://www.youtube.com/@AInVFX)
  [![LinkedIn](https://img.shields.io/badge/LinkedIn-Follow-blue?style=social&logo=linkedin)](https://www.linkedin.com/company/ainvfx)
  [![Instagram](https://img.shields.io/badge/Instagram-Follow-E4405F?style=social&logo=instagram)](https://www.instagram.com/ainvfxcom)
  [![Facebook](https://img.shields.io/badge/Facebook-Like-1877F2?style=social&logo=facebook)](https://www.facebook.com/ainvfxcom)
  [![TikTok](https://img.shields.io/badge/TikTok-Follow-black?style=social&logo=tiktok)](https://www.tiktok.com/@ainvfxcom)
  [![GitHub](https://img.shields.io/github/followers/AInVFX?style=social)](https://github.com/AInVFX)
  
</div>

---

<div align="center">
  
  📅 **Last Updated:** June 6, 2025 | 📺 **Latest Episode:** June 6, 2025
  
  ⭐ **If you find this helpful, please star this repository!**
  
  ---
  
  **💡 About AInVFX News**
  
  *Led by Adrien Toupet (former Head of Effects at Wētā FX), AInVFX bridges the gap between cutting-edge AI research and practical VFX applications.*
  
</div>




