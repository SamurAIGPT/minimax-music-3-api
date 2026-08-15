#!/usr/bin/env python3
"""Generate an instrumental-only cinematic cue with minimax-music-3-api."""

from minimax_music_3_api import MiniMaxMusic3API


def main():
    api = MiniMaxMusic3API()

    result_url = api.generate_and_wait(
        prompt=(
            "Massive cinematic trailer score, orchestral strings and brass building over a "
            "hybrid taiko drum ostinato, choir swell at the climax, huge low-end braams"
        ),
        lyrics="##\n[Instrumental — orchestral trailer cue]\n##",
        is_instrumental=True,
        bitrate=256000,
        sample_rate=44100,
    )
    print(f"Instrumental cue ready: {result_url}")


if __name__ == "__main__":
    main()
