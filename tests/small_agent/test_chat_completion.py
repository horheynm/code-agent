import unittest
from unittest.mock import patch, MagicMock
from small_agent.chat_completion import (
    ChatCompletion,
)  # Adjust the import to the correct module path


class TestChatCompletion(unittest.TestCase):

    @patch("small_agent.chat_completion.OpenAI")
    def setUp(self, MockOpenAI):
        self.mock_client = MockOpenAI.return_value
        self.chat_completion = ChatCompletion(openai_key="test_key")

    def test_generate_sync(self):
        messages = [{"role": "user", "content": "Hello!"}]
        self.mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Hi there!"))]
        )

        result = self.chat_completion.generate(
            stream=False,
            model="gpt-3.5-turbo",
            messages=messages,
        )

        self.mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-3.5-turbo", stream=False, messages=messages
        )
        self.assertEqual(result, "Hi there!")

    def test_generate_stream(self):
        messages = [{"role": "user", "content": "Hello!"}]
        response_mock = MagicMock()
        chunk_mock = MagicMock(choices=[MagicMock(delta=MagicMock(content="Hi"))])
        response_mock.__iter__.return_value = iter([chunk_mock])

        self.mock_client.chat.completions.create.return_value = response_mock

        result = list(
            self.chat_completion.generate(
                stream=True,
                model="gpt-3.5-turbo",
                messages=messages,
            )
        )

        self.mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-3.5-turbo", stream=True, messages=messages
        )
        self.assertEqual(result, ["Hi"])

    def test_make_request(self):
        messages = [{"role": "user", "content": "Hello!"}]
        self.mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Hi there!"))]
        )

        result = self.chat_completion.make_request(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        self.mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-3.5-turbo", stream=False, messages=messages
        )
        self.assertEqual(result, "Hi there!")

    def test_make_stream_request(self):
        messages = [{"role": "user", "content": "Hello!"}]
        response_mock = MagicMock()
        chunk_mock = MagicMock(choices=[MagicMock(delta=MagicMock(content="Hi"))])
        response_mock.__iter__.return_value = iter([chunk_mock])

        self.mock_client.chat.completions.create.return_value = response_mock

        result = list(
            self.chat_completion.make_stream_request(
                model="gpt-3.5-turbo",
                messages=messages,
            )
        )

        self.mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-3.5-turbo", stream=True, messages=messages
        )
        self.assertEqual(result, ["Hi"])


if __name__ == "__main__":
    unittest.main()
