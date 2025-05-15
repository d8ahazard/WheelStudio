#!/usr/bin/env python3
import os
import subprocess
import sys
import argparse
import shutil
import time

# Define the submodules with their URLs
SUBMODULES = {
    "coqui-ai-TTS": "https://github.com/d8ahazard/coqui-ai-TTS.git",
    "mamba": "https://github.com/d8ahazard/mamba.git",
    "causal-conv1d": "https://github.com/d8ahazard/causal-conv1d.git",
    "fairseq": "https://github.com/d8ahazard/fairseq.git",
    "stable-audio-tools": "https://github.com/d8ahazard/stable-audio-tools.git",
    "versatile_audio_super_resolution": "https://github.com/d8ahazard/versatile_audio_super_resolution.git",
    "openvoice-cli": "https://github.com/d8ahazard/openvoice-cli.git",
    "CLAP": "https://github.com/d8ahazard/CLAP.git",
}

def run_command(cmd, cwd=None):
    """Run a command and return the output"""
    try:
        result = subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(cmd)}")
        print(f"Error message: {e.stderr}")
        return e.stdout, e.stderr, e.returncode

def check_submodule_exists(name):
    """Check if a submodule exists in .gitmodules file"""
    if os.path.exists(".gitmodules"):
        with open(".gitmodules", "r") as f:
            content = f.read()
            return f'path = {name}' in content
    return False

def check_if_directory_exists(name):
    """Check if a directory exists"""
    return os.path.exists(name) and os.path.isdir(name)

def initialize_submodules():
    """Initialize and update all submodules"""
    print("Initializing all submodules...")
    run_command(["git", "submodule", "init"])
    run_command(["git", "submodule", "update"])
    print("Submodules initialized.")

def update_submodules():
    """Update all submodules to latest commit"""
    print("Updating all submodules...")
    run_command(["git", "submodule", "update", "--remote", "--merge"])
    print("Submodules updated.")

def safely_move_directory(src, dst):
    """Safely move a directory with retries on Windows"""
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        try:
            if os.path.exists(dst):
                shutil.rmtree(dst)
            
            shutil.move(src, dst)
            return True
        except (PermissionError, OSError) as e:
            attempts += 1
            print(f"Error moving directory (attempt {attempts}/{max_attempts}): {str(e)}")
            
            # On Windows, sometimes it helps to wait a bit
            time.sleep(1)
    
    print(f"Failed to move directory after {max_attempts} attempts.")
    return False

def safely_remove_directory(dir_path):
    """Safely remove a directory with retries on Windows"""
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        try:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
            return True
        except (PermissionError, OSError) as e:
            attempts += 1
            print(f"Error removing directory (attempt {attempts}/{max_attempts}): {str(e)}")
            
            # On Windows, sometimes it helps to wait a bit
            time.sleep(1)
    
    print(f"Failed to remove directory after {max_attempts} attempts.")
    return False

def add_missing_submodules():
    """Add missing submodules based on the SUBMODULES dictionary"""
    for name, url in SUBMODULES.items():
        if not check_submodule_exists(name):
            if check_if_directory_exists(name):
                print(f"Directory '{name}' exists but is not a submodule. Converting to submodule...")
                
                # Backup any potential local changes
                if os.path.exists(f"{name}/.git"):
                    print(f"Backing up existing git repository '{name}'...")
                    os.makedirs("backup_repos", exist_ok=True)
                    backup_dir = f"backup_repos/{name}_backup"
                    
                    # Remove previous backup if it exists
                    safely_remove_directory(backup_dir)
                    
                    # Check for local changes
                    stdout, stderr, return_code = run_command(["git", "status", "--porcelain"], cwd=name)
                    has_changes = stdout.strip() != ""
                    
                    if has_changes:
                        print(f"Local changes found in '{name}'. Saving changes...")
                        run_command(["git", "diff", "--staged"], cwd=name)
                        # Create a patch of uncommitted changes
                        stdout, stderr, return_code = run_command(["git", "diff"], cwd=name)
                        os.makedirs(backup_dir, exist_ok=True)
                        with open(f"{backup_dir}/local_changes.patch", "w") as f:
                            f.write(stdout)
                        print(f"Changes saved to {backup_dir}/local_changes.patch")
                    
                    # Rename the directory
                    temp_dir = f"{name}_temp"
                    if not safely_move_directory(name, temp_dir):
                        print(f"Could not move directory '{name}'. Skipping...")
                        continue
                    
                    # Add the repository as a submodule
                    print(f"Adding submodule '{name}' from {url}...")
                    run_command(["git", "submodule", "add", url, name])
                    
                    # Apply any saved patches if necessary
                    if has_changes and os.path.exists(f"{backup_dir}/local_changes.patch"):
                        print(f"Applying local changes to '{name}'...")
                        with open(f"{backup_dir}/local_changes.patch", "r") as f:
                            patch_content = f.read()
                        
                        if patch_content.strip():
                            # Save the patch to a temp file
                            with open(f"{backup_dir}/temp.patch", "w") as f:
                                f.write(patch_content)
                            
                            # Apply the patch
                            run_command(["git", "apply", f"{backup_dir}/temp.patch"], cwd=name)
                            print(f"Local changes applied to '{name}'")
                    
                    # Remove the temporary directory
                    safely_remove_directory(temp_dir)
                    
                else:
                    # Directory exists but is not a git repository
                    # Move it aside and add submodule
                    temp_dir = f"{name}_temp"
                    if not safely_move_directory(name, temp_dir):
                        print(f"Could not move directory '{name}'. Skipping...")
                        continue
                    
                    run_command(["git", "submodule", "add", url, name])
                    
                    # Remove the temporary directory
                    safely_remove_directory(temp_dir)
            else:
                # Directory doesn't exist, simply add the submodule
                print(f"Adding submodule '{name}' from {url}...")
                run_command(["git", "submodule", "add", url, name])

def check_and_pull_submodules():
    """Check if submodules are initialized and pull if necessary"""
    for name, url in SUBMODULES.items():
        if check_submodule_exists(name):
            if not os.path.exists(f"{name}/.git"):
                print(f"Submodule '{name}' is not initialized. Initializing...")
                run_command(["git", "submodule", "update", "--init", name])
            else:
                print(f"Submodule '{name}' is already initialized")
        else:
            print(f"Submodule '{name}' is not configured in .gitmodules")

def setup_submodules():
    """Setup all submodules - add, init, and update"""
    add_missing_submodules()
    initialize_submodules()

def main():
    parser = argparse.ArgumentParser(description="Manage Git submodules for the project")
    parser.add_argument("--add-missing", action="store_true", help="Add missing submodules")
    parser.add_argument("--update", action="store_true", help="Update all submodules to latest commit")
    parser.add_argument("--check", action="store_true", help="Check if submodules are initialized and pull if necessary")
    parser.add_argument("--setup", action="store_true", help="Setup all submodules (add, init, update)")
    
    args = parser.parse_args()
    
    if args.add_missing:
        add_missing_submodules()
    elif args.update:
        update_submodules()
    elif args.check:
        check_and_pull_submodules()
    elif args.setup:
        setup_submodules()
    else:
        # Default action: check and pull
        check_and_pull_submodules()

if __name__ == "__main__":
    main() 