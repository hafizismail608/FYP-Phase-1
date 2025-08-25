import os
import subprocess
import wave
import json
import zipfile
from typing import Optional, List, Tuple

import requests

try:
    from vosk import Model, KaldiRecognizer
    VOSK_AVAILABLE = True
except Exception:
    VOSK_AVAILABLE = False


class SubtitleService:
    """
    Generate subtitles (WebVTT) from a video using free/offline Vosk STT.
    Requires ffmpeg installed and Python package `vosk`.
    """

    def __init__(self, models_dir: str = None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.models_dir = models_dir or os.path.join(base_dir, 'services', 'models')
        os.makedirs(self.models_dir, exist_ok=True)
        self.model_name = 'vosk-model-small-en-us-0.15'
        self.model_path = os.path.join(self.models_dir, self.model_name)

    def ensure_model(self) -> bool:
        if not VOSK_AVAILABLE:
            print('Vosk not installed. Install with: pip install vosk')
            return False
        if os.path.isdir(self.model_path):
            return True
        # Download small English model
        url = 'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip'
        zip_path = os.path.join(self.models_dir, self.model_name + '.zip')
        try:
            print('Downloading Vosk model (small)...')
            with requests.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(zip_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(self.models_dir)
            os.remove(zip_path)
            return os.path.isdir(self.model_path)
        except Exception as e:
            print(f'Failed to download Vosk model: {e}')
            return False

    def extract_audio(self, video_path: str, wav_path: str) -> bool:
        try:
            cmd = [
                'ffmpeg', '-y',
                '-i', video_path,
                '-ac', '1',          # mono
                '-ar', '16000',      # 16 kHz
                '-vn',               # no video
                wav_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0 and os.path.exists(wav_path)
        except Exception as e:
            print(f'ffmpeg extract_audio error: {e}')
            return False

    def transcribe(self, wav_path: str) -> List[dict]:
        """
        Returns a list of word dicts with 'word', 'start', 'end'
        """
        words: List[dict] = []
        try:
            if not self.ensure_model():
                return words
            model = Model(self.model_path)
            wf = wave.open(wav_path, 'rb')
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
                wf.close()
                return words
            rec = KaldiRecognizer(model, wf.getframerate())
            rec.SetWords(True)
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    res = json.loads(rec.Result())
                    if 'result' in res:
                        words.extend(res['result'])
            # final
            res = json.loads(rec.FinalResult())
            if 'result' in res:
                words.extend(res['result'])
            wf.close()
        except Exception as e:
            print(f'Vosk transcribe error: {e}')
        return words

    @staticmethod
    def _format_ts(seconds: float) -> str:
        ms = int(seconds * 1000)
        h = ms // 3600000
        ms %= 3600000
        m = ms // 60000
        ms %= 60000
        s = ms // 1000
        ms %= 1000
        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

    def words_to_vtt(self, words: List[dict], vtt_path: str, max_duration: float = 5.0, max_words: int = 12) -> bool:
        try:
            with open(vtt_path, 'w', encoding='utf-8') as f:
                f.write('WEBVTT\n\n')
                if not words:
                    # Write a placeholder cue if empty
                    f.write('00:00:00.000 --> 00:00:05.000\nAutomatic subtitles unavailable.\n\n')
                    return True
                bucket: List[dict] = []
                bucket_start = None
                for w in words:
                    start = float(w.get('start', 0.0))
                    end = float(w.get('end', start + 0.4))
                    if bucket and (end - bucket_start >= max_duration or len(bucket) >= max_words):
                        text = ' '.join(x.get('word', '') for x in bucket)
                        f.write(f"{self._format_ts(bucket_start)} --> {self._format_ts(bucket[-1].get('end', bucket_start))}\n")
                        f.write(text + '\n\n')
                        bucket = []
                        bucket_start = None
                    if not bucket:
                        bucket_start = start
                    bucket.append({'word': w.get('word', ''), 'end': end})
                if bucket:
                    text = ' '.join(x.get('word', '') for x in bucket)
                    f.write(f"{self._format_ts(bucket_start)} --> {self._format_ts(bucket[-1].get('end', bucket_start))}\n")
                    f.write(text + '\n\n')
            return True
        except Exception as e:
            print(f'Error writing VTT: {e}')
            return False

    def generate_subtitles(self, video_path: str, output_dir: str) -> Optional[str]:
        """
        Generate WebVTT subtitles for a video and return the subtitle filename (saved in output_dir).
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            base = os.path.splitext(os.path.basename(video_path))[0]
            wav_path = os.path.join(output_dir, f'{base}_stt.wav')
            vtt_path = os.path.join(output_dir, f'{base}.vtt')
            if not self.extract_audio(video_path, wav_path):
                print('Audio extraction failed; cannot generate subtitles')
                return None
            words = self.transcribe(wav_path)
            # Clean up wav to save space
            try:
                os.remove(wav_path)
            except Exception:
                pass
            if self.words_to_vtt(words, vtt_path):
                return os.path.basename(vtt_path)
            return None
        except Exception as e:
            print(f'generate_subtitles error: {e}')
            return None 