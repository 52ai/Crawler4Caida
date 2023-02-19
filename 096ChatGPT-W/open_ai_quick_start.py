# coding: utf-8
"""
create on Feb 15, 2023 By Wayne YU
Email: ieeflsyu@outlook.com

Function:

测试ChatGPT的API接口的另一种实现openai，并探索其他的可能性，比如代码自动生成、图片生成等功能

"""
import os
import openai
import time

key_file = ".key/openai_key.txt"
with open(key_file, 'r', encoding='utf-8') as f:
    line = f.readlines()[0].strip()
    # print("openai api key:", line)
    openai_api_key = line

# Load your API key from an environment variable or secret management service
openai.api_key = openai_api_key


def openai_text():
    """
    Openai在文本生成方面的应用
    :return:
    """
    prompt = "I'm a Chinese, would you please tell me how to learning English very well?"
    print("问题：", prompt)

    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=prompt,
                                        temperature=0.7,
                                        max_tokens=2048,
                                        n=5)
    # 输出响应结果
    result = response['choices'][0]['text'].strip()
    print("回答:", result)


def openai_image():
    """
    Openai在图片生成方面的应用
    :return:
    """
    prompt = "a beautiful house in the mountain with river"
    response_image = openai.Image.create(
      prompt=prompt,
      n=1,
      size="512x512"
    )
    print(response_image)
    print("Get image url:")
    for item in response_image["data"]:
        print(item["url"])


if __name__ == "__main__":
    time_start = time.time()
    openai_text()
    # openai_image()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
