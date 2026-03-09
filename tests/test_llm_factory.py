from virtual_dev_pod.llm_factory import _extract_chat_content, _is_conversational_only_error


class _Message:
    def __init__(self, content: str):
        self.content = content


class _Choice:
    def __init__(self, message: _Message):
        self.message = message


class _Response:
    def __init__(self, content: str):
        self.choices = [_Choice(_Message(content))]


def test_detects_conversational_only_error():
    exc = ValueError(
        "Model X is not supported for task text-generation and provider Y. "
        "Supported task: conversational."
    )
    assert _is_conversational_only_error(exc) is True


def test_extract_chat_content_from_choices():
    response = _Response("hello from chat")
    assert _extract_chat_content(response) == "hello from chat"
