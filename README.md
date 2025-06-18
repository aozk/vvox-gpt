# VOICEVOX-GPT

![Test](https://github.com/aozk/vvox-gpt/actions/workflows/test.yml/badge.svg)

📢 ChatGPT の応答を VOICEVOX エンジンで音声合成し、Web ブラウザで再生する FastAPI アプリケーションです。
個人の趣味でチクチクと育てています。

---

## 🧩 機能

- ChatGPT（OpenAI API）でプロンプトに応答
- VOICEVOX で音声合成（ローカルエンジンを利用）
- `/chattts?prompt=こんにちは` で非同期音声生成 → `/result/xxxx` にリダイレクト
- 音声ファイルは `static/` に保存され、HTMLで再生

---

## 📂 ディレクトリ構成

```text
.
├─ main.py             # FastAPIアプリ本体
├─ config.py           # 環境変数の管理
├─ static/             # 音声ファイルの保存先
├─ templates/          # HTMLテンプレート（player.html）
├─ extention/          # VOICEVOX エンジン配置先
├─ tests/              # pytest によるテストコード
├─ .env                # OpenAI APIキーなど（git管理外）
├─ .gitignore
└─ README.md
```

[VOICEVOX エンジン](https://github.com/VOICEVOX/voicevox_engine/releases)は別途用意してくだだい。

---

## 🚀 セットアップ手順（Windows / VSCode）

### 1. 仮想環境と依存関係

```sh
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. `.env` を作成（APIキーなど）

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o
VOICEVOX_ENGINE_URL=http://localhost:50021
VOICEVOX_SPEAKER_ID=3
STATIC_AUDIO_DIR=static
TEMPLATE_DIR=templates
```

### 3. VOICEVOXエンジン（ローカル）を起動

```sh
extention/voicevox_engine-windows-cpu-0.23.0/windows-cpu/run.exe
```

※ 起動後、<http://localhost:50021> にアクセス可能なことを確認

---

## 💻 アプリ実行

```bash
uvicorn main:app --reload
```

`http://localhost:8000/form` にアクセスすると、 ChatGPT にメッセージを送ることができます。
そのあとは画面の指示に従ってください。

---

## 🧪 テスト実行

`pytest` をインストールした後に、以下を実行してください。

```bash
$env:PYTHONPATH="."; pytest --cov=main tests/
```

---

## ⚠️ 注意事項

- `.env` には個人の API キーを記載します。**絶対に Git に含めないでください！**
- [VOICEVOX エンジン](https://github.com/VOICEVOX/voicevox_engine/releases)はローカルで動作するものを使用します。

---

## 📜 その他

このプロジェクトは個人利用を想定しています。
また VOICEVOX および OpenAI API の利用規約に従ってください。

---
