import os
import sys
import openai
from tenacity import (
    retry,
    stop_after_attempt, # type: ignore
    wait_random_exponential, # type: ignore
)
# import transformers


from typing import Optional, List
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


Model = Literal["gpt-4", "gpt-3.5-turbo", "text-davinci-003", "Qwen", "llama"]

openai.api_key = os.getenv('OPENAI_API_KEY')

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_completion(prompt: str, temperature: float = 0.0, max_tokens: int = 256, stop_strs: Optional[List[str]] = None) -> str:
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=stop_strs,
    )
    return response.choices[0].text

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_chat(prompt: str, model: Model, temperature: float = 0.0, max_tokens: int = 256, stop_strs: Optional[List[str]] = None, is_batched: bool = False) -> str:
    assert model != "text-davinci-003"
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        stop=stop_strs,
        temperature=temperature,
    )
    return response.choices[0]["message"]["content"]

from langchain_openai import ChatOpenAI
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_4o(prompt: str, model: str = "4o", temperature: float = 0.0, max_tokens: int = 256, stop_strs: Optional[List[str]] = None, is_batched: bool = False) -> str:
    class ModelConfig:
        def __init__(
            self,
            model : str,
            base_url : str,
            temperature=0.1,
            top_p=0.7,
            max_tokens = 1024,
            seed = 4595,
            api_key : str = " ",
            stop: List[str] = ["\n"] 
        ) -> None:
            '''
            config settings for model
            '''
            self.model = model
            self.base_url = base_url
            self.temperature = temperature
            self.top_p = top_p
            self.max_tokens = max_tokens
            self.api_key = api_key
            self.seed = seed
            self.stop = stop

    summarizer_config = ModelConfig(
        model =  "gpt-4o", 
        base_url = "https://api.openai.com/v1", 
        api_key = "" ,
        temperature = 0.0,
        max_tokens = 256, 
        stop = stop_strs  
    )

    ChatSummarizer = ChatOpenAI(
        api_key = summarizer_config.api_key,
        model = summarizer_config.model,
        base_url = summarizer_config.base_url,
        temperature = summarizer_config.temperature,
        top_p = summarizer_config.top_p,
        max_tokens = summarizer_config.max_tokens,
        seed = summarizer_config.seed,
        stop=summarizer_config.stop
    )

    completion = ChatSummarizer.invoke(
    input=[
        {"role": "system", "content": "you are a agent."},
        {"role": "user", "content": prompt}
    ]
    ).content
    # print('4o')
    return completion

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_Qwen(prompt: str, model: str = "Qwen", temperature: float = 0.0, max_tokens: int = 512, stop_strs: Optional[List[str]] = None, is_batched: bool = False) -> str:
    from openai import OpenAI
    client = OpenAI(
        # 若没有配置环境变量，请用百炼 API Key 将下行替换为：api_key="sk-xxx",
        api_key="",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    def get_chat(prompt: str, temperature: float = 0.0, max_tokens: int = 256, stop_strs: Optional[List[str]] = None,
                 is_batched: bool = False) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are a action planner, you should answer the direct think or action. For example,'think: First I need to go to the kitchen.' or 'go east'"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        completion = client.chat.completions.create(
            model="qwen2.5-72b-instruct",
            messages=messages,
            max_tokens=max_tokens,
            stop=stop_strs,
            temperature=temperature,
        )
        return completion.choices[0].message.content
    return get_chat(prompt, temperature, max_tokens, stop_strs)


# @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_llama(prompt: str, model: str = "llama",  temperature: float = 0.01, max_tokens: int = 2560, stop_strs: Optional[List[str]] = None, is_batched: bool = False) -> str:
    import requests

    url = "https://api.siliconflow.cn/v1/chat/completions"
    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://sf-maas-uat-prod.oss-cn-shanghai.aliyuncs.com/dog.png",
                            "detail": "auto"
                        }
                    }
                ]
            }
        ],
        "stream": False,
        "max_tokens": 512,
        "stop": ["null"],
        "temperature": 0,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"}
    }
    headers = {
        "Authorization": "",
        "Content-Type": "application/json"
    }
