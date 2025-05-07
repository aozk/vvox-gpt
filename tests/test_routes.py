import uuid
from unittest import mock
from fastapi.testclient import TestClient
from main import app, job_results

client = TestClient(app)


def test_chattts_redirect():
    with mock.patch("main.generate_audio") as mock_gen:
        mock_gen.side_effect = lambda job_id, prompt: job_results.update({
            job_id: {"message": "ダミー応答", "audio_url": f"/dummy/{job_id}.wav"}
        })
        prompt = "テストです"

        response = client.get(
            f"/chattts?prompt={prompt}", follow_redirects=False)
        redirected_path = response.headers["location"]
        job_id = redirected_path.split("/")[-1]

        assert response.status_code == 303
        assert "location" in response.headers
        assert redirected_path.startswith("/result/")
        assert job_id in job_results

        job_results.clear()


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
