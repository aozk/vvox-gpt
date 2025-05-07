from dotenv import load_dotenv
import os

load_dotenv()

# OpenAI設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# VOICEVOX設定
VOICEVOX_ENGINE_URL = os.getenv(
    "VOICEVOX_ENGINE_URL", "http://127.0.0.1:50021")
VOICEVOX_SPEAKER_ID = int(os.getenv("VOICEVOX_SPEAKER_ID", 1))

# ディレクトリ設定
STATIC_AUDIO_DIR = os.getenv("STATIC_AUDIO_DIR", "static")
TEMPLATE_DIR = os.getenv("TEMPLATE_DIR", "templates")
