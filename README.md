# 🎬 AInVFX-News

<div align="center">
  
  [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AInVFX)
  [![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@AInVFX)
  [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/ainvfx)
  
  **Sources & links related to AInVFX news episodes**
  
</div>

---

## 📅 Episode Archive

### 🎬 SeedVR2: One-Step Video Restoration Deep Dive | AInVFX July 11

[![SeedVR2: One-Step Video Restoration via Diffusion Adversarial Post-Training](https://img.youtube.com/vi/I0sl45GMqNg/maxresdefault.jpg)](https://youtu.be/I0sl45GMqNg)

> ByteDance's SeedVR2 transforms video upscaling with one-step restoration instead of 15-50. Complete tutorial covering ComfyUI setup, BlockSwap for consumer GPUs, alpha channel workflows, and multi-GPU processing.

**📁 ComfyUI Workflows & Assets:** [episodes/20250711](https://github.com/AInVFX/AInVFX-News/tree/main/episodes/20250711)

**🔗 Resources:**

**SeedVR2 Research:**
- [Project Page](https://iceclear.github.io/projects/seedvr2/) • [SeedVR Paper](https://arxiv.org/abs/2501.01320) • [SeedVR2 Paper](https://arxiv.org/abs/2506.05301)
- [Official GitHub](https://github.com/ByteDance-Seed/SeedVR)

**ComfyUI Implementation:**
- [SeedVR2 Node by NumZ](https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler)
- [CoCoTools IO](https://github.com/Conor-Collins/ComfyUI-CoCoTools_IO)
- [Video Helper Suite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite)

📰 Read the full article: [One-step 4K video upscaling and beyond for free in ComfyUI with SeedVR2]([https://www.ainvfx.com/blog/seedvr2-one-step-video-restoration-deep-dive/](https://www.ainvfx.com/blog/one-step-4k-video-upscaling-and-beyond-for-free-in-comfyui-with-seedvr2/)

---

### 🎬  Speed up WAN 2-3x with MagCache + NAG negative prompting + One-step upscale | AInVFX News June 21

[![Speed Up Video Generation 2-3x: MagCache, NAG, DLoRAL & AI Art Restoration](https://img.youtube.com/vi/YGTUQw9ff4E/maxresdefault.jpg)](https://youtu.be/YGTUQw9ff4E)

> Four practical techniques for faster, better video generation: MagCache accelerates diffusion 2-3x, NAG brings back negative prompting to distilled models, DLoRAL upscales videos in one step, and MIT shows how AI can be use for Art restoration.

**📁 ComfyUI Workflows & Assets:** [episodes/20250621](https://github.com/AInVFX/AInVFX-News/tree/main/episodes/20250621)

**🔗 Resources:**

**MagCache: Fast Video Generation with Magnitude-Aware Cache**
- [Project Page](https://zehong-ma.github.io/MagCache/) • [Paper](https://arxiv.org/abs/2506.09045) • [GitHub](https://github.com/Zehong-Ma/ComfyUI-MagCache)
- [WanVideoWrapper Integration](https://github.com/kijai/ComfyUI-WanVideoWrapper)

**NAG: Normalized Attention Guidance**
- [Project Page](https://chendaryen.github.io/NAG.github.io/) • [Paper](https://arxiv.org/abs/2505.21179) • [GitHub](https://github.com/ChenDarYen/Normalized-Attention-Guidance)
- [Self-Forcing LoRA](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Wan21_T2V_14B_lightx2v_cfg_step_distill_lora_rank32.safetensors)

**DLoRAL: One-Step Video Super-Resolution**
- [Paper](https://arxiv.org/abs/2506.15591) • [GitHub](https://github.com/yjsunnn/DLoRAL) • [Demo Video](https://www.youtube.com/embed/Jsk8zSE3U-w?si=jz1Isdzxt_NqqDFL&vq=hd1080)

**Physical Art Restoration with AI**
- [MIT News](https://news.mit.edu/2025/restoring-damaged-paintings-using-ai-generated-mask-0611) • [Nature Paper](https://www.nature.com/articles/s41586-025-09045-4) • [Nature Video](https://www.nature.com/articles/d41586-025-01836-z)

📰 Read the full article: [Speed Up Video Generation 2-3x: MagCache, NAG, DLoRAL & AI Art Restoration](https://www.ainvfx.com/blog/speed-up-video-generation-2-3x-magcache-nag-dloral-and-ai-art-restoration/)

---

### 🎬 Democratizing AI: train models with 256 NPUs, track through occlusions | AInVFX News June 18

[![ContentV, CoTracker3, Self-Forcing & CBottle](https://img.youtube.com/vi/U6LoN10ZpxU/maxresdefault.jpg)](https://youtu.be/U6LoN10ZpxU)

> Four groundbreaking papers democratizing AI development - from training competitive video models with 256 NPUs to tracking through occlusions, streaming video generation, and climate modeling.

**🔗 Resources:**

**ContentV: Efficient Training of Video Generation Models**
- [Project Page](https://contentv.github.io/) • [Paper](https://arxiv.org/abs/2506.05343) • [GitHub](https://github.com/bytedance/ContentV)

**CoTracker3: Tracking Any Point Through Occlusions**
- [Project Page](https://cotracker3.github.io/) • [Paper](https://arxiv.org/abs/2410.11831) • [GitHub](https://github.com/facebookresearch/co-tracker)
- [ComfyUI Node](https://github.com/s9roll7/comfyui_cotracker_node)
- See our [LEGO DeepDive](https://youtu.be/7YmiJxPEMk0) for CoTracker + ATI workflow

**Self-Forcing: Autoregressive Video Diffusion**
- [Project Page](https://self-forcing.github.io/) • [Paper](https://arxiv.org/abs/2506.08009) • [GitHub](https://github.com/guandeh17/Self-Forcing)

**CBottle: Climate Foundation Model**
- [NVIDIA Earth-2](https://www.nvidia.com/en-us/high-performance-computing/earth-2/) • [Blog](https://blogs.nvidia.com/blog/earth2-generative-ai-foundation-model-global-climate-kernel-scale-resolution/)
- [Paper](https://arxiv.org/abs/2505.06474v1) • [GitHub](https://github.com/NVlabs/cBottle)

📰 Read the full article: [ContentV, CoTracker3, Self-Forcing & CBottle - Democratizing AI Development](https://www.ainvfx.com/blog/contentv-cotracker3-self-forcing-and-cbottle-democratizing-ai-development/)

---

### 🤿 Create your own LEGO animation: complete AI workflow from photo to final shot | AInVFX June 13

[![Create your own LEGO animated shot from scratch: WAN + ATI + CoTracker + SAM2 + VACE](https://img.youtube.com/vi/7YmiJxPEMk0/maxresdefault.jpg)](https://youtu.be/7YmiJxPEMk0)

> Transform a single LEGO photo into a complete animated shot! Join Adrien for an in-depth tutorial combining the latest open-source AI tools to bring our favorite toys to life.

**📁 ComfyUI Workflows & Assets:** [episodes/20250614](https://github.com/AInVFX/AInVFX-News/tree/main/episodes/20250614)

**🔗 Resources:**

**WAN 2.1 + ATI (Any Trajectory Instruction) + VACE + CausVid**
- [ComfyUI WANVideoWrapper](https://github.com/kijai/ComfyUI-WanVideoWrapper)
- [WAN, ATI, VACE, CausVid Models](https://huggingface.co/Kijai/WanVideo_comfy/tree/main)
- [WAN BF16 Models](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/tree/main/split_files/diffusion_models)

**CoTracker**
- [Research Paper](https://github.com/facebookresearch/co-tracker)
- [ComfyUI CoTracker Node](https://github.com/s9roll7/comfyui_cotracker_node)

**SAM2 (Segment Anything 2)**
- [Official GitHub](https://github.com/facebookresearch/segment-anything-2)
- [ComfyUI Implementation](https://github.com/kijai/ComfyUI-segment-anything-2)

**Additional Resources:**
- [KJ Nodes](https://github.com/kijai/ComfyUI-KJNodes)
- [Video Helper Suite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite)

📰 Read the full article: [LEGO Animation DeepDive: WAN + ATI + CoTracker + SAM2 + VACE Complete Workflow](https://www.ainvfx.com/blog/lego-animation-deepdive-wan-ati-cotracker-sam2-vace-complete-workflow/)

---

### 🎬 Master art direction in AI video: normals, bokeh, camera control & trajectories | AInVFX June 6

[![Art direct Wan 2.1 ComfyUI - ATI, Uni3C, NormalCrafter & Any2Bokeh](https://img.youtube.com/vi/0cw2N3W7nKo/maxresdefault.jpg)](https://youtu.be/0cw2N3W7nKo)

> Learn to art direct Wan 2.1 - Join Adrien for an in-depth ComfyUI tutorial covering four game-changing research papers that enable unprecedented art direction in video diffusion models.

**📁 ComfyUI Workflows & Assets:** [episodes/20250606](https://github.com/AInVFX/AInVFX-News/tree/main/episodes/20250606)

**🔗 Resources:**

**NormalCrafter: Learning Temporally Consistent Normals from Video Diffusion Priors**
- [Project Page](https://normalcrafter.github.io/) • [GitHub](https://github.com/Binyr/NormalCrafter) • [Paper](https://arxiv.org/abs/2504.11427)
- [ComfyUI Wrapper](https://github.com/AIWarper/ComfyUI-NormalCrafterWrapper)
- [ComfyUI Workflow](https://github.com/AInVFX/AInVFX-News/blob/main/episodes/20250606/AInVFX_NormalCrafter.json) • [Input Video](https://github.com/AInVFX/AInVFX-News/blob/main/episodes/20250606/5192157-hd_1920_1080_30fps.mp4)

**Any-to-Bokeh: One-Step Video Bokeh via Multi-Plane Image Guided Diffusion**
- [Project Page](https://vivocameraresearch.github.io/any2bokeh/) • [GitHub](https://github.com/vivoCameraResearch/any-to-bokeh) • [Paper](https://arxiv.org/abs/2505.21593)

**Uni3C: Unifying Precisely 3D-Enhanced Camera and Human Motion Controls for Video Generation**
- [Project Page](https://ewrfcas.github.io/Uni3C/) • [GitHub](https://github.com/ewrfcas/Uni3C) • [Paper](https://arxiv.org/abs/2504.14899)
- [ComfyUI Wrapper](https://github.com/kijai/ComfyUI-WanVideoWrapper) • [Model](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Wan21_Uni3C_controlnet_fp16.safetensors) • [CausVid LoRA (optional)](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors)
- [ComfyUI Workflow](https://github.com/AInVFX/AInVFX-News/blob/main/episodes/20250606/AInVFX_Uni3C.json) • [Input Image](https://github.com/AInVFX/AInVFX-News/blob/main/episodes/20250606/pexels-webbshow-2406455.jpg) • [3D Cube](https://github.com/AInVFX/AInVFX-News/blob/main/episodes/20250606/cube.obj)

**ATI: Any Trajectory Instruction for Controllable Video Generation**
- [Project Page](https://anytraj.github.io/) • [GitHub](https://github.com/bytedance/ATI) • [Paper](https://arxiv.org/abs/2505.22944)
- [Model](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Wan2_1-I2V-ATI-14B_fp8_e4m3fn.safetensors)
- [ComfyUI Workflow (Start)](https://github.com/AInVFX/AInVFX-News/blob/main/episodes/20250606/AInVFX_ATI.json) • [ComfyUI Workflow (Final)](https://github.com/AInVFX/AInVFX-News/blob/main/episodes/20250606/AInVFX_ATI_Final.json) • [Input Image](https://github.com/AInVFX/AInVFX-News/blob/main/episodes/20250606/elderly-friends-playing-petanque.jpg)

📰 Read the full article: [Art direct Wan 2.1 ComfyUI - ATI, Uni3C, NormalCrafter & Any2Bokeh](https://www.ainvfx.com/blog/art-direct-wan2-1-normalcrafter-any-to-bokeh-uni3c-and-ati-deep-dive/)

---

### 🎬 ILM turns 50, Cannes surprises, and AI gets 10x faster | AInVFX News May 28

[![ILM's 50th, Cannes, TechX, SpatialScore, Jenga & AgenticSeek](https://img.youtube.com/vi/ffyLCdJc9B8/maxresdefault.jpg)](https://youtu.be/ffyLCdJc9B8)

> Join Adrien as we celebrate 50 years of Industrial Light & Magic, explore Jafar Panahi's inspiring Palme d'Or win at Cannes, and dive into the latest AI developments transforming the VFX industry.

**🔗 Resources:**

**ILM 50th Anniversary**
- [ILM's Audacious Start](https://www.ilm.com/ilms-audacious-start-in-an-empty-warehouse-began-50-years-ago/) • [Creating the Impossible](https://www.imdb.com/title/tt1657302/)
- [The Dykstraflex](https://www.lucasfilm.com/news/lucasfilm-originals-the-dykstraflex/) • [John Dykstra Profile](https://mrfeelgood.com/articles/wtf-is-john-dykstra)
- [Rob Bredow TED Talk](https://www.youtube.com/watch?v=E3Yo7PULlPs) • [Original 70s Footage](https://vimeo.com/5494280)

**Cannes 2025**
- [Quentin Tarantino Interview](https://www.festival-cannes.com/en/medialibrary/interview-with-quentin-tarantino/)
- [Palme d'Or Announcement](https://www.youtube.com/watch?v=bgFB_SH8AU8) • [Film Clip](https://www.youtube.com/watch?v=Sxcrm1FGO9c)

**Industry & Research**
- **Cinesite TechX:** [Portal](https://cinesite.com/techx/) • [Company](https://cinesite.com/)
- **SpatialScore: Towards Unified Evaluation for Multimodal Spatial Understanding** [Project](https://haoningwu3639.github.io/SpatialScore/) • [Paper](https://arxiv.org/abs/2505.17012) • [GitHub](https://github.com/haoningwu3639/SpatialScore/)
- **Jenga: Training-Free Efficient Video Generation via Dynamic Token Carving** [Project](https://julianjuaner.github.io/projects/jenga/) • [Paper](https://arxiv.org/abs/2505.16864) • [GitHub](https://github.com/dvlab-research/Jenga/)
- **agenticSeek: Private, Local Manus Alternative** [GitHub](https://github.com/Fosowl/agenticSeek)

📰 Read the full article: [ILM's 50th, Cannes, TechX, SpatialScore, Jenga & AgenticSeek](https://www.ainvfx.com/blog/ilms-50th-cannes-techx-spatialscore-jenga-and-agenticseek/)

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
  
  📅 **Last Updated:** June 18, 2025
  
  ⭐ **If you find this helpful, please star this repository!**
  
  ---
  
  **💡 About AInVFX News**
  
  *Led by Adrien Toupet (former Head of Effects at Wētā FX), AInVFX bridges the gap between cutting-edge AI research and practical VFX applications.*
  
</div>
