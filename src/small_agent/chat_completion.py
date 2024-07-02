from typing import Generator, Any, List, Dict
from openai import OpenAI


class ChatCompletion:
    def __init__(self, openai_key: str) -> None:
        self.client = OpenAI(api_key=openai_key)

    def generate(
        self,
        stream: bool,
        model: str = "gpt-3.5-turbo",
        **kwargs: Any,
    ) -> Any:
        if stream:
            return self.make_stream_request(model=model, **kwargs)
        else:
            return self.make_request(model=model, **kwargs)

    def make_request(
        self,
        model: str,
        messages: List[Dict],
        **kwargs: Any,
    ) -> str:
        response = self.client.chat.completions.create(
            model=model,
            stream=False,
            messages=messages,
            **kwargs,
        )
        message = response.choices[0].message
        return message.content

    def make_stream_request(
        self,
        model: str,
        messages: List[Dict],
        **kwargs: Any,
    ) -> Generator[str, None, None]:
        response = self.client.chat.completions.create(
            model=model,
            stream=True,
            messages=messages,
            **kwargs,
        )
        for chunk in response:
            choice_delta = chunk.choices[0].delta
            if (content := choice_delta.content) is not None:
                yield content
