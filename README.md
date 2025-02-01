# Chatbot (Ollama and Langchain)

## Overview
Built using the Langchain framework and Ollama, this chatbot helps me explore the topic of AI and large language models (LLMs).

### Key Features
- **Context memory:** The chatbot remembers past conversations, so it gives more relevant responses.
- **Customization:** If you use DeepSeek R1, you can choose to show or hide its thinking using the `/toggle_thoughts` command.

## Installation

### Prerequisites:
- Docker Desktop for Windows
- Windows Subsystem for Linux (WSL)
- Internet connection
- At least 15GB of storage

Follow this procedure to install.

1. Clone the repository.

    ```bash
    git clone https://github.com/boysbytes/langchain-chatbot.git
    cd langchain-chatbot
    ```

2. Create the Ollama data directory.

    ```bash
    mkdir data
    mkdir ./data/ollama
    ```

3. Build the Docker image.

    ```bash
    docker-compose build
    ```

4. Start the services.

    ```bash
    docker-compose up -d
    ```

5. Pull a model.

    ```bash
    docker exec -it ollama ollama run deepseek-r1:1.5b
    ```

## Usage

1. Access the chatbot: `http://localhost:3000`

2. By default, its thinking process is hidden. You can see its thinking process by sending this command: `/toggle_thoughts`

3. When you're done, stop and clean-up.

    ```bash
    docker-compose down
    ```


## Configuration

### Change the model

1. Start the Docker services.

2. Replace the model.

    ```bash
    # List the models
    docker exec -it ollama ollama list

    # Delete a model
    docker exec -it ollama ollama rm <model_name>
    
    # Pull another model
    docker exec -it ollama ollama run <model_name> 
    ```
3. Update the model name in `chatbot.py`

    ```python
    class Chatbot:
        def __init__(self, model_name="<model_name>", temperature=0.6):
            # Initialize memory to store conversation history
            self.memory = ConversationBufferMemory(return_messages=True)
    ```

    For example, if you use `deepseek-r1:1.5b`, then update as follows:
    ```python
    class Chatbot:
        def __init__(self, model_name="deepseek-r1:1.5b", temperature=0.6):
            # Initialize memory to store conversation history
            self.memory = ConversationBufferMemory(return_messages=True)
    ```


4. Rebuild and run the containers.

    ```bash
    docker-compose up --build
    ```

    ## Troubleshooting

- Ensure Docker Desktop is running.
- Check container logs: If something doesn't work, monitor the logs for errors:

    ```bash
    docker-compose logs -f
    ```

- Verify the model was pulled successfully.

    ```bash
    docker exec ollama-chatbot ollama list
    ```

- Restart services: If issues persist, restart the containers:

    ```bash
    docker-compose down
    docker-compose up -d
    ```