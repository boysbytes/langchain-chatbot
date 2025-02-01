FROM python:latest

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl https://ollama.ai/install.sh | sh


# Copy Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY chatbot.py .

# Expose the chatbot port
EXPOSE 3000

# Default command (not needed if overridden by docker-compose.yml)
CMD ["chainlit", "run", "chatbot.py", "--port", "3000"]