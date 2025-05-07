import importlib


def test_config_values(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-3.5-test")
    monkeypatch.setenv("VOICEVOX_ENGINE_URL", "http://localhost:9999")
    monkeypatch.setenv("VOICEVOX_SPEAKER_ID", "42")
    monkeypatch.setenv("STATIC_AUDIO_DIR", "test_static")
    monkeypatch.setenv("TEMPLATE_DIR", "test_templates")

    import config
    importlib.reload(config)

    assert config.OPENAI_API_KEY == "test-key"
    assert config.OPENAI_MODEL == "gpt-3.5-test"
    assert config.VOICEVOX_ENGINE_URL == "http://localhost:9999"
    assert config.VOICEVOX_SPEAKER_ID == 42
    assert config.STATIC_AUDIO_DIR == "test_static"
    assert config.TEMPLATE_DIR == "test_templates"
