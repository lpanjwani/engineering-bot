FROM python:3.9

# Install Dependencies
RUN apt update
RUN apt install -y tesseract-ocr libtesseract-dev

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
CMD ["python3", "src/app.py", "--pull_model=True" , "--reindex=True"]

