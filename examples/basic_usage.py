#!/usr/bin/env python3
"""Basic usage example for the minimax-music-3-api Python SDK.

Usage:
    export MUAPI_API_KEY=your_key_here
    python examples/basic_usage.py
"""

from minimax_music_3_api import MiniMaxMusic3API


def main():
    api = MiniMaxMusic3API()

    prompt = (
        "Upbeat 80s-influenced synth-pop anthem, driving four-on-the-floor drums, "
        "glossy analog synth arpeggios, warm bass, soaring female vocal, big "
        "anthemic chorus, radio-ready mix"
    )
    lyrics = (
        "[Verse]\n"
        "Headlights cutting through the violet haze\n"
        "We're chasing echoes of our younger days\n"
        "\n\n"
        "##\n"
        "[Chorus]\n"
        "We are shining, we are free\n"
        "Running wild along the sea"
    )

    print("Generating vocal song...")
    audio_url = api.generate_and_wait(prompt=prompt, lyrics=lyrics)
    print(f"Song ready: {audio_url}")

    print("Generating instrumental twin of the same arrangement...")
    instrumental_url = api.generate_and_wait(prompt=prompt, lyrics=lyrics, is_instrumental=True)
    print(f"Instrumental ready: {instrumental_url}")


if __name__ == "__main__":
    main()
