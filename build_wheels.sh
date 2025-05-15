#!/bin/bash
set -e

# Parse arguments
package=""
flag=""

while [ "$#" -gt 0 ]; do
    case "$1" in
        --package)
            package="$2"
            shift 2
            ;;
        --no-isolation)
            flag="--no-isolation"
            shift
            ;;
        *)
            echo "Unknown parameter: $1"
            exit 1
            ;;
    esac
done

# Detect Python executable
if ! command -v python3 &> /dev/null; then
    echo "Python not found! Please install Python 3.8 or newer."
    exit 1
fi

# Set CUDA_HOME if it's not set but CUDA is installed
if [ -z "$CUDA_HOME" ]; then
    for cuda_path in /usr/local/cuda-* /usr/local/cuda; do
        if [ -e "$cuda_path/bin/nvcc" ]; then
            export CUDA_HOME="$cuda_path"
            echo "Set CUDA_HOME to $CUDA_HOME"
            break
        fi
    done
fi

# Create and activate virtual environment
if [ ! -d "build_venv" ]; then
    echo "Creating build virtual environment..."
    python3 -m venv build_venv
fi

source build_venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install build pip-tools

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

# Run the build script
if [ -n "$package" ]; then
    echo "Building only package: $package, CUDA_HOME: $CUDA_HOME"
    python build_wheels.py --package "$package" $flag --cuda-home "$CUDA_HOME"
else
    echo "Building all packages, CUDA_HOME: $CUDA_HOME"
    python build_wheels.py $flag --cuda-home "$CUDA_HOME"
fi

echo
echo "Build completed! Check the wheels directory for built wheels."

if [ $? -ne 0 ]; then
    echo "Error building wheels. Check the output above."
    deactivate
    exit 1
fi

# Deactivate venv
deactivate

echo
echo "All wheels have been built and collected in the wheels directory."
echo "You can install them with: pip install wheels/*.whl"
echo 