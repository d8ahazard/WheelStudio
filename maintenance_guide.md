# Audio Libraries Maintenance Guide

This guide provides instructions for maintaining the standardized audio libraries.

## Overview

The repository contains multiple audio-related Python packages that have been standardized to use compatible dependency versions. This standardization allows these libraries to be used together without conflicts.

## Updating Dependencies

When updating dependencies, follow these principles:

1. **Maintain Compatibility**: Any dependency update should be applied consistently across all projects.
2. **Prefer Modern Versions**: Use the most recent stable versions of dependencies that don't introduce breaking changes.
3. **Test Thoroughly**: After updating, test all projects to ensure they still function correctly.

## Common Dependencies to Monitor

Monitor these key dependencies which are shared across multiple projects:

- **PyTorch Ecosystem**: torch, torchaudio, torchvision
- **Hugging Face**: transformers
- **Data Processing**: numpy, pandas, scipy
- **Audio Processing**: librosa, soundfile

## Update Process

1. **Check for Updates**: Regularly check for new versions of common dependencies.
2. **Evaluate Impact**: Before updating, evaluate the impact of new versions on each project.
3. **Update All Projects**: Apply consistent updates across all projects.
4. **Update Documentation**: Update the dependency comparison document when making changes.

## Adding New Projects

When adding a new audio-related project to this collection:

1. **Analyze Dependencies**: Review the project's dependencies and identify potential conflicts.
2. **Standardize Dependencies**: Update the project's dependency specifications to match the standardized versions.
3. **Convert to pyproject.toml**: If the project uses setup.py, consider converting it to use pyproject.toml.
4. **Update Documentation**: Add the project to the README.md and dependency_comparison.md.

## Potential Issues

Watch for these common issues when updating dependencies:

1. **Breaking Changes**: New versions of libraries might introduce breaking changes. Test thoroughly after updates.
2. **Compiled Extensions**: Projects like fairseq with compiled C++ extensions may require additional testing.
3. **Version Constraints**: Some projects may have specific version constraints for valid reasons (e.g., CLAP's original transformers cap).

## Maintaining Documentation

Keep the following documentation updated:

1. **README.md**: General information about the projects and standardized dependencies.
2. **dependency_comparison.md**: Detailed comparison of original vs. standardized dependencies.
3. **This maintenance guide**: Update with new lessons learned or best practices.

## Testing

After any update, test each project by:

1. Installing the project using pip
2. Running basic functionality tests
3. Checking for any warnings or errors related to dependencies

## Contribution Guidelines

When contributing updates:

1. Explain the rationale for dependency changes
2. Document any compatibility issues encountered
3. Provide thorough testing results 