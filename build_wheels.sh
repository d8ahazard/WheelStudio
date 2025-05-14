#!/bin/bash
set -e

echo "Building wheels for all audio projects..."

# Create and activate virtual environment
echo "Creating virtual environment for building..."
python3 -m venv build_venv
source build_venv/bin/activate

# Install build dependencies
echo "Installing build dependencies..."
python -m pip install --upgrade pip setuptools wheel build

echo
echo "Checking for CUDA support..."
if command -v nvidia-smi &> /dev/null; then
    echo "CUDA detected! Installing PyTorch with CUDA support..."
    pip install torch>=2.4.0 torchvision>=0.19.0 torchaudio>=2.4.0 --index-url https://download.pytorch.org/whl/cu124
else
    echo "CUDA not detected. Installing CPU version of PyTorch..."
    pip install torch>=2.4.0 torchvision>=0.19.0 torchaudio>=2.4.0
fi

# Create wheels directory
mkdir -p wheels

# Build all projects without isolation
echo
echo "Building all wheels without isolation..."
python build_wheels.py --no-isolation

if [ $? -eq 0 ]; then
    echo ""
    echo "All wheels have been built and collected in the wheels directory."
    echo "You can install them with: pip install wheels/*.whl"
else
    echo "Error building wheels. Check the output above."
    deactivate
    exit 1
fi

# Deactivate venv
deactivate 