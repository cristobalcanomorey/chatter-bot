#!/bin/bash

# Run the installation script and wait for it to complete
curl -fsSL https://ollama.com/install.sh | sh

# Start the ollama server in the background
ollama serve &

# Function to check if the ollama server is running
check_server() {
  curl -s http://127.0.0.1:11434 > /dev/null
}

# Wait until the ollama server is up and running
until check_server; do
  echo "Waiting for ollama server to start..."
  sleep 5
done

echo "Ollama server is up and running."

# Pull llama3 in the background
ollama pull llama3 &
PULL_PID=$!  # Capture the process ID of the pull command

# Wait for the pull command to complete
wait $PULL_PID

echo "llama3 has been pulled successfully."

# Run the Streamlit app in the background
streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false &