# Audio Library Dependency Standardization

This repository contains a collection of forked audio-related Python packages that have been standardized for better compatibility and maintenance.

## Overview

The goal of this project is to standardize the dependency requirements across multiple audio processing libraries, ensuring that they can be used together without conflicts.

## Projects Included

1. **CLAP** - Contrastive Language-Audio Pretraining Model
2. **versatile_audio_super_resolution** - High-quality audio super-resolution tool
3. **stable-audio-tools** - Training and inference tools for generative audio models from Stability AI
4. **openvoice-cli** - CLI tool for OpenVoice voice cloning
5. **fairseq** - Facebook AI Research Sequence-to-Sequence Toolkit
6. **causal-conv1d** - Efficient 1D causal convolution kernel for PyTorch
7. **mamba** - Efficient implementation of selective state space models (Mamba)

## Standardized Dependencies

All projects have been updated to use compatible dependency versions:

| Dependency      | Standardized Version  |
|-----------------|----------------------|
| torch           | >=2.4.0              |
| torchaudio      | >=2.4.0              |
| torchvision     | >=0.19.0             |
| transformers    | >=4.51.3             |
| numpy           | >=1.24.2             |
| pandas          | >=2.2.0              |
| scipy           | >=1.15.0             |
| librosa         | latest               |
| huggingface_hub | latest               |

## Modernization

Where appropriate, projects have been converted from `setup.py` to `pyproject.toml` format following modern Python packaging standards.

## Building Wheels

For instructions on building wheels for all packages, see [WHEEL_BUILDING.md](WHEEL_BUILDING.md).

## Notes for AI Assistants

- All libraries have been standardized to use the same versions of common dependencies
- The most recent dependency versions have been adopted to ensure access to the latest features
- When using these libraries, be aware they have been modified from their original versions
- If you encounter any compatibility issues, check the specific version requirements in the pyproject.toml files
- For CUDA-accelerated projects (fairseq, causal-conv1d, mamba), ensure compatible CUDA toolkit is installed

## Original Repositories

Links to the original repositories:
- [CLAP](https://github.com/LAION-AI/CLAP)
- [versatile_audio_super_resolution](https://github.com/haoheliu/versatile_audio_super_resolution)
- [stable-audio-tools](https://github.com/Stability-AI/stable-audio-tools)
- [openvoice-cli](https://github.com/daswer123/OpenVoice-cli)
- [fairseq](https://github.com/pytorch/fairseq)
- [causal-conv1d](https://github.com/Dao-AILab/causal-conv1d)
- [mamba](https://github.com/state-spaces/mamba) 