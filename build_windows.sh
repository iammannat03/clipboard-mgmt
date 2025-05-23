#!/bin/bash

# Build the Docker image
echo "Building Docker image..."
docker build -t clipboard-windows-builder .

# Create a container and run the build
echo "Building Windows executable..."
docker run --rm -v "$(pwd)/build:/app/build" clipboard-windows-builder

# Check if build was successful
if [ -d "build/ClipboardManager" ]; then
    echo "Build successful! Windows executable is in build/ClipboardManager/"
    echo "Files created:"
    ls -R build/ClipboardManager/
else
    echo "Build failed. Check the Docker output for errors."
    exit 1
fi 