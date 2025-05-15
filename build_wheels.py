#!/usr/bin/env python3
"""
Build wheels for all audio projects and collect them in a centralized wheels directory.
"""

import os
import shutil
import subprocess
import sys
import argparse
from pathlib import Path
import platform


def create_dir(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")


def run_command(command, cwd=None, env=None):
    """Run a shell command and return the result."""
    print(f"Running: {' '.join(command)} in {cwd or os.getcwd()}")
    try:
        if env:
            result = subprocess.run(
                command,
                cwd=cwd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )
        else:
            result = subprocess.run(
                command,
                cwd=cwd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        print(f"Command succeeded")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        raise


def has_cuda():
    """Check if CUDA is available."""
    try:
        # Try to detect CUDA using nvidia-smi
        result = subprocess.run(
            ["nvidia-smi"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        return result.returncode == 0
    except:
        # If nvidia-smi is not found, try checking with torch
        try:
            import torch
            return torch.cuda.is_available()
        except:
            # As a last resort, check if nvcc is in PATH or common CUDA locations exist
            if platform.system() == "Windows":
                for path in ["C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v*\\bin\\nvcc.exe"]:
                    import glob
                    if glob.glob(path):
                        return True
            return False


def find_cuda_home():
    """Find CUDA home directory based on common locations."""
    if 'CUDA_HOME' in os.environ:
        return os.environ['CUDA_HOME']
    
    if platform.system() == "Windows":
        # Try to get CUDA path from Windows registry
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\NVIDIA Corporation\GPU Computing Toolkit\CUDA") as key:
                latest_version = 0
                latest_version_str = ""
                
                # Find the latest version
                try:
                    i = 0
                    while True:
                        version_str = winreg.EnumKey(key, i)
                        try:
                            # Try to parse version like "v12.1"
                            if version_str.startswith('v'):
                                version_parts = version_str[1:].split('.')
                                if len(version_parts) >= 1:
                                    major = int(version_parts[0])
                                    minor = int(version_parts[1]) if len(version_parts) > 1 else 0
                                    version = major * 100 + minor
                                    if version > latest_version:
                                        latest_version = version
                                        latest_version_str = version_str
                        except:
                            pass  # Skip if we can't parse the version
                        i += 1
                except WindowsError:
                    pass  # No more keys
                
                # Get the installation directory from the latest version
                if latest_version_str:
                    with winreg.OpenKey(key, latest_version_str) as version_key:
                        install_dir, _ = winreg.QueryValueEx(version_key, "InstallPath")
                        return install_dir
        except Exception as e:
            print(f"Could not get CUDA path from registry: {e}")
        
        # Check Program Files for CUDA if registry approach failed
        cuda_paths = []
        for root_dir in ["C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA", 
                         "C:\\NVIDIA\\CUDA"]:
            if os.path.exists(root_dir):
                # Find the highest version number
                versions = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d)) and d.startswith('v')]
                if versions:
                    versions.sort(reverse=True)
                    cuda_paths.append(os.path.join(root_dir, versions[0]))
                else:
                    # Try direct folders
                    for ver in range(12, 9, -1):  # Try CUDA 12.x down to 10.x
                        for minor in range(9, -1, -1):
                            test_path = os.path.join(root_dir, f"v{ver}.{minor}")
                            if os.path.exists(test_path):
                                cuda_paths.append(test_path)
        
        if cuda_paths:
            return cuda_paths[0]
    else:
        # Linux/Mac
        common_paths = [
            "/usr/local/cuda",
            "/opt/cuda",
            "/usr/lib/cuda"
        ]
        for path in common_paths:
            if os.path.exists(path):
                return path
    
    return None


def is_windows():
    """Check if running on Windows."""
    return platform.system() == "Windows"


def ensure_torch_with_cuda():
    """Ensure PyTorch is installed with CUDA support if CUDA is available."""
    if not has_cuda():
        print("CUDA not detected. No need to reinstall PyTorch.")
        return
    
    try:
        import torch
        if torch.cuda.is_available():
            print("PyTorch already has CUDA support. No need to reinstall.")
            return
        
        print("CUDA is available but PyTorch was not installed with CUDA support. Reinstalling...")
        run_command([
            sys.executable, "-m", "pip", "install", "--force-reinstall",
            "torch>=2.4.0", "torchvision>=0.19.0", "torchaudio>=2.4.0",
            "--index-url", "https://download.pytorch.org/whl/cu124"
        ])
        print("PyTorch reinstalled with CUDA support.")
    except ImportError:
        print("PyTorch not found. Installing with CUDA support...")
        run_command([
            sys.executable, "-m", "pip", "install",
            "torch>=2.4.0", "torchvision>=0.19.0", "torchaudio>=2.4.0",
            "--index-url", "https://download.pytorch.org/whl/cu124"
        ])
        print("PyTorch installed with CUDA support.")


def install_project_dependencies():
    """Install specific dependencies required for building each project."""
        # Install triton based on platform
    if is_windows():
        print("Installing triton-windows for mamba...")
        try:
            run_command([sys.executable, "-m", "pip", "install", "triton-windows"])
        except Exception as e:
            print(f"Warning: Could not install triton-windows: {e}")
            print("Continuing build process, but mamba might not work optimally without triton.")
    else:
        print("Installing triton for mamba...")
        try:
            run_command([sys.executable, "-m", "pip", "install", "triton"])
        except Exception as e:
            print(f"Warning: Could not install triton: {e}")
            print("Continuing build process, but mamba might not work optimally without triton.")
    
    # Install ninja which is required for mamba
    print("Installing ninja for mamba...")
    try:
        run_command([sys.executable, "-m", "pip", "install", "ninja"])
    except Exception as e:
        print(f"Warning: Could not install ninja: {e}")
        print("Continuing build process, but mamba build might fail without ninja.")
        
    # Ensure packaging is installed
    print("Installing packaging for causal-conv1d...")
    try:
        run_command([sys.executable, "-m", "pip", "install", "packaging"])
    except Exception as e:
        print(f"Warning: Could not install packaging: {e}")
        
    # Install hatchling build backend which is required for openvoice-cli
    print("Installing hatchling and hatch-vcs for openvoice-cli...")
    try:
        run_command([sys.executable, "-m", "pip", "install", "hatchling", "hatch-vcs"])
    except Exception as e:
        print(f"Warning: Could not install hatchling: {e}")
            
    # Install cython which is required for fairseq
    print("Installing cython for fairseq...")
    try:
        run_command([sys.executable, "-m", "pip", "install", "cython"])
    except Exception as e:
        print(f"Warning: Could not install cython: {e}")


def build_wheel(project_path, project_name=None, no_isolation=True):
    """Build a wheel for the project."""
    try:
        # Clean any previous builds
        dist_path = os.path.join(project_path, "dist")
        build_path = os.path.join(project_path, "build")
        if not project_name:
            project_name = os.path.basename(project_path)
        egg_info_path = os.path.join(project_path, f"{project_name}.egg-info")
        if os.path.exists(dist_path):
            shutil.rmtree(dist_path)
        if os.path.exists(build_path):
            shutil.rmtree(build_path)
        if os.path.exists(egg_info_path):
            shutil.rmtree(egg_info_path)
        
        toml_path = os.path.join(project_path, "pyproject.toml")
        if not os.path.exists(toml_path):
            print(f"pyproject.toml does not exist: {toml_path}")
            return None
        
        build_cmd = [sys.executable, "-m", "build", "--wheel"]
        if no_isolation:
            build_cmd.append("--no-isolation")

        if has_cuda() and 'CUDA_HOME' not in os.environ:
                cuda_home = find_cuda_home()
                if cuda_home:
                    print(f"Setting CUDA_HOME to {cuda_home}")
                    os.environ['CUDA_HOME'] = cuda_home
                else:
                    print("CUDA detected but could not determine CUDA_HOME. Build might fail.")
        
        create_dir(dist_path)
        env = os.environ.copy()
            
        # For causal-conv1d, we need to ensure CUDA_HOME is set
        if project_name == "causal-conv1d":
            if has_cuda():
                env["TORCH_CUDA_ARCH_LIST"] = "all"
                env["CAUSAL_CONV1D_FORCE_BUILD"] = "TRUE"
            
            
        # Special case for fairseq with CUDA
        if project_name == "fairseq" and has_cuda():
            print("CUDA detected. Building fairseq with CUDA support...")
            
            # Set environment variable to build with CUDA
            env["TORCH_CUDA_ARCH_LIST"] = "all"
            env["FORCE_CUDA"] = "1"
            
        # Special case for CLAP to ensure version 1.1.5
        # Special case for mamba with CUDA
        elif project_name == "mamba":
            if has_cuda():
                print("CUDA detected. Building mamba with CUDA support...")
                
                # Set environment variable to build with CUDA
                env["TORCH_CUDA_ARCH_LIST"] = "all"
                env["MAMBA_FORCE_BUILD"] = "TRUE"
        
        # Build the shit
        run_command(build_cmd, project_path, env=env)
        
        # Return path to the dist directory
        return dist_path
    except Exception as e:
        print(f"Failed to build wheel for {project_path}: {e}")
        return None


def copy_wheels(source_dir, target_dir):
    """Copy all wheel files from source to target directory."""
    if not os.path.exists(source_dir):
        print(f"Source directory does not exist: {source_dir}")
        return 0
    
    count = 0
    copied_files = []
    for file in os.listdir(source_dir):
        if file.endswith('.whl'):
            src_file = os.path.join(source_dir, file)
            dst_file = os.path.join(target_dir, file)
            # Check if this is a duplicate CLAP version
            if "laion_clap-1.1.4" in file and any("laion_clap-1.1.5" in existing for existing in os.listdir(target_dir)):
                print(f"Skipping {file} as version 1.1.5 is already present")
                continue
            
            shutil.copy2(src_file, dst_file)
            copied_files.append(file)
            print(f"Copied {file} to {target_dir}")
            count += 1
    
    return count, copied_files


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Build wheels for audio projects")
    parser.add_argument("--no-isolation", action="store_true", 
                        help="Build wheels without isolation (use when in a dedicated venv)")
    parser.add_argument("--package", type=str, default=None,
                        help="Build only a specific package (use project directory name)")
    parser.add_argument("--cuda-home", type=str, default=None,
                        help="Set CUDA_HOME manually (useful for CI/CD)")
    return parser.parse_args()


def main():
    # Parse arguments
    args = parse_args()
    
    # Define project directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the build order - causal-conv1d must be built before mamba
    
    all_projects = [
        "CLAP",  # This builds LAION-CLAP 1.1.5 (preferred version)
        "openvoice-cli",
        "versatile_audio_super_resolution",
        "stable-audio-tools",
        "fairseq",
        "causal-conv1d",  # Build causal-conv1d before mamba (dependency)
        "mamba",          # Requires causal-conv1d
        "coqui-ai-TTS",
        "dctorch"
    ]
    
    # Filter to specific package if requested
    if args.package:
        if args.package in all_projects:
            projects = [args.package]
            print(f"\n===== Building only {args.package} =====\n")
        else:
            print(f"ERROR: Package {args.package} not found. Available packages: {', '.join(all_projects)}")
            return
    else:
        projects = all_projects
    
    # Create wheels directory
    wheels_dir = os.path.join(base_dir, "wheels")
    create_dir(wheels_dir)
    cuda_home = None
    cuda_available = False
    if args.cuda_home:
        os.environ['CUDA_HOME'] = args.cuda_home
        print(f"\n===== Setting CUDA_HOME to {args.cuda_home} =====\n")
        cuda_home = args.cuda_home
        if os.path.exists(cuda_home):
            print(f"CUDA_HOME exists: {cuda_home}")
            cuda_available = True
        else:
            print(f"CUDA_HOME does not exist: {cuda_home}")
    else:
        # Always set CUDA_HOME if it's not set but CUDA is detected
        cuda_available = has_cuda()
        if cuda_available and 'CUDA_HOME' not in os.environ:
            cuda_home = find_cuda_home()
    
    if cuda_home:
        print(f"\n===== Setting CUDA_HOME to {cuda_home} =====\n")
        os.environ['CUDA_HOME'] = cuda_home
    
    if cuda_available:
        print("\n===== CUDA detected! CUDA support will be enabled where applicable =====\n")
        
        # Ensure PyTorch is installed with CUDA support
        print("Checking if PyTorch is installed with CUDA support...")
        ensure_torch_with_cuda()
    else:
        print("\n===== CUDA not detected. Building CPU-only versions =====\n")
    
    install_project_dependencies()
    # Check for Windows
    if is_windows():
        print("\n===== Windows detected. Will use triton-windows for mamba =====\n")
    
    # Always use no_isolation since we're in a dedicated venv
    no_isolation = True
    print("\n===== Building wheels without isolation (using current environment) =====\n")
    
    # Build wheels for each project
    total_wheels = 0
    copied_wheels = []
    for project in projects:
        project_path = os.path.join(base_dir, project)
        if not os.path.exists(project_path):
            print(f"Project directory doesn't exist: {project_path}")
            continue
        
        print(f"\n{'=' * 40}")
        print(f"Building wheel for {project}")
        print(f"{'=' * 40}")
        
        dist_dir = build_wheel(project_path, project, no_isolation)
        if dist_dir:
            wheel_count, copied_files = copy_wheels(dist_dir, wheels_dir)
            total_wheels += wheel_count
            copied_wheels.extend(copied_files)
            print(f"Successfully built {wheel_count} wheel(s) for {project}")
        else:
            print(f"Failed to build wheel for {project}")
    
    print(f"\n{'=' * 40}")
    print(f"Build complete! {total_wheels} wheel(s) collected in {wheels_dir}")
    print(f"{'=' * 40}")
    
    # List all built wheels
    print("\nBuilt wheels:")
    for wheel in sorted(os.listdir(wheels_dir)):
        if wheel in copied_wheels and wheel.endswith('.whl'):
            print(f"  - {wheel}")
    
    # Add a note about CUDA support
    if cuda_available:
        print("\nNOTE: fairseq, causal-conv1d, and mamba were built with CUDA support.")
    else:
        print("\nNOTE: fairseq, causal-conv1d, and mamba were built without CUDA support (CPU-only).")
    
    # Add a note about triton for mamba
    if is_windows():
        print("\nNOTE: mamba was built with triton-windows for Windows compatibility.")
    else:
        print("\nNOTE: mamba was built with the standard triton library.")


if __name__ == "__main__":
    main() 