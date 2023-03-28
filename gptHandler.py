import openai
import os
from time import time
import json

history_file = open(os.getcwd() + "/gptHistory/chat_history.log", "a")
history_file.write(f"--Timestamp:{time()}--\n")


def WriteHistory(prompt, response):
    history_file.write(f"Prompt: {prompt}\n")
    history_file.write("Response: " + response["message"]["content"].strip())
    history_file.write("\n\n")
    history_file.flush()

openai.api_key = os.environ["OPENAI_API_KEY"]



def generate_response(prompt, memory_file, keep_memory = True, write_history = True):
    if keep_memory:
        try:
            with open(memory_file, "r") as history_json:
                memory = json.load(history_json)
        except Exception as e:
            memory = []
            with open(memory_file, "w") as history_json:
                json.dump(memory, history_json, indent=4)      

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

        # Write to gptHistory/chat_history.json the json file response
        with open(memory_file, "w") as history_json:
            json.dump(memory, history_json, indent=4)

    if write_history:
        WriteHistory(prompt, response)


    return response

