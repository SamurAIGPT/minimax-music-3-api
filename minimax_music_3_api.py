import os
import time

import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


BITRATES = (60000, 32000, 64000, 128000, 256000)
SAMPLE_RATES = (16000, 24000, 32000, 44100)


class MiniMaxMusic3API:
    """Python client for MuAPI's MiniMax Music 3.0 text-to-music endpoint."""

    def __init__(self, api_key=None):
        """
        Initialize the MiniMax Music 3.0 API client.

        :param api_key: MuAPI API key. Defaults to the MUAPI_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("MUAPI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API Key is required. Set MUAPI_API_KEY in .env or pass it to the constructor."
            )

        self.base_url = "https://api.muapi.ai/api/v1"
        self.endpoint = "{}/minimax-music-3.0".format(self.base_url)
        self.headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Content-Type": "application/json",
        }

    def generate(self, prompt, lyrics, is_instrumental=False, bitrate=256000, sample_rate=44100):
        """
        Submit a MiniMax Music 3.0 generation request.

        :param prompt: Style, mood, tempo, and instrumentation description.
        :param lyrics: 10-3000 characters. A single newline starts a new line, a
            double newline inserts a pause, and "##" marks a section where
            instrumental accompaniment should be layered in.
        :param is_instrumental: Render an instrumental-only version of the same
            arrangement described by prompt/lyrics. Defaults to False.
        :param bitrate: One of 60000, 32000, 64000, 128000, 256000. Defaults to 256000.
        :param sample_rate: One of 16000, 24000, 32000, 44100. Defaults to 44100.
        :return: dict with at least a "request_id" key.
        """
        self._validate(prompt, lyrics, bitrate, sample_rate)
        payload = {
            "prompt": prompt,
            "lyrics": lyrics,
            "is_instrumental": is_instrumental,
            "bitrate": bitrate,
            "sample_rate": sample_rate,
        }
        return self._post_request(payload)

    def generate_instrumental(self, prompt, lyrics, bitrate=256000, sample_rate=44100):
        """Convenience wrapper for generate(..., is_instrumental=True)."""
        return self.generate(prompt, lyrics, is_instrumental=True, bitrate=bitrate, sample_rate=sample_rate)

    def get_result(self, request_id):
        """Check the status/result of a submitted generation request."""
        endpoint = "{}/predictions/{}/result".format(self.base_url, request_id)
        response = requests.get(endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def wait_for_completion(self, request_id, poll_interval=5, timeout=300):
        """Poll until a request completes or fails, returning the completed result."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self.get_result(request_id)
            status = result.get("status")
            if status in ("completed", "success"):
                return result
            if status in ("failed", "cancelled"):
                raise RuntimeError("Music generation failed: {}".format(result.get("error")))
            time.sleep(poll_interval)
        raise TimeoutError("Timed out waiting for music generation to complete.")

    def generate_and_wait(self, prompt, lyrics, is_instrumental=False, bitrate=256000,
                           sample_rate=44100, poll_interval=5, timeout=300):
        """Submit a request and block until the audio URL is ready."""
        submission = self.generate(prompt, lyrics, is_instrumental, bitrate, sample_rate)
        request_id = submission.get("request_id")
        if not request_id:
            raise RuntimeError("No request_id in submission response: {}".format(submission))
        result = self.wait_for_completion(request_id, poll_interval=poll_interval, timeout=timeout)
        audio_url = self.extract_audio_url(result)
        if not audio_url:
            raise RuntimeError("No audio URL in completed result: {}".format(result))
        return audio_url

    @staticmethod
    def extract_audio_url(result):
        """Pull the hosted audio URL out of a completed prediction result."""
        output = result.get("output")
        if isinstance(output, dict) and output.get("audio"):
            return output["audio"]
        if isinstance(output, str):
            return output
        return result.get("audio")

    @staticmethod
    def _validate(prompt, lyrics, bitrate, sample_rate):
        if not prompt or not prompt.strip():
            raise ValueError("prompt is required")
        if not lyrics or not (10 <= len(lyrics) <= 3000):
            raise ValueError("lyrics is required and must be 10-3000 characters")
        if bitrate not in BITRATES:
            raise ValueError("bitrate must be one of {}".format(BITRATES))
        if sample_rate not in SAMPLE_RATES:
            raise ValueError("sample_rate must be one of {}".format(SAMPLE_RATES))

    def _post_request(self, payload):
        response = requests.post(self.endpoint, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    try:
        api = MiniMaxMusic3API()
        submission = api.generate(
            prompt="an upbeat synth-pop anthem with driving drums and a soaring chorus",
            lyrics="[Verse]\nWalking through the city lights\n\n##\n[Chorus]\nWe are shining, we are free",
        )
        request_id = submission.get("request_id")
        print("Task submitted. Request ID: {}".format(request_id))
        result = api.wait_for_completion(request_id)
        print("Generation completed: {}".format(result))
    except Exception as exc:
        print("Error: {}".format(exc))
