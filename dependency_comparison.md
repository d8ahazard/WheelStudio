# Dependency Comparison - Original vs. Standardized

This document tracks the changes made to standardize dependencies across all audio projects.

## Common Dependencies Standardized

| Dependency      | Standardized Version | Notes |
|-----------------|----------------------|-------|
| torch           | >=2.4.0              | Upgraded from various versions (lowest was 1.13.1 in openvoice-cli) |
| torchaudio      | >=2.4.0              | Upgraded from various versions (lowest was 0.13.1 in openvoice-cli) |
| torchvision     | >=0.19.0             | Added where missing, upgraded where present |
| transformers    | >=4.51.3             | Removed cap in CLAP (was <=4.30.2), upgraded where present |
| numpy           | >=1.24.2             | Standard minimum version across all projects |
| scipy           | >=1.15.0             | Upgraded to latest version |
| pandas          | >=2.2.0              | Upgraded to latest version |

## Project-Specific Changes

### CLAP

**Original Dependencies (Key):**
- numpy>=2.0.0
- transformers<=4.30.2
- No torch/torchaudio explicit requirements

**Standardized:**
- numpy>=1.24.2 (reduced minimum version)
- transformers>=4.51.3 (removed cap, upgraded)
- Added torch>=2.4.0, torchaudio>=2.4.0, torchvision>=0.19.0

### openvoice-cli

**Original Dependencies (Key):**
- torch>=1.13.1
- torchaudio>=0.13.1
- numpy>=1.24.2
- No transformers requirement

**Standardized:**
- torch>=2.4.0 (significant upgrade)
- torchaudio>=2.4.0 (significant upgrade)
- numpy>=1.24.2 (unchanged)
- Added transformers>=4.51.3

### versatile_audio_super_resolution

**Original Dependencies (Key):**
- torch>=2.6.0
- torchaudio>=2.6.0
- torchvision>=0.21.0
- transformers>=4.51.3
- No specific numpy requirement

**Standardized:**
- torch>=2.4.0 (relaxed requirement)
- torchaudio>=2.4.0 (relaxed requirement)
- torchvision>=0.19.0 (relaxed requirement)
- transformers>=4.51.3 (unchanged)
- Added numpy>=1.24.2

### stable-audio-tools

**Original Dependencies (Key):**
- torch>=2.5.1
- torchaudio>=2.5.1
- transformers>=4.51.0
- numpy>=1.23.5
- No specific torchvision requirement

**Standardized:**
- torch>=2.4.0 (relaxed requirement)
- torchaudio>=2.4.0 (relaxed requirement)
- transformers>=4.51.3 (upgraded)
- numpy>=1.24.2 (upgraded)
- Added torchvision>=0.19.0

### fairseq

**Original Dependencies (Key):**
- torch>=2.1.0
- numpy>=1.21.3
- No transformers, pandas, or scipy requirements
- No torchaudio or torchvision requirements

**Standardized:**
- torch>=2.4.0 (upgraded)
- numpy>=1.24.2 (upgraded)
- Added torchaudio>=2.4.0, torchvision>=0.19.0
- Added transformers>=4.51.3, pandas>=2.2.0, scipy>=1.15.0

### causal-conv1d

**Original Dependencies (Key):**
- Only setup.py with no explicit version requirements
- Requires CUDA 11.6+ for GPU support

**Standardized:**
- torch>=2.4.0
- numpy>=1.24.2
- einops (retained)
- packaging (retained)
- Added pyproject.toml with modern structure
- Maintained CUDA support (11.6+ requirement)

### mamba

**Original Dependencies (Key):**
- torch (no version specified)
- triton
- ninja
- einops
- transformers (no version specified)
- packaging
- Requires causal-conv1d>=1.2.0 as optional dependency

**Standardized:**
- torch>=2.4.0
- numpy>=1.24.2
- triton (for non-Windows) and triton-windows (for Windows) - retained
- ninja - retained
- einops - retained
- packaging - retained
- transformers>=4.51.3 (specified version)
- causal-conv1d as direct dependency
- Added pyproject.toml with modern structure
- Maintained CUDA support

## Packaging Changes

| Project | Original Format | New Format | Notes |
|---------|----------------|------------|-------|
| CLAP | pyproject.toml | pyproject.toml | Updated dependencies only |
| openvoice-cli | pyproject.toml | pyproject.toml | Updated dependencies only |
| versatile_audio_super_resolution | setup.py | pyproject.toml | Converted to modern format |
| stable-audio-tools | Both | pyproject.toml | Standardized on pyproject.toml |
| fairseq | Basic pyproject.toml + setup.py | Complete pyproject.toml | Enhanced pyproject.toml |
| causal-conv1d | setup.py | pyproject.toml | Converted to modern format |
| mamba | setup.py | pyproject.toml | Converted to modern format |

## Potential Issues to Watch

1. CLAP originally had a cap on transformers (<=4.30.2), might have compatibility issues with newer versions
2. fairseq has complex build requirements and C++ extensions that might need additional testing
3. NumPy version changes (especially downgrading from >=2.0.0 to >=1.24.2 in CLAP) may affect functionality
4. The significant torch/torchaudio upgrades in openvoice-cli (from 1.13.1 to 2.4.0) may require code changes
5. causal-conv1d and mamba have CUDA dependencies that require CUDA 11.6+ for full functionality
6. mamba depends on causal-conv1d, so build order is important when building from source
7. mamba requires triton (or triton-windows on Windows systems) for optimal performance 