import streamlit as st
# import replicate
import os
import subprocess

import time
import requests

# Function to run a command in the shell
def run_command(command):
    """Run a command in the shell."""
    process = subprocess.Popen(command, shell=True)
    return process

# Function to check if the server is running
def check_server(url):
    """Check if the server at the given URL is up."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        return False
    return False

# Ensure setup commands run only once
if 'setup_done' not in st.session_state:
    st.session_state.setup_done = False

if not st.session_state.setup_done:
    # Streamlit app
    st.title("Ollama Chatbot Setup and Interface")
    # Run the installation script and wait for it to complete
    with st.spinner("Installing Ollama..."):
        st.markdown("### Running installation script...")
        subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
        st.markdown("### Installation script completed.")

        # Start the ollama server in the background
        st.markdown("### Starting ollama server...")
        ollama_server = run_command("ollama serve")

        # Wait until the ollama server is up and running
        while not check_server("http://127.0.0.1:11434"):
            st.markdown("Waiting for ollama server to start...")
            time.sleep(5)

        st.markdown("### Ollama server is up and running.")

        # Pull llama3 in the background
        st.markdown("### Pulling llama3 model...")
        pull_llama3 = run_command("ollama pull llama3")

        # Wait for the pull command to complete
        pull_llama3.wait()

        st.markdown("### llama3 model has been pulled successfully.")

        # Mark setup as done
        st.session_state.setup_done = True

# import ollama
from langchain_community.llms import Ollama

llm = Ollama(model='llama3')

# st.set_page_config(
#     layout="wide"
# )

if st.button("Clear Messages"):
    st.session_state.messages.clear()

# Function to run a shell command and print its output
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line, end='')
    for line in process.stderr:
        print(line, end='')
    process.wait()
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        st.error(f"Error occurred: {stderr.strip()}{stdout}")
    else:
        st.success("Command executed successfully.")

prompt = ""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
        "role": "assistant",
        "content": "Hello! I am a helpful assistant."
        }
    ]
    # Command to install Ollama
    # install_command = "curl -fsSL https://ollama.com/install.sh | sh"
    # with st.spinner("Installing Ollama..."):
    #     run_command(install_command)

    # # Command to serve Ollama
    # serve_command = "ollama serve"
    # with st.spinner("Starting Ollama server..."):
    #     subprocess.Popen(serve_command, shell=True)  # Running this in the background

    # # Command to pull the Llama3 model
    # pull_command = "ollama pull llama3"
    # with st.spinner("Downloading llama3..."):
    #     run_command(pull_command)
    
    
    

# streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false


for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        prompt += f'{message["role"]} said: {message["content"]}\n '

sent = st.chat_input('Ask me anything')

if sent:
    prompt += f'user said: {sent}\n'
    with st.chat_message('user'):
        st.markdown(sent)

    user_prompt = {
        "role": "user",
        "content": sent
    }
    st.session_state.messages.append(user_prompt)

    prompt += 'assistant said:'
    with st.spinner("Generating response..."):
        chat_response = llm.invoke(prompt, stop=['<|eot_id|>'])
        response = f'{chat_response}'
        with st.chat_message(name='assistant'):
            st.write(response)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

