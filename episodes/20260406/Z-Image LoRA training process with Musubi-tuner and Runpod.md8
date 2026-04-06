# Z-Image LoRA Training Guide (Musubi-Tuner / H100)

---

### Step 1 — RunPod pod setup

Use the **RunPod PyTorch template**. You need:
- H100 SXM
- Container: `Runpod Pytorch 2.8.0 - runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404`
- Disk: 200GB /workspace volume
- Open port 6006

In the pod terminal:

```bash
# Verify GPU
nvidia-smi

# Clone Musubi
cd /workspace
git clone https://github.com/kohya-ss/musubi-tuner
cd musubi-tuner

# Install dependencies
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu130
pip install -e .
pip install ascii-magic matplotlib tensorboard nano huggingface_hub hf_transfer torch-optimi

# Install FlashAttention for H100 (much faster than sdpa)
pip install flash-attn --no-build-isolation
```

---

### Step 2 — Configure Accelerate

Run this once. Answer each question as shown:

```bash
accelerate config
```

```
In which compute environment are you running?  → This machine
Which type of machine are you using?           → No distributed training
Do you want to run your training on CPU only?  → NO
Do you wish to optimize with torch dynamo?     → NO
Do you want to use DeepSpeed?                  → NO
What GPU(s) should be used?                    → all
Would you like to enable numa efficiency?      → NO
Do you wish to use mixed precision?            → bf16
```

---

### Step 3 — Download models

```bash
mkdir -p /workspace/models
cd /workspace/models

# Download Z-Image Base DiT
python -c "
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='Comfy-Org/z_image',
    local_dir='/workspace/models/z_image',
    allow_patterns=['*.safetensors']
)"
```

---

### Step 4 — Dataset preparation

```bash
mkdir -p /workspace/dataset/ink_artwork
mkdir -p /workspace/cache/ink_lora
```

Put your images here in any mix of 16:9 and 9:16. Supported formats: `.jpg`, `.png`, `.webp`. No pre-resizing needed.

For each image, create a matching `.txt` caption file with the **same filename**:

```
ink_001.jpg   →   ink_001.txt
ink_002.jpg   →   ink_002.txt
```

**File upload**

On your local machine, compress and upload the images:
```bash
tar -I pigz -cvf dataset.gz to_caption
scp -P <your_port> -i <path_to_your_key> dataset.gz root@<remote_ip_or_hostname>:/workspace/dataset/ink_artwork/
```

On the pod, uncompress them:
```bash
cd /workspace/dataset/ink_artwork
tar -xzf dataset.gz
mv to_caption/* .
rm -rf to_caption
rm dataset.gz
```

**Caption strategy** → see caption.py

**Captioning language.** Z-Image was trained on multilingual data. If your subject matter has stronger visual associations in a language other than English within the training data, adding captions in that language alongside English can significantly improve style adherence. For example, bilingual captions work well for subjects with rich non-English visual traditions:

```
A standing figure drawn with sparse brushstrokes, white background. 站立的人物，笔触稀疏，白色背景。
```

**Trigger word placement and format.** Community testing found that double-quoted strings activate differently in this model. Do NOT put your trigger word in quotes. Put it at the very start of the caption in natural sentence position, not comma-separated:

```
In the style of Suiboku, a standing figure with arms at sides   ← correct
Suiboku, standing figure, arms at sides                         ← worse (comma-list format)
"Suiboku" a standing figure                                     ← avoid quotes
```

**The concept bleed principle.** Community testing confirmed: leaving things out of the training captions is essentially deliberate concept bleed — the model learns that uncaptioned elements should apply everywhere without being explicitly prompted. This validates a targeted caption strategy. Whatever you don't caption in your training images gets baked into the trigger word. As a general rule, don't caption the core style elements you want embedded — things like medium, texture, and overall aesthetic treatment.

**Caption variety matters more than length for Z-Image.** Analysis of Z-Image's training confirmed it was trained on five different caption styles (short word tags, short natural language, long natural language, in multiple languages). You don't need to perfectly replicate this — but having a mix of short (5–10 word) and longer (30–50 word) captions for different images in your dataset improves LoRA generalization significantly. Don't write identically structured captions for every image.

---

### Step 5 — Dataset TOML

Create `/workspace/dataset.toml`:

```toml
[general]
resolution = [1024, 576]
caption_extension = ".txt"
batch_size = 4
enable_bucket = true
bucket_no_upscale = false

[[datasets]]
image_directory = "/workspace/dataset/ink_artwork"
cache_directory = "/workspace/cache/ink_lora"
num_repeats = 1
```

`resolution = [1024, 576]` is `[width, height]`. This is your training resolution. The bucketing system will auto-create portrait buckets for your 9:16 images.

`bucket_no_upscale = false` — this allows upscaling images that are smaller than the bucket target. If all your images are high-resolution, they'll only ever be downscaled, so this setting has no practical effect on those datasets.

---

### Step 6 — Sample prompt file

Create `/workspace/sample_prompts.txt`:

```
In the style of Suiboku, a Canadian rocky cliff face covered in snow, a single icicle hanging from the overhang, negative space, minimal brushwork --n photorealistic, photograph, noise, grain, blurry --w 1024 --h 576 --fs 2.0 --s 25 --d 42 --l 4
In the style of Suiboku, a standing figure, minimal lines, large empty space, white background --n photorealistic, photograph --w 1024 --h 576 --fs 2.0 --s 25 --d 42 --l 4
```

The flags per prompt line:
- `--n` : negative prompt
- `--w` / `--h` : width / height
- `--fs` : flow shift (use `2.0` for Z-Image Base)
- `--s` : inference steps (25 for Base with CFG)
- `--d` : seed
- `--l` : CFG scale (`4.0` is the official default for Z-Image Base)

---

### Step 7 — Pre-cache latents

```bash
cd /workspace/musubi-tuner

python src/musubi_tuner/zimage_cache_latents.py \
    --dataset_config /workspace/dataset.toml \
    --vae /workspace/models/z_image/split_files/vae/ae.safetensors
```

This processes every image in your dataset, encodes it through the VAE, and saves the latent tensor next to the image (in the `cache_directory`). Must complete without errors before proceeding.

---

### Step 8 — Pre-cache text encoder outputs

```bash
python src/musubi_tuner/zimage_cache_text_encoder_outputs.py \
    --dataset_config /workspace/dataset.toml \
    --text_encoder /workspace/models/z_image/split_files/text_encoders/qwen_3_4b.safetensors \
    --batch_size 16
```

This reads every `.txt` caption, runs it through Qwen3, and caches the embeddings. `--batch_size 16` is fine on H100 80GB. On H100 this step is very fast.

Both cache steps write `.npz` files into your `cache_directory`. Do not delete that folder during training.

---

### Step 9 — Training command

Calculate your `--max_train_epochs` first as below. Example for 73 images at batch size 4 targeting ~4000 steps: `210 epochs`.

```
ceil(73 ÷ 4) = 19 steps per epoch
4,000 ÷ 19 = 210 epochs
```

Do not commit to a fixed stopping point upfront. The empirical community sweet spot is 3,750–4,000 steps. Style LoRAs are harder to read than character LoRAs and the correct stopping point depends on your specific dataset density.

Multiple community members independently converged on 3,750–4,000 steps as a general target, with one noting immediately after testing that even that range could be overcooked depending on the dataset. These measurements were primarily on **Z-Image Turbo** (distilled). Z-Image **Base** is undistilled and trains more cleanly — the sweet spot may shift, and some Base LoRAs have shown good results as early as 900 steps with the right optimizer.

**The overtraining signal:** prompt a generic subject that has nothing to do with your training images — if your style appears without the trigger word, you have overtrained. If changing the seed gives you the exact same composition, that's also overtraining.

**Use these settings:**

```bash
accelerate launch \
    --num_cpu_threads_per_process 1 \
    --mixed_precision bf16 \
    src/musubi_tuner/zimage_train_network.py \
    --dit /workspace/models/z_image/split_files/diffusion_models/z_image_bf16.safetensors \
    --vae /workspace/models/z_image/split_files/vae/ae.safetensors \
    --text_encoder /workspace/models/z_image/split_files/text_encoders/qwen_3_4b.safetensors \
    --dataset_config /workspace/dataset.toml \
    --flash_attn \
    --mixed_precision bf16 \
    --timestep_sampling logsnr \
    --logit_mean -6.0 \
    --logit_std 2.0 \
    --optimizer_type optimi.AdamW \
    --optimizer_args "betas=[0.9,0.99]" "weight_decay=0.01" "eps=1e-8" \
    --learning_rate 1e-4 \
    --gradient_checkpointing \
    --max_data_loader_n_workers 2 \
    --persistent_data_loader_workers \
    --network_module networks.lora_zimage \
    --network_dim 32 \
    --network_alpha 16 \
    --max_train_epochs 210 \
    --save_every_n_epochs 10 \
    --sample_every_n_epochs 10 \
    --sample_at_first \
    --sample_prompts /workspace/sample_prompts.txt \
    --seed 42 \
    --log_with tensorboard \
    --logging_dir /workspace/logs \
    --output_dir /workspace/output \
    --output_name suiboku_ink
```

**Parameter notes:**

- `--flash_attn` — use this instead of `--sdpa` on H100, it's significantly faster. Requires the `flash-attn` install from Step 1.
- `--network_dim 32` — rank 32. This is the documented default for Z-Image.
- `--network_alpha 16` — alpha = dim/2 is standard convention (not in the docs example but is an inherited kohya parameter).
- `--gradient_checkpointing` — keep this even on H100. It lets you use batch_size 4 comfortably and costs ~10% speed.
- `--sample_at_first` — generates a sample image at epoch 0 (before any training), giving you a baseline to compare against.
- `--save_every_n_epochs 10` — saves a checkpoint every 10 epochs. With 210 epochs that's 21 checkpoints. Adjust if you want fewer.
- No `--fp8_base`, no `--blocks_to_swap`, no `--fp8_llm` — with 80GB VRAM these are unnecessary.
- `--optimizer_type optimi.AdamW` — Community testing confirmed that `adamw8bit` fails for BF16 Z-Image because small gradient updates are zeroed out in the low-precision arithmetic. This has been documented with reference to optimizer precision literature, and practically: one user achieved excellent results at 900 steps using a pipeline that defaults to `optimi.AdamW` (a Kahan-summation optimizer), versus needing 3,000+ steps with `adamw8bit` and still requiring 2.15x LoRA strength at inference to compensate. That 2.15x-strength workaround is a symptom of the precision issue, not a fixed property of Base→Turbo transfer.
  If `optimi.AdamW` fails to load (you'll get an immediate error on startup), fall back to `--optimizer_type prodigy` which also has stochastic rounding. If that also fails, use `--optimizer_type adamw8bit` — it will work, just less efficiently, and your LoRA may need higher strength on inference.
- `--timestep_sampling logsnr` — The `logsnr` timestep sampler is specifically designed for style learning, distinct from the default `shift` sampler. It focuses training on high-noise regions where global style information lives, which is exactly what you want for aesthetic/style LoRAs rather than fine character detail.

**What to watch in the loss output:**

The initial loss will be around `0.4–0.6`. A healthy style LoRA typically shows the loss dropping to `0.02–0.05` and then plateauing. If it drops below `0.01` and keeps falling, you're overtraining. Check your samples at the 50%, 75%, and 100% epoch marks.

**Monitoring loss with TensorBoard (visual loss curve)**

Open a second RunPod terminal and run:
```bash
tensorboard --logdir /workspace/logs --port 6006 --bind_all
```

Then check your sample images. The `--sample_every_n_epochs` flag generates sample images at regular intervals. These are your most honest quality signal. Compare them against the baseline (the `--sample_at_first` image). The loss number tells you the mathematical direction; the sample images tell you if you're actually learning the right thing.

**Downloading sample files locally:**
```bash
scp -P <your_port> -i <path_to_your_key> "root@<remote_ip_or_hostname>:/workspace/output/sample/*.png" .
```

**Downloading sample files & LoRA checkpoints locally (skips already-downloaded files):**
```bash
rsync -avP -e "ssh -p <your_port> -i <path_to_your_key>" root@<remote_ip_or_hostname>:/workspace/output/ .
```

---

### Step 10 — Convert LoRA for ComfyUI

This step is **mandatory**. Z-Image LoRAs from Musubi are in Musubi's internal format and will not load directly in ComfyUI.

```bash
python src/musubi_tuner/networks/convert_z_image_lora_to_comfy.py \
    /workspace/output/suiboku_ink.safetensors \
    /workspace/output/suiboku_ink_comfy.safetensors
```

`--target other` = Diffusers format, which is what ComfyUI expects. Copy `suiboku_ink_comfy.safetensors` to your ComfyUI `models/loras/` folder.

---

### Step 11 — Test inference via Musubi before moving to ComfyUI

Verify the LoRA works before downloading it:

```bash
python src/musubi_tuner/zimage_generate_image.py \
    --dit /workspace/models/z_image/split_files/diffusion_models/z_image_bf16.safetensors \
    --vae /workspace/models/z_image/split_files/vae/ae.safetensors \
    --text_encoder /workspace/models/z_image/split_files/text_encoders/qwen_3_4b.safetensors \
    --prompt "In the style of Suiboku, a Canadian rocky cliff face covered in snow, a single icicle hanging from an overhang, negative space, minimal brushwork" \
    --image_size 1024 576 \
    --infer_steps 25 \
    --flow_shift 2.0 \
    --guidance_scale 4.0 \
    --attn_mode torch \
    --save_path /workspace/output/test \
    --seed 42 \
    --lora_weight /workspace/output/suiboku_ink.safetensors \
    --lora_multiplier 1.0
```

Note: use the **Musubi-format** LoRA (not the `_comfy` converted one) for Musubi inference. Use the converted `_comfy` file only in ComfyUI.

---

### Step 12 — ComfyUI

**Mixing LoRAs at inference.** Community testing confirmed that combining a character LoRA with a style LoRA in Z-Image leads to quality collapse, similar to issues seen with Flux distilled. For most workflows this means: use your style LoRA alone for initial generation. If you later need to stack a character LoRA, test them separately first — they may need to be merged at the weight level rather than stacked at inference.

**Trigger word placement in ComfyUI.** Community testing found that style LoRAs work best when the trigger word is in the *system prompt* position of the Qwen3 chat template (when using the Z-Image ComfyUI nodes). In ComfyUI with the standard Z-Image workflow, put your trigger word at the start of the prompt string. Do not place it in a separate system prompt field.
