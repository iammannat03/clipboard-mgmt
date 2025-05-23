FROM python:3.9-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    wine \
    xvfb \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set up Wine environment
ENV WINEPREFIX=/root/.wine
ENV WINEARCH=win64
ENV DISPLAY=:99

# Install Python for Windows using Wine
RUN wineboot --init && \
    wget https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe && \
    xvfb-run wine python-3.9.13-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 && \
    rm python-3.9.13-amd64.exe

# Install pip for Windows
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    xvfb-run wine python get-pip.py && \
    rm get-pip.py

# Set up working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN xvfb-run wine pip install -r requirements.txt
RUN xvfb-run wine pip install pyinstaller

# Copy application files
COPY . .

# Build script
CMD ["xvfb-run", "wine", "python", "build.py"] 