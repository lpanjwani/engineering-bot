FROM python:3.9

# Create app directory
WORKDIR /workspaces/smart-bot

# Install app dependencies
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy app source
COPY . .

# Set environment variables
ENV PYTHONPATH "/workspaces/smart-bot"

# Run app
CMD ["bash", "docker/dev/entrypoint.sh"]
