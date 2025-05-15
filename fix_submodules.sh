#!/bin/bash

echo "Setting up submodules properly..."

# List of submodules to add
declare -A submodules=(
  ["coqui-ai-TTS"]="https://github.com/d8ahazard/coqui-ai-TTS.git"
  ["mamba"]="https://github.com/d8ahazard/mamba.git"
  ["causal-conv1d"]="https://github.com/d8ahazard/causal-conv1d.git"
  ["fairseq"]="https://github.com/d8ahazard/fairseq.git"
  ["stable-audio-tool"]="https://github.com/d8ahazard/stable-audio-tools.git"
  ["versatile_audio_super_resolution"]="https://github.com/d8ahazard/versatile_audio_super_resolution.git"
  ["openvoice-cli"]="https://github.com/d8ahazard/openvoice-cli.git"
  ["CLAP"]="https://github.com/d8ahazard/CLAP.git"
  ["dctorch"]="https://github.com/d8ahazard/dctorch.git"
)

# Make sure we're not trying to use submodules already
echo "Removing existing .git/modules if present..."
if [ -d ".git/modules" ]; then
  rm -rf .git/modules
fi

# Remove all current submodule entries from .git/config
echo "Cleaning git config of submodule entries..."
git config --local --remove-section submodule 2>/dev/null || true

# Remove the submodule entries from .gitmodules
echo "Creating fresh .gitmodules file..."
> .gitmodules

# Add each submodule properly
for dir in "${!submodules[@]}"; do
  url="${submodules[$dir]}"
  
  echo "Adding submodule $dir from $url"
  
  # Remove the directory if it exists
  if [ -d "$dir" ]; then
    echo "Removing existing directory $dir..."
    rm -rf "$dir"
  fi
  
  # Add the submodule
  git submodule add "$url" "$dir"
  
  # If the operation failed, try again with force
  if [ $? -ne 0 ]; then
    echo "Retrying with --force..."
    git submodule add --force "$url" "$dir"
  fi
done

# Initialize all submodules
echo "Initializing and updating all submodules..."
git submodule init
git submodule update

echo "All submodules should be properly configured now!" 