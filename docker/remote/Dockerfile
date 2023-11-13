FROM python:3.9-bookworm

# Install Dependencies
RUN apt update
RUN apt install -y \
    tesseract-ocr \
    libtesseract-dev \
    libcairo2-dev \
    poppler-utils \
    gcc \
    git

# Create SSH Keys Directory
RUN mkdir ~/.ssh

# Create app directory
WORKDIR /workspaces/Smart_Bot

# Install app dependencies
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy app source
COPY . .

# Run app
CMD ["python3", "src/app.py", "--pull_model=True" , "--reindex=True"]

