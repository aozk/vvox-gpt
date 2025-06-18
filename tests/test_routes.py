import uuid
from unittest import mock
from fastapi.testclient import TestClient
from main import app, job_results

client = TestClient(app)


def test_form_page():
    response = client.get("/form")
    assert response.status_code == 200
    assert "音声チャットフォーム" in response.text
    assert '<form action="/chattts" method="post">' in response.text


def test_chattts_form_success():
    message = "こんにちは、これはテストです。"

    with mock.patch("main.Thread") as mock_thread:
        response = client.post(
            "/chattts", data={"prompt": message}, follow_redirects=False)
        args, kwargs = mock_thread.call_args
        # kwargs["args"] が generate_audio の引数タプル
        job_id = kwargs["args"][0]

        assert response.status_code == 303
        assert isinstance(job_id, str)
        assert response.headers["Location"] == f"/result/{job_id}"


def test_result_page_success():
    job_id = str(uuid.uuid4())
    job_results[job_id] = {
        "message": "テスト成功",
        "audio_url": f"/static/{job_id}.wav"
    }

    response = client.get(f"/result/{job_id}")

    assert response.status_code == 200
    assert "テスト成功" in response.text
    assert f"/static/{job_id}.wav" in response.text

    job_results.clear()


def test_result_page_pending():
    job_id = str(uuid.uuid4())  # 存在しない job_id

    response = client.get(f"/result/{job_id}")

    assert response.status_code == 200
    assert "音声生成中" in response.text


def test_result_page_error():
    job_id = str(uuid.uuid4())
    job_results[job_id] = {"error": "VOICEVOX失敗"}

    response = client.get(f"/result/{job_id}")

    assert response.status_code == 500
    assert "エラーが発生しました" in response.text
    assert "VOICEVOX失敗" in response.text

    job_results.clear()


def test_player_template_rendering():
    job_id = str(uuid.uuid4())
    message = "こんにちは、これはテストです。"
    audio_url = f"/static/{job_id}.wav"
    job_results[job_id] = {
        "message": message,
        "audio_url": audio_url
    }

    response = client.get(f"/result/{job_id}")

    assert response.status_code == 200
    assert message in response.text
    assert audio_url in response.text
    assert "<audio" in response.text
    assert "controls" in response.text

    job_results.clear()
