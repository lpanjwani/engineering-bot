FROM python:3.10

# Install Dependencies
RUN apt update
RUN apt install -y \
    tesseract-ocr \
    libtesseract-dev \
    libcairo2-dev \
    git \
    poppler-utils

# Create app directory
WORKDIR /workspaces/Smart_Bot

# Install app dependencies
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy app source
COPY . .

# Create SSH Keys
RUN mkdir ~/.ssh

# Run app
CMD ["python3", "src/app.py", "--pull_model=True" , "--reindex=True"]

