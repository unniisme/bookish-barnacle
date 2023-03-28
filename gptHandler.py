import openai
import os
from time import time
import json

history_file = open(os.getcwd() + "/gptHistory/chat_history.txt", "a")
memory = []
history_file.write(f"--Timestamp:{time()}--\n")


def WriteHistory(prompt, response):
    history_file.write(f"Prompt: {prompt}\n")
    history_file.write("Response: " + response["message"]["content"].strip())
    history_file.write("\n\n")
    history_file.flush()

openai.api_key = os.environ["OPENAI_API_KEY"]



def generate_response(prompt, keep_memory = True, write_history = True):
    messages = [{"role":"system", "content":"You are a helpful assistant"}] + memory + [{"role": "user", "content": prompt}]
    # print("-----")
    # print(messages)
    # print("-----")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0]
    
    if keep_memory:
        memory.append({"role":"user", "content":prompt})
        memory.append(response["message"])

    if write_history:
        WriteHistory(prompt, response)

        # Write to gptHistory/chat_history.json the json file response
        with open("gptHistory/chat_history.json", "w") as history_json:
            json.dump(memory, history_json, indent=4)

    return response

