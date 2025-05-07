from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import uuid
import json
from threading import Thread
import openai
import requests
import os

from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    VOICEVOX_ENGINE_URL,
    VOICEVOX_SPEAKER_ID,
    STATIC_AUDIO_DIR,
    TEMPLATE_DIR
)

# OpenAIキー設定
openai.api_key = OPENAI_API_KEY

# FastAPI 構成
app = FastAPI()

# 静的ファイル（生成された音声）をマウント
app.mount(f"/{STATIC_AUDIO_DIR}",
          StaticFiles(directory=STATIC_AUDIO_DIR), name="static")

# Jinja2 テンプレート
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# 音声生成結果を保存する辞書（本番運用ではDBなどを推奨）
job_results = {}

# 非同期処理関数：ChatGPT + VOICEVOXで音声生成


def generate_audio(job_id: str, prompt: str):
    try:
        # ChatGPT による応答生成
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        message = response.choices[0].message.content

        # VOICEVOXへクエリ送信
        query = requests.post(
            f"{VOICEVOX_ENGINE_URL}/audio_query",
            params={"text": message, "speaker": VOICEVOX_SPEAKER_ID}
        )
        query.raise_for_status()

        # 合成リクエスト
        synthesis = requests.post(
            f"{VOICEVOX_ENGINE_URL}/synthesis",
            params={"speaker": VOICEVOX_SPEAKER_ID},
            data=json.dumps(query.json()),
            headers={"Content-Type": "application/json"}
        )
        synthesis.raise_for_status()

        # 音声ファイルを保存
        filename = f"{job_id}.wav"
        filepath = os.path.join(STATIC_AUDIO_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(synthesis.content)

        # 結果保存
        job_results[job_id] = {
            "message": message,
            "audio_url": f"/{STATIC_AUDIO_DIR}/{filename}"
        }

    except Exception as e:
        job_results[job_id] = {
            "error": str(e)
        }
        print(f"[ERROR] 音声生成失敗 (job_id={job_id}): {e}")

# 音声生成を非同期で開始し、結果表示ページへリダイレクト


@app.get("/chattts")
def chattts_redirect(prompt: str):
    job_id = str(uuid.uuid4())
    Thread(target=generate_audio, args=(job_id, prompt)).start()
    return RedirectResponse(f"/result/{job_id}", status_code=303)

# 結果表示ページ：完了していれば再生ページ表示、未完なら再試行を促す


@app.get("/result/{job_id}", response_class=HTMLResponse)
async def show_result(request: Request, job_id: str):
    if job_id not in job_results:
        return HTMLResponse(
            content="音声生成中です。数秒後に再読み込みしてください。", status_code=200)

    result = job_results[job_id]

    if "error" in result:
        return HTMLResponse(
            content=f"エラーが発生しました：{result['error']}", status_code=500)

    return templates.TemplateResponse(
        request,
        "player.html",
        {
            "message": result["message"],
            "audio_url": result["audio_url"],
        }
    )
