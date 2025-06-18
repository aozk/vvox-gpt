from dotenv import load_dotenv
import os

load_dotenv()

# OpenAIの設定

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
"""
OpenAI APIキーを環境変数から取得します。
デフォルトでは、環境変数 `OPENAI_API_KEY` を使用します。
設定されていない場合は、エラーが発生します。
"""
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
"""
OpenAIモデルを環境変数から取得します。
デフォルトでは、環境変数 `OPENAI_MODEL` を使用し
設定されていない場合は `gpt-4o` を使用します。
この設定は、音声生成のためのChatGPTモデルを指定します。
"""

# VOICEVOXの設定

VOICEVOX_ENGINE_URL = os.getenv("VOICEVOX_ENGINE_URL", "http://127.0.0.1:50021")  # noqa: E501
"""
VOICEVOXエンジンのURLを環境変数から取得します。

デフォルトでは、環境変数 `VOICEVOX_ENGINE_URL` を使用し
設定されていない場合は `http://127.0.1:50021` を使用します。
"""
VOICEVOX_SPEAKER_ID = int(os.getenv("VOICEVOX_SPEAKER_ID", 1))
"""
VOICEVOXのスピーカーIDを環境変数から取得します。

デフォルトでは、環境変数 `VOICEVOX_SPEAKER_ID` を使用し
設定されていない場合は `1` を使用します。
なお、VOICEVOXのスピーカーIDは整数値である必要があります
"""

# 静的ファイルとテンプレートのディレクトリ設定 (FastAPI用)

STATIC_AUDIO_DIR = os.getenv("STATIC_AUDIO_DIR", "static")
"""
静的ファイル（生成された音声）を保存するディレクトリを環境変数から取得します。

デフォルトでは、環境変数 `STATIC_AUDIO_DIR` を使用し
設定されていない場合は `static` を使用します。
このディレクトリは、FastAPIで静的ファイルとして提供されます。
"""
TEMPLATE_DIR = os.getenv("TEMPLATE_DIR", "templates")
"""
Jinja2テンプレートのディレクトリを環境変数から取得します。

デフォルトでは、環境変数 `TEMPLATE_DIR` を使用し
設定されていない場合は `templates` を使用します。
このディレクトリは、FastAPIでHTMLテンプレートとして提供されます。
"""
