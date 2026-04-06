# LTX-V 2.3 LoRA Training — Style LoRA for I2V

## Before You Start — Concerns and Clarifications

### T2V vs I2V: It's One LoRA

LTX-V 2.3 is a single unified model that handles both text-to-video and image-to-video. You train one style LoRA and use it for both modes. For I2V, you pass a keyframe as the first-frame condition in ComfyUI and the style LoRA biases the continuation. Nothing else changes.

### Known LTX 2.3 Color Issue

Community testing confirmed that LTX 2.3 T2V produces washed-out colors for flat 2D/animation styles. **I2V does not have this issue.** If I2V is your primary workflow, this is not a blocker. If you later want to use the LoRA for T2V as well, increasing rank from 32→64 has been reported to help make colors more vibrant.

### Image-Only Dataset for a Video Model

LTX treats images as 1-frame videos. Training on still images works and will teach the style distribution. The base model handles temporal coherence during generation. The LoRA biases the aesthetic, not the motion. This is the right approach for a style LoRA.

### Caption Reuse from a Prior LoRA

If you have existing `.txt` captions from a previous LoRA training run (e.g. Z-Image), they are **fully reusable**. Gemma 3 12B is a multilingual model. The same trigger word, concept-bleed strategy, and bilingual caption format all apply.

### No Conversion Step

Unlike Z-Image (which required a Musubi→ComfyUI conversion step), LTX-V checkpoints from this fork are saved in ComfyUI format by default. The `*.comfy.safetensors` file is dropped in `output/` alongside the original and goes directly into your ComfyUI `models/loras/` folder.

---

## Step 1 — RunPod Pod Setup

Use the **RunPod PyTorch template** (same as Z-Image).

- GPU: H100 SXM (80GB)
- Container: `Runpod Pytorch 2.8.0 - runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404`
- Disk: 200GB network volume (LTX 2.3 model is ~44GB BF16, Gemma is ~24GB unquantized)
- Open port 6006 (TensorBoard)

In the pod terminal:

```bash
# Verify GPU
nvidia-smi

# Clone Musubi — use the ltx-2-dev branch, which has LTX-2.3 support
cd /workspace
git clone --branch ltx-2-dev https://github.com/AkaneTendo25/musubi-tuner
cd musubi-tuner

# Install dependencies
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu130
pip install -e .
pip install ascii-magic matplotlib tensorboard huggingface_hub hf_transfer

# bitsandbytes is required for --gemma_load_in_8bit during text encoder caching
pip install bitsandbytes

# FlashAttention for H100 (significantly faster than sdpa)
pip install flash-attn --no-build-isolation
```

---

## Step 2 — Configure Accelerate

Run once and answer exactly as shown:

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

## Step 3 — Download Models

```bash
mkdir -p /workspace/models/ltx
mkdir -p /workspace/models/gemma

cd /workspace/models

# Download LTX-2.3 BF16 checkpoint (~44GB)
HF_HUB_ENABLE_HF_TRANSFER=1 python -c "
from huggingface_hub import hf_hub_download
hf_hub_download(
    repo_id='Lightricks/LTX-2.3',
    filename='ltx-2.3-22b-dev.safetensors',
    local_dir='/workspace/models/ltx'
)"

# Download Gemma 3 12B text encoder (~24GB in this quantized form, ~12GB in 8-bit at runtime)
HF_HUB_ENABLE_HF_TRANSFER=1 python -c "
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='Lightricks/gemma-3-12b-it-qat-q4_0-unquantized',
    local_dir='/workspace/models/gemma'
)"
```

Verify both downloaded correctly:

```bash
ls /workspace/models/ltx/         # should show ltx-2.3-22b-dev.safetensors
ls /workspace/models/gemma/        # should show model files including tokenizer
```

---

## Step 4 — Dataset Preparation

```bash
mkdir -p /workspace/cache/ink_lora_ltxv
mkdir -p /workspace/dataset/images/
```

If reusing images from a prior pod, skip the upload. If starting fresh:

```bash
# Upload from your local machine
tar -I pigz -cvf dataset.gz to_caption
scp -P <your_port> -i <path_to_your_key> dataset.gz root@<remote_ip>:/workspace/dataset/images/

# Extract on the pod
cd /workspace/dataset/images
tar -xzf dataset.gz
mv to_caption/* .
rm -rf to_caption
rm dataset.gz
```

**Caption reuse:** Existing `.txt` files from a prior LoRA training run are compatible without changes. Gemma 3 12B handles both English and multilingual text. Your trigger word, bilingual caption format, and concept-bleed strategy (not captioning core style elements you want baked into the trigger word) all carry over directly.

---

## Step 5 — Dataset TOML

Create `/workspace/dataset.toml`:

```toml
[general]
resolution = [1024, 576]
caption_extension = ".txt"
batch_size = 1
enable_bucket = true
bucket_no_upscale = false

[[datasets]]
image_directory = "/workspace/dataset/images"
cache_directory = "/workspace/cache/ink_lora_ltxv"
num_repeats = 1
```

**Key differences from Z-Image:**

- `target_frames = [1]` explicitly tells the trainer to use images as single-frame samples.
- `resolution = [1024, 576]` is `[width, height]`. 16:9 images will bucket to 1024×576; 9:16 images will bucket to 576×1024 automatically.
- `bucket_no_upscale = false` allows upscaling images smaller than the bucket target. If all your images are high-resolution, they will only ever be downscaled.
- Use `image_directory` for your image files. Even though LTX-V treats images as 1-frame videos during training, the dataset configuration must use `image_directory` so the dataloader knows to search for image file extensions.

---

## Step 6 — Sample Prompt File

Create `/workspace/sample_prompts.txt` with prompts relevant to your subject matter. Example:

```
In the style of Suiboku, a Canadian rocky cliff face covered in snow, a single icicle hanging from the overhang, negative space, minimal brushwork --n photorealistic, photograph, noise, grain, blurry, watermark --w 1024 --h 576 --f 125 --s 30 --l 4.0 --d 42
In the style of Suiboku, a standing figure, minimal lines, large empty space, white background --n photorealistic, photograph --w 1024 --h 576 --f 125 --s 30 --l 4.0 --d 42
```

**LTX-V prompt flags:**

| Flag | Meaning | Note |
|------|---------|------|
| `--n` | Negative prompt | |
| `--w` / `--h` | Width / Height | Match your training resolution |
| `--f` | Frame count | 125 frames = ~5 seconds at 25 fps |
| `--s` | Inference steps | 30 for the non-distilled BF16 checkpoint |
| `--l` | Guidance scale | 4.0 is standard for LTX-V |
| `--d` | Seed | |

**No `--fs` (flow shift) flag.** LTX-V handles timestep shifting internally via its sampler — there is no flow shift parameter to set in prompts.

---

## Step 7 — Pre-cache Latents

```bash
cd /workspace/musubi-tuner

python src/musubi_tuner/ltx2_cache_latents.py \
    --dataset_config /workspace/dataset.toml \
    --ltx2_checkpoint /workspace/models/ltx/ltx-2.3-22b-dev.safetensors \
    --device cuda \
    --vae_dtype bf16
```

This encodes each image through the LTX VAE and writes `*_ltx2.safetensors` latent files into the cache directory. Must complete without errors before proceeding.

---

## Step 8 — Pre-cache Text Encoder Outputs

```bash
python src/musubi_tuner/ltx2_cache_text_encoder_outputs.py \
    --dataset_config /workspace/dataset.toml \
    --ltx2_checkpoint /workspace/models/ltx/ltx-2.3-22b-dev.safetensors \
    --gemma_root /workspace/models/gemma \
    --gemma_load_in_8bit \
    --device cuda \
    --mixed_precision bf16 \
    --batch_size 4 \
    --precache_sample_prompts \
    --sample_prompts /workspace/sample_prompts.txt
```

**Notes:**

- `--gemma_load_in_8bit` loads the 12B text encoder in 8-bit (~12GB), well within H100's 80GB.
- `--precache_sample_prompts` also caches the sample prompt embeddings, allowing training to generate samples without reloading Gemma at every checkpoint interval. This saves significant time per save interval.
- Output files are `*_ltx2_te.safetensors` in the cache directory.

---

## Step 9 — Training Command

**Calculate epochs first:**

```
<dataset_size> images ÷ batch_size 1 = <dataset_size> steps per epoch
Target: 2000–3000 steps
ceil(2500 ÷ <dataset_size>) = N epochs
```

The sweet spot for style LoRAs on LTX-V is reported between 1500–3000 steps. With a clean dataset and good captions, start conservative. The same overtraining signal as Z-Image applies: if the style appears in a generic prompt without your trigger word, you've overshot.

Training a highly textural style on a video model requires balancing detail retention against the model's structural logic. Below are two iterations of the training command, demonstrating the shift from an experimental baseline to a refined, texture-focused run.

### Version 1: The Experimental HFATO Baseline

This initial run uses the experimental High-Frequency Awareness Training Objective (HFATO) to force the model to reconstruct degraded images.

**Loss Expectation:** Because HFATO uses an `x0-prediction` loss rather than standard velocity loss, the loss curve will plateau much higher (~0.30–0.35). While conceptually designed to prevent video models from losing high-frequency details when trained purely on static images, the artificial spatial degradation may inadvertently wash out extremely delicate textural details like fine brushstrokes.

```bash
accelerate launch \
    --num_cpu_threads_per_process 1 \
    --mixed_precision bf16 \
    src/musubi_tuner/ltx2_train_network.py \
    --mixed_precision bf16 \
    --dataset_config /workspace/dataset.toml \
    --ltx2_checkpoint /workspace/models/ltx/ltx-2.3-22b-dev.safetensors \
    --ltx_version 2.3 \
    --ltx_version_check_mode error \
    --flash_attn \
    --fp8_base \
    --fp8_scaled \
    --gradient_checkpointing \
    --max_data_loader_n_workers 2 \
    --persistent_data_loader_workers \
    --network_module networks.lora_ltx2 \
    --network_dim 32 \
    --network_alpha 32 \
    --network_args "include_patterns=['.*\.to_k$','.*\.to_q$','.*\.to_v$','.*\.to_out\.0$','.*\.ff\.net\.0\.proj$','.*\.ff\.net\.2$']" \
    --hfato \
    --hfato_args scale_factor=0.5 \
    --timestep_sampling shifted_logit_normal \
    --learning_rate 1e-4 \
    --optimizer_type AdamW8bit \
    --lr_scheduler constant_with_warmup \
    --lr_warmup_steps 10 \
    --max_train_epochs 40 \
    --save_every_n_epochs 5 \
    --sample_at_first \
    --sample_every_n_epochs 5 \
    --sample_prompts /workspace/sample_prompts.txt \
    --use_precached_sample_prompts \
    --sample_with_offloading \
    --sample_tiled_vae \
    --sample_vae_tile_size 512 \
    --sample_vae_temporal_tile_size 48 \
    --seed 42 \
    --log_with tensorboard \
    --logging_dir /workspace/logs \
    --output_dir /workspace/output \
    --output_name my_style_ltxv \
    --save_checkpoint_metadata
```

---

### Version 2: The Balanced Texture-Focused Run (Recommended)

This refined run abandons HFATO to return to standard velocity loss. It increases LoRA capacity to capture complex textures, smooths optimizer updates via gradient accumulation, and forces the timestep sampler to explicitly spend 30% of its time learning fine, low-noise details (confirmed via upstream community testing).

**Adjusted Epoch Math & Early Stopping:**
Because gradients are accumulated over 4 steps, the number of optimization steps per epoch changes significantly:
- `<dataset_size>` images ÷ batch_size 1 = `<dataset_size>` forward passes per epoch
- `<dataset_size>` passes ÷ 4 gradient accumulation steps = ~`<N>` optimization steps per epoch
- **The sweet spot:** With Rank 64 targeting all FFN layers, the model typically learns the dataset fully between steps 1,000 and 1,500. Pushing beyond this causes `grad_norm` to destabilize as the optimizer overfits.
- To safely capture this window, set `--max_train_epochs 100` and save every 10 epochs.

```bash
accelerate launch \
    --num_cpu_threads_per_process 1 \
    --mixed_precision bf16 \
    src/musubi_tuner/ltx2_train_network.py \
    --mixed_precision bf16 \
    --dataset_config /workspace/dataset.toml \
    --ltx2_checkpoint /workspace/models/ltx/ltx-2.3-22b-dev.safetensors \
    --ltx_version 2.3 \
    --ltx_version_check_mode error \
    --flash_attn \
    --fp8_base \
    --fp8_scaled \
    --gradient_checkpointing \
    --gradient_accumulation_steps 4 \
    --max_data_loader_n_workers 2 \
    --persistent_data_loader_workers \
    --network_module networks.lora_ltx2 \
    --network_dim 64 \
    --network_alpha 64 \
    --network_args "include_patterns=['.*\.to_k$','.*\.to_q$','.*\.to_v$','.*\.to_out\.0$','.*\.ff\.net\.0\.proj$','.*\.ff\.net\.2$']" \
    --timestep_sampling shifted_logit_normal \
    --shifted_logit_uniform_prob 0.30 \
    --learning_rate 6e-5 \
    --optimizer_type AdamW8bit \
    --lr_scheduler constant_with_warmup \
    --lr_warmup_steps 10 \
    --caption_dropout_rate 0.1 \
    --max_train_epochs 100 \
    --save_every_n_epochs 10 \
    --sample_at_first \
    --sample_every_n_epochs 10 \
    --sample_prompts /workspace/sample_prompts.txt \
    --use_precached_sample_prompts \
    --sample_with_offloading \
    --sample_tiled_vae \
    --sample_vae_tile_size 512 \
    --sample_vae_temporal_tile_size 48 \
    --seed 42 \
    --log_with tensorboard \
    --logging_dir /workspace/logs \
    --output_dir /workspace/output \
    --output_name my_style_ltxv_balanced \
    --save_checkpoint_metadata
```

---

### Parameter Dictionary & Monitoring Notes

**Monitoring the Loss & Gradient Norm:**
- **The "Sawtooth" Loss Curve:** With `--shifted_logit_uniform_prob 0.30`, the loss curve will look highly unstable, rhythmically jumping up and down. This is expected — it is the visual signature of the dataloader bouncing between high-noise (structural) batches and low-noise (texture) batches.
- **Watch `grad_norm/video`:** The most critical chart to watch is the Gradient Norm. As long as it stays compressed (e.g., oscillating tightly around 0.02–0.03), the model is learning safely. If `grad_norm` begins a sustained upward climb (spiking to 0.05+), the optimizer is taking unstable steps and the model is beginning to overfit. Your best checkpoint is usually right before this climb begins.

**Core Architecture & Memory**
- `--ltx_version 2.3` — Required. Sets correct metadata in the LoRA output and enables the stretched `shifted_logit_normal` sampler (v2.3 default).
- `--fp8_base --fp8_scaled` — Quantizes the 44GB BF16 checkpoint to ~22GB FP8 on the fly. The BF16 checkpoint is the upstream-recommended training base.
- `--use_precached_sample_prompts` — Uses the Gemma embeddings cached in Step 8 so Gemma does not reload during training, saving VRAM.

**LoRA Targeting & Capacity**
- `--network_args "include_patterns=..."` — Manually targets both Attention and Feed-Forward Network (FFN) layers without triggering the IC-LoRA `v2v` strategy. Targeting FFN layers is strongly recommended by community testing for better style and detail retention. Custom `include_patterns` override any preset.
- `--network_dim 64 --network_alpha 64` *(Version 2)* — Higher rank gives the model more capacity to imprint complex textures. Community testing indicates this helps resolve washed-out colors at inference.

**Learning Objectives & Timesteps**
- `--timestep_sampling shifted_logit_normal` — The correct sampler for LTX 2.3.
- `--shifted_logit_uniform_prob 0.30` *(Version 2)* — Forces 30% of steps to be drawn uniformly from low-noise levels instead of the default 10%. This ensures the model learns fine textural details rather than only structural information.

**Optimization & Stability**
- `--gradient_accumulation_steps 4` *(Version 2)* — Accumulating 4 steps before updating weights smooths the `grad_norm` for stable learning, preventing violent parameter swings.
- `--learning_rate 6e-5` *(Version 2)* — Community-validated rate for LTX 2.3; stabilizes the heavier FFN layer training.
- `--caption_dropout_rate 0.1` *(Version 2)* — Drops text conditioning 10% of the time. This trains the model to generate without text guidance, enabling Classifier-Free Guidance (CFG) to work properly at inference.
- `--save_checkpoint_metadata` — Saves a `.json` sidecar with loss, LR, step, and epoch per checkpoint.

**Monitoring loss with TensorBoard:**

```bash
# Open a second RunPod terminal
tensorboard --logdir /workspace/logs --port 6006 --bind_all
```

**Downloading checkpoints locally, syncing every 60 seconds:**

```bash
mkdir output
cd output
while true; do
    rsync -avP -e "ssh -p <port> -i <key>" root@<remote_ip>:/workspace/output/ .
    echo "Sync complete. Waiting 60 seconds..."
    sleep 60
done
```

**Downloading logs locally, syncing every 60 seconds:**

```bash
mkdir logs
cd logs
while true; do
    rsync -avP -e "ssh -p <port> -i <key>" root@<remote_ip>:/workspace/logs/ .
    echo "Sync complete. Waiting 60 seconds..."
    sleep 60
done
```

---

## Step 10 — Test Inference via Musubi Before Downloading

Verify the LoRA works on the pod before downloading:

```bash
python src/musubi_tuner/ltx2_generate_video.py \
    --ltx2_checkpoint /workspace/models/ltx/ltx-2.3-22b-dev.safetensors \
    --gemma_root /workspace/models/gemma \
    --gemma_load_in_8bit \
    --prompt "In the style of Suiboku, a Canadian rocky cliff face covered in snow, a single icicle hanging from an overhang, negative space, minimal brushwork" \
    --negative_prompt "photorealistic, photograph, noise, grain, blurry, watermark" \
    --width 1024 \
    --height 576 \
    --num_frames 25 \
    --num_inference_steps 30 \
    --guidance_scale 4.0 \
    --seed 42 \
    --output_path /workspace/output/test_t2v.mp4 \
    --lora_weight /workspace/output/my_style_ltxv.safetensors \
    --lora_multiplier 1.0 \
    --fp8_base \
    --fp8_scaled \
    --flash_attn
```

Use the **original** `.safetensors` file (not the `.comfy.safetensors`) for Musubi inference. Use the `.comfy.safetensors` only in ComfyUI.

---

## Step 11 — ComfyUI: I2V Workflow

The LoRA is already in ComfyUI format. No conversion needed.

1. Copy `my_style_ltxv.comfy.safetensors` to your local ComfyUI `models/loras/` folder.
2. Use an **LTX-Video I2V workflow** in ComfyUI (available in the official ComfyUI examples or community workflows for LTX-V 2.3).
3. Load your keyframe as the first-frame conditioning image.
4. Apply the style LoRA via a LoRA loader node, multiplier 1.0 as a starting point.
5. Use `shifted_logit_normal` timestep sampling in the sampler node.
6. Recommended inference settings: 30 steps, guidance scale 4.0.

**Distilled LoRA note:** If using the LTX 2.3 distilled LoRA (a separate community artifact for fast inference) alongside your style LoRA, bring the distilled LoRA strength down to 0.3–0.5. Community testing confirmed that using a distilled LoRA at 1.0 strength produces poor results on 2.3.

**LoRA stacking:** As noted in the Z-Image ComfyUI guide, stacking LoRAs at inference on distilled models causes quality collapse. Test your style LoRA alone first. If you later want a character LoRA as well, test them separately first, and consider merging at the weight level rather than stacking.

---

## Appendix — Troubleshooting

**"ltx_version mismatch" on startup:**
You set `--ltx_version_check_mode error`. The checkpoint you pointed to isn't LTX-2.3. Re-check the `--ltx2_checkpoint` path.

**OOM during text encoder caching:**
Add `--gemma_load_in_4bit` instead of `--gemma_load_in_8bit` to drop Gemma from ~12GB to ~6GB.

**OOM during latent caching:**
Add `--vae_chunk_size 16` or `--vae_spatial_tile_size 512 --vae_spatial_tile_overlap 64`.

**OOM during training:**
On H100 80GB with this config, OOM is unlikely. If it occurs, add `--blocks_to_swap 10` first.

**Style not appearing at LoRA multiplier 1.0:**
Try 1.5–2.0. This is normal if the concept is subtle or if you undershot on steps. Also check that you're using the `.comfy.safetensors` in ComfyUI (correct) vs the original (not correct for ComfyUI).

**Washed-out colors in T2V output:**
Known LTX 2.3 T2V issue for flat/2D styles. Options: (1) use I2V instead (the issue doesn't appear in I2V), (2) retrain with `--network_dim 64 --network_alpha 64`, (3) add `--lora_target_preset v2v` to include FFN layers.

**Loss below 0.01 and still falling before epoch 40:**
Stop training and use the most recent checkpoint. You've overfit. The trigger word should now activate the style at a lower multiplier (0.7–0.8).

**`flash_attn` not found:**
Run `pip install flash-attn --no-build-isolation` in the pod terminal. This can take 5–10 minutes on H100 if building from source.
