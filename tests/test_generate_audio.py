import os
import uuid
import tempfile
from unittest import mock
from main import generate_audio, job_results


# VOICEVOX の音声合成が成功した場合のテスト
@mock.patch("main.openai.chat.completions.create")
@mock.patch("main.requests.post")
@mock.patch("main.STATIC_AUDIO_DIR", new_callable=lambda: tempfile.mkdtemp())
def test_generate_audio_success(mock_static_dir, mock_post, mock_openai):
    mock_openai.return_value = mock.Mock(
        choices=[mock.Mock(message=mock.Mock(content="テスト音声"))])
    mock_post.side_effect = [
        mock.Mock(status_code=201, json=lambda: {"mock": "query"}),
        mock.Mock(status_code=200, content=b"FAKE_WAV_DATA")
    ]

    job_id = str(uuid.uuid4())

    generate_audio(job_id, "こんにちは")

    result = job_results.get(job_id)
    assert result is not None
    assert "message" in result
    assert "audio_url" in result
    assert result["message"] == "テスト音声"

    file_path = os.path.join(mock_static_dir, f"{job_id}.wav")
    assert os.path.exists(file_path)

    job_results.clear()


# VOICEVOX audio_query が失敗（HTTP 500）した場合のテスト
@mock.patch("main.openai.chat.completions.create")
@mock.patch("main.requests.post")
def test_generate_audio_voicevox_error(mock_post, mock_openai):
    mock_openai.return_value = mock.Mock(
        choices=[mock.Mock(message=mock.Mock(content="テスト音声"))]
    )

    mock_post.side_effect = [
        mock.Mock(
            status_code=500,
            raise_for_status=mock.Mock(
                side_effect=Exception("VOICEVOX query error"))
        )
    ]

    job_id = str(uuid.uuid4())

    generate_audio(job_id, "VOICEVOX に失敗させたい")

    result = job_results.get(job_id)
    assert result is not None
    assert "error" in result
    assert "VOICEVOX query error" in result["error"]

    # cleanup
    job_results.clear()
