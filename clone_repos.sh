#!/bin/bash

# Simple script to clone all needed repositories
echo "Cloning all repositories..."

# List of repositories to clone
declare -A repos=(
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

# Clone or update each repository
for dir in "${!repos[@]}"; do
  url="${repos[$dir]}"
  
  echo "Processing $dir from $url"
  
  if [ -d "$dir" ]; then
    echo "Directory $dir already exists. Updating..."
    cd "$dir"
    git fetch
    git pull
    cd ..
  else
    echo "Cloning $dir..."
    git clone "$url" "$dir"
  fi
done

echo "All repositories cloned/updated successfully!" 