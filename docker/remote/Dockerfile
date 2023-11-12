FROM python:3.10

# Install Dependencies
RUN apt update
RUN apt install -y tesseract-ocr libtesseract-dev libcairo2-dev git

# Create app directory
WORKDIR /workspaces/Smart_Bot

# Install app dependencies
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy app source
COPY . .

# Set Environment Variable
RUN echo $GITHUB_SSH_KEY >> ~/.ssh/id_rsa

# Run app
CMD ["python3", "src/app.py", "--pull_model=True" , "--reindex=True"]

