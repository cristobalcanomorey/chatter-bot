import streamlit as st
# import replicate
import os
from langchain_community.llms import Ollama
import subprocess

llm = Ollama(model='llama3')

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
        st.error(f"Error occurred: {stderr}")
    else:
        st.success("Command executed successfully.")

prompt = ""
if "messages" not in st.session_state:
    # Command to install Ollama
    install_command = "curl -fsSL https://ollama.com/install.sh | sh"
    with st.spinner("Installing Ollama..."):
        run_command(install_command)

    # Command to serve Ollama
    serve_command = "ollama serve"
    with st.spinner("Starting Ollama server..."):
        subprocess.Popen(serve_command, shell=True)  # Running this in the background

    # Command to pull the Llama3 model
    pull_command = "ollama pull llama3"
    with st.spinner("Downloading llama3..."):
        run_command(pull_command)
    st.session_state.messages = [
        {
        "role": "assistant",
        "content": "Hello! I am a helpful assistant."
        }
    ]

# streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
if st.button("Clear Messages"):
    st.session_state.messages.clear()

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

