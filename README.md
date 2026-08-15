# MiniMax Music 3.0 API: Python Wrapper for Text-to-Music Generation

[![Powered by MuAPI](https://img.shields.io/badge/Powered%20by-MuAPI-6366f1?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0tMSAxNHYtNGgtMnYtMmg0djZoLTJ6bTAtOFY2aDJ2MmgtMnoiLz48L3N2Zz4=)](https://muapi.ai?utm_source=github&utm_medium=badge&utm_campaign=minimax-music-3-api)

[![PyPI version](https://img.shields.io/pypi/v/minimax-music-3-api.svg)](https://pypi.org/project/minimax-music-3-api/)
[![GitHub stars](https://img.shields.io/github/stars/SamurAIGPT/minimax-music-3-api.svg)](https://github.com/SamurAIGPT/minimax-music-3-api/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A clean, standalone Python SDK for **MiniMax Music 3.0**, delivered via [muapi.ai](https://muapi.ai?utm_source=github&utm_medium=readme&utm_campaign=minimax-music-3-api). Generate a fully arranged, mixed song — or its instrumental twin — from a style prompt and a set of lyrics in a single API call.

## Related Projects

- [awesome-minimax-music-3-prompts](https://github.com/Anil-matcha/awesome-minimax-music-3-prompts) — curated prompt library, lyrics-formatting guide, and prompt engineering tips
- [minimax-music-3-comfyui](https://github.com/Anil-matcha/minimax-music-3-comfyui) — native ComfyUI custom nodes for MiniMax Music 3.0
- [Seedance-2.5-API](https://github.com/SamurAIGPT/Seedance-2.5-API) — Python wrapper for Seedance 2.5 video generation
- [MiniMax-H3-API](https://github.com/Anil-matcha/MiniMax-H3-API) — Python SDK for MiniMax's H3 video model
- [Open-Generative-AI](https://github.com/Anil-matcha/Open-Generative-AI) — open-source studio for running generative image, video, and audio workflows
- [Generative-Media-Skills](https://github.com/SamurAIGPT/Generative-Media-Skills) — agent-ready skills for building generative-media pipelines
- [muapi-cli](https://github.com/SamurAIGPT/muapi-cli) — CLI and MCP access to MuAPI generation tasks

## 🚀 Why Use MiniMax Music 3.0 API?

MiniMax Music 3.0 generates a complete song — not a loop, not a stem — in one request.

- **Full song generation**: Verse/chorus structure, instrumentation, and a mixed/mastered vocal (or instrumental) track from a single call.
- **Structured lyrics input**: Control line breaks, pauses, and instrumental sections with a small, explicit formatting syntax.
- **Vocal or instrumental**: Toggle `is_instrumental` to render the identical arrangement with or without vocals — useful for karaoke tracks or sync deliverables.
- **Configurable audio quality**: Choose `bitrate` and `sample_rate` to match your delivery pipeline.
- **Developer-first**: Simple Python SDK, fast turnaround via MuAPI's infrastructure, no per-provider account setup.

## 🌟 Key Features

- ✅ **Text-to-Music**: Generate a complete song from a style description and lyrics.
- ✅ **Lyrics formatting**: Single newline for a new line, double newline for a pause, `##` to mark an instrumental section.
- ✅ **Instrumental toggle**: `is_instrumental=True` renders the same arrangement without vocals.
- ✅ **Bitrate control**: `60000`, `32000`, `64000`, `128000`, or `256000` (default `256000`).
- ✅ **Sample rate control**: `16000`, `24000`, `32000`, or `44100` Hz (default `44100`).
- ✅ **Blocking helper**: `generate_and_wait()` submits and polls in one call, returning the final audio URL.

---

## 🛠 Installation

### Via Pip (Recommended)
```bash
pip install minimax-music-3-api
```

### From Source
```bash
git clone https://github.com/SamurAIGPT/minimax-music-3-api.git
cd minimax-music-3-api
pip install -r requirements.txt
```

### Configuration
Create a `.env` file in the root directory and add your [MuAPI](https://muapi.ai?utm_source=github&utm_medium=readme&utm_campaign=minimax-music-3-api) API key:
```env
MUAPI_API_KEY=your_muapi_api_key_here
```

---

## 💻 Quick Start (Python)

```python
from minimax_music_3_api import MiniMaxMusic3API

api = MiniMaxMusic3API()

# 1. Generate a song
print("Generating song with MiniMax Music 3.0...")
submission = api.generate(
    prompt="an upbeat synth-pop anthem with driving drums and a soaring chorus",
    lyrics="[Verse]\nWalking through the city lights\n\n##\n[Chorus]\nWe are shining, we are free",
)

# 2. Wait for completion
result = api.wait_for_completion(submission["request_id"])
audio_url = api.extract_audio_url(result)
print(f"Success! Listen to your song here: {audio_url}")

# ...or do both in one call:
audio_url = api.generate_and_wait(
    prompt="an upbeat synth-pop anthem with driving drums and a soaring chorus",
    lyrics="[Verse]\nWalking through the city lights\n\n##\n[Chorus]\nWe are shining, we are free",
)
```

---

## 📡 API Reference

Base URL: `https://api.muapi.ai/api/v1`
Endpoint: `POST /minimax-music-3.0`

```bash
curl --location --request POST "https://api.muapi.ai/api/v1/minimax-music-3.0" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data-raw '{
      "prompt": "an upbeat synth-pop anthem with driving drums and a soaring chorus",
      "lyrics": "[Verse]\nWalking through the city lights\n\n##\n[Chorus]\nWe are shining, we are free",
      "is_instrumental": false,
      "bitrate": 256000,
      "sample_rate": 44100
  }'
```

### Lyrics formatting rules

| Syntax | Effect |
|---|---|
| `\n` (single newline) | New line within a section |
| `\n\n` (double newline) | Pause / section break |
| `##` | Marks a point where instrumental accompaniment should be layered in |

### Parameters

| Parameter | Type | Options | Default | Required | Description |
|---|---|---|---|---|---|
| `prompt` | string | — | — | Yes | Style, mood, tempo, and instrumentation description |
| `lyrics` | string | 10–3000 chars | — | Yes | Song lyrics using the formatting rules above |
| `is_instrumental` | boolean | `true` / `false` | `false` | No | Render an instrumental-only version of the same arrangement |
| `bitrate` | int | `60000` `32000` `64000` `128000` `256000` | `256000` | No | Output audio bitrate |
| `sample_rate` | int | `16000` `24000` `32000` `44100` | `44100` | No | Output sample rate (Hz) |

### Polling for results

```python
import time
import requests


def wait_for_result(request_id, api_key, poll_interval=5, timeout=300):
    start = time.time()
    while time.time() - start < timeout:
        result = requests.get(
            "https://api.muapi.ai/api/v1/predictions/{}/result".format(request_id),
            headers={"Authorization": "Bearer {}".format(api_key)},
        ).json()
        if result["status"] == "completed":
            return result
        if result["status"] == "failed":
            raise RuntimeError(result.get("error", "Generation failed"))
        time.sleep(poll_interval)
    raise TimeoutError("Generation timed out")
```

### Response

```json
{
  "status": "completed",
  "output": {
    "audio": "https://cdn.muapi.ai/output/minimax-music-3.0/abc123.mp3"
  }
}
```

---

## 🎤 Vocal + Instrumental Pair Example

Generate a matching instrumental track for the same song by resubmitting with `is_instrumental=True`:

```python
from minimax_music_3_api import MiniMaxMusic3API

api = MiniMaxMusic3API()

prompt = "warm acoustic folk ballad, fingerpicked guitar, gentle upright bass, intimate vocal"
lyrics = "[Verse]\nWe walked the road where the pines grow tall\n\n##\n[Chorus]\nHome isn't a place, it's a feeling we made"

vocal_url = api.generate_and_wait(prompt=prompt, lyrics=lyrics, is_instrumental=False)
instrumental_url = api.generate_and_wait(prompt=prompt, lyrics=lyrics, is_instrumental=True)

print(f"Vocal:       {vocal_url}")
print(f"Instrumental: {instrumental_url}")
```

See [`examples/basic_usage.py`](examples/basic_usage.py) and [`examples/instrumental_example.py`](examples/instrumental_example.py) for runnable scripts.

---

## 📖 Documentation & Guides

For prompt engineering, lyrics-formatting tips, and a curated song-prompt library, see [awesome-minimax-music-3-prompts](https://github.com/Anil-matcha/awesome-minimax-music-3-prompts).

| Method | Parameters | Description |
| :--- | :--- | :--- |
| `generate` | `prompt`, `lyrics`, `is_instrumental`, `bitrate`, `sample_rate` | Submit a MiniMax Music 3.0 generation request. |
| `generate_instrumental` | `prompt`, `lyrics`, `bitrate`, `sample_rate` | Convenience wrapper for `generate(..., is_instrumental=True)`. |
| `generate_and_wait` | same as `generate` plus `poll_interval`, `timeout` | Submit and block until the audio URL is ready. |
| `get_result` | `request_id` | Check the status/result of a submitted request. |
| `wait_for_completion` | `request_id`, `poll_interval`, `timeout` | Blocking helper that polls until the task completes or fails. |
| `extract_audio_url` | `result` | Static helper to pull the hosted audio URL out of a completed result. |

---

## 🔗 Official Resources
- **Playground**: [muapi.ai/playground/minimax-music-3.0](https://muapi.ai/playground/minimax-music-3.0?utm_source=github&utm_medium=readme&utm_campaign=minimax-music-3-api)
- **Model page**: [muapi.ai/minimax-music-3.0](https://muapi.ai/minimax-music-3.0?utm_source=github&utm_medium=readme&utm_campaign=minimax-music-3-api)
- **API Provider**: [MuAPI.ai](https://muapi.ai?utm_source=github&utm_medium=readme&utm_campaign=minimax-music-3-api)

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Keywords**: MiniMax Music 3.0, text-to-music API, AI music generator, AI song generator, lyrics-to-song API, MuAPI, Python music SDK, AI audio generation, generative music API, AI music composition, text-to-audio API.
