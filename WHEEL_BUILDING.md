# Building Wheels for Audio Libraries

This document explains how to build wheel packages for all the standardized audio libraries in this repository.

## Prerequisites

Before building the wheels, ensure you have the following installed:

- Python 3.9 or higher
- pip
- setuptools
- wheel
- build

You can install the build dependencies with:

```bash
pip install --upgrade pip setuptools wheel build
```

### CUDA Support

For building fairseq, causal-conv1d, and mamba with CUDA support:
- Make sure you have NVIDIA drivers installed
- Install the CUDA toolkit that's compatible with your PyTorch version (CUDA 11.6 or higher is required)
- The build script will automatically detect CUDA and build with CUDA support if available

**Note about PyTorch with CUDA**: 
The build scripts automatically check if PyTorch is installed with CUDA support. If CUDA is available on your system but PyTorch was installed without CUDA support, the scripts will reinstall PyTorch 2.4.0+ with CUDA 12.4 support.

## Building All Wheels

### Windows

1. Open a command prompt in the repository root directory
2. Run the batch script:
   ```
   build_wheels.bat
   ```

### Linux/macOS

1. Open a terminal in the repository root directory
2. Make the shell script executable (if needed):
   ```bash
   chmod +x build_wheels.sh
   ```
3. Run the shell script:
   ```bash
   ./build_wheels.sh
   ```

### Manual Build (Any Platform)

You can also run the Python script directly:

```bash
python build_wheels.py
```

## Output

All built wheels will be collected in the `wheels` directory in the root of the repository.

## Installing Wheels

After building, you can install all the wheels at once:

```bash
pip install wheels/*.whl  # Linux/macOS
pip install wheels\*.whl  # Windows
```

Or install individual wheels:

```bash
pip install wheels/specific_package-1.0.0-py3-none-any.whl
```

## Project-Specific Notes

### CLAP

The build script verifies that the CLAP version is 1.1.5, which is the intended version. If a different version is detected in the pyproject.toml file, a warning will be displayed.

### fairseq

fairseq can be built with CUDA support if CUDA is available on your system. The build script automatically detects CUDA and enables it for fairseq. This provides significant performance benefits for training and inference on NVIDIA GPUs.

### causal-conv1d

causal-conv1d is an efficient 1D causal convolution kernel for PyTorch. It's built with CUDA support if available. This package is required by mamba, so it will be built before the mamba package.

### mamba

mamba (mamba_ssm) is an efficient implementation of selective state space models. It depends on causal-conv1d and will be built with CUDA support if available. The build process ensures that causal-conv1d is built first.

On Windows systems, the build script will automatically install the `triton-windows` package instead of the standard `triton` package for compatibility.

## Environment Variables

To force CUDA build manually, you can set these environment variables before running the script:

```bash
# Linux/macOS
export TORCH_CUDA_ARCH_LIST=all
export FORCE_CUDA=1           # For fairseq
export CAUSAL_CONV1D_FORCE_BUILD=TRUE  # For causal-conv1d
export MAMBA_FORCE_BUILD=TRUE  # For mamba

# Windows PowerShell
$env:TORCH_CUDA_ARCH_LIST="all"
$env:FORCE_CUDA=1
$env:CAUSAL_CONV1D_FORCE_BUILD="TRUE"
$env:MAMBA_FORCE_BUILD="TRUE"
```

## Troubleshooting

If you encounter build errors:

1. Check that you have the required build dependencies installed
2. Ensure you have a C++ compiler if building packages with C extensions (like fairseq, causal-conv1d, and mamba)
3. On Windows, you may need Visual C++ Build Tools
4. For CUDA extensions, ensure you have CUDA toolkit installed and that it's compatible with your PyTorch version

### Common Issues with CUDA Builds

- **Missing NVCC**: Ensure the CUDA compiler (nvcc) is in your PATH
- **Architecture Issues**: If you get errors about unsupported GPU architectures, you can specify which ones to build for using `TORCH_CUDA_ARCH_LIST`
- **Missing CUDA Headers**: Make sure CUDA is properly installed and environment variables are set correctly
- **Build Order**: When building manually, make sure to build causal-conv1d before mamba, as mamba depends on it
- **PyTorch without CUDA**: If PyTorch was installed without CUDA, the build scripts will attempt to reinstall it with CUDA 12.4 support and version 2.4.0+

## Manual Building

If you prefer to build packages individually:

```bash
cd <project_directory>
python -m build --wheel
```

The wheel file will be in the `dist` directory of the project. 