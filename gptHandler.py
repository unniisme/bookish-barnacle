# Importing necessary modules
import openai
import os
from time import time
import json

# Open a file in append mode
history_file = open(os.getcwd() + "/gptHistory/chat_history.log", "a")
# Write the current timestamp to the file
history_file.write(f"--Timestamp:{time()}--\n")

# Function to write the prompt and response to the history file
def WriteHistory(prompt, response):
    history_file.write(f"Prompt: {prompt}\n")
    history_file.write("Response: " + response["message"]["content"].strip())
    history_file.write("\n\n")
    history_file.flush()

# Set the OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Function to generate the AI response
def generate_response(prompt, memory_file, keep_memory = True, write_history = True):
    # Load previous conversation history if keep_memory is True
    if keep_memory:
        try:
            with open(memory_file, "r") as history_json:
                memory = json.load(history_json)
        except Exception as e:
            memory = []
            with open(memory_file, "w") as history_json:
                json.dump(memory, history_json, indent=4)      

    # Create messages to send to the AI, consisting of previous conversation history and the prompt
    messages = [{"role":"system", "content":"You are a helpful assistant"}] + memory + [{"role": "user", "content": prompt}]
    # Use OpenAI's API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0]
    
    # If keep_memory is True, add the prompt and response to the conversation history
    if keep_memory:
        memory.append({"role":"user", "content":prompt})
        memory.append(response["message"])

        # Write the conversation history to a JSON file
        with open(memory_file, "w") as history_json:
            json.dump(memory, history_json, indent=4)

    # If write_history is True, write the prompt and response to the history file
    if write_history:
        WriteHistory(prompt, response)

    # Return the generated response
    return response