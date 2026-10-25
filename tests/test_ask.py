from types import SimpleNamespace
from unittest.mock import patch

from app.ask import ask


def test_ask_prints_input_and_output_token_counts(capsys):
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(
            prompt_token_count=12,
            candidates_token_count=7,
        ),
        text="回答",
    )
    client = SimpleNamespace(
        models=SimpleNamespace(generate_content=lambda **kwargs: response)
    )

    with patch("app.ask.genai.Client", return_value=client), patch(
        "app.ask.get_api_key", return_value="test-key"
    ):
        result = ask("質問")

    assert result == "回答"
    output = capsys.readouterr().out
    assert "入力: 12" in output
    assert "出力: 7" in output