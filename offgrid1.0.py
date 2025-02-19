import os
import subprocess
import requests
import shutil

# Folder where all resources will be saved
BASE_DIR = "offline_survival_resources"
os.makedirs(BASE_DIR, exist_ok=True)

# Define categories and their corresponding YouTube video links
categories = {
    "Medical": [
        "https://www.youtube.com/watch?v=BFheNvvJGoQ",
        "https://www.youtube.com/watch?v=nnUQHKZqnkw",
        "https://youtube.com/shorts/xDpcxucT6dw?si=aJRVyfvryuA1h0no",
    ],
    "Weapons": [
        "https://www.youtube.com/watch?v=XToBzC5B_qg",
        "https://www.youtube.com/watch?v=FxlZihQzpTQ",
        "https://www.youtube.com/watch?v=l4Z9Yg1OHMM",
    ],
    "Hunting": [
        "https://www.youtube.com/watch?v=klcV-y68uUg&ab_channel=FARGONE",
        "https://www.youtube.com/watch?v=bcKQZlRUu-4",
        "https://www.youtube.com/watch?v=sb80TkNKmHk",
    ],
    "Farming": [
        "https://www.youtube.com/watch?v=6X9WryRnt_w",
        "https://www.youtube.com/watch?v=5rkTfP5_q4I",
        "https://www.youtube.com/watch?v=x8F2Xj2fl0o",
    ],
}

# Survival PDF resources
resources = [
    {"url": "https://archive.org/download/ultimate-survival-manual/Ultimate_Survival_Manual.pdf", "filename": "Ultimate_Survival_Manual.pdf"},
    {"url": "https://archive.org/download/Survival_Manual_20130607/Survival_Manual.pdf", "filename": "Survival_Manual.pdf"},
    {"url": "https://archive.org/download/HerbalMedicineBook/Herbal_Medicine_for_Beginners.pdf", "filename": "Herbal_Medicine_for_Beginners.pdf"},
    {"url": "https://archive.org/download/first-aid-manuals/Basic_First_Aid.pdf", "filename": "Basic_First_Aid.pdf"},
    {"url": "https://archive.org/download/Backyard-Homesteading/Backyard_Homesteading_Guide.pdf", "filename": "Backyard_Homesteading_Guide.pdf"},
    {"url": "https://archive.org/download/diy-greenhouse/Diy_Greenhouse_Guide.pdf", "filename": "DIY_Greenhouse_Guide.pdf"},
    {"url": "https://archive.org/download/ham-radio-guide/Ham_Radio_Guide.pdf", "filename": "Ham_Radio_Guide.pdf"},
    {"url": "https://archive.org/download/MedicalBooks/Emergency_Medical_Guide.pdf", "filename": "Emergency_Medical_Guide.pdf"},
    {"url": "https://archive.org/download/SurvivalHandbook/Survival_Handbook_Complete.pdf", "filename": "Survival_Handbook_Complete.pdf"},
    {"url": "https://archive.org/download/SelfSufficiencyGuide/Self_Sufficiency_Guide.pdf", "filename": "Self_Sufficiency_Guide.pdf"}
]

# Function to check if a command is available
def command_exists(command):
    try:
        subprocess.run([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

# Function to install a package using the appropriate package manager
def install_package(package, os_type):
    if os_type == "windows":
        subprocess.run(["choco", "install", "-y", package])
    elif os_type == "linux":
        subprocess.run(["sudo", "apt-get", "install", "-y", package])
    else:
        raise ValueError("Unsupported OS type")

# Function to download a file from the web using requests
def download_file(url, save_path):
    if os.path.exists(save_path):
        print(f"File {save_path} already exists, skipping download.")
        return
    try:
        print(f"Downloading from {url}...")
        response = requests.get(url, stream=True)
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded {save_path}")
    except Exception as e:
        print(f"Failed to download {url}. Error: {e}")

# Download PDF resources
def download_pdfs():
    for resource in resources:
        save_path = os.path.join(BASE_DIR, resource['filename'])
        download_file(resource['url'], save_path)

# Function to download YouTube videos into categories
def download_youtube_videos():
    for category, links in categories.items():
        category_dir = os.path.join(BASE_DIR, category)
        os.makedirs(category_dir, exist_ok=True)

        for video in links:
            video_path = os.path.join(category_dir, f"{video.split('watch?v=')[-1]}.mp4")
            if os.path.exists(video_path):
                print(f"Video {video_path} already exists, skipping download.")
                continue
            print(f"Downloading video {video} to {category} category...")
            try:
                output_path = os.path.join(category_dir, '%(title)s.%(ext)s')
                subprocess.run(['yt-dlp', '-o', output_path, video], check=True)
                print(f"Downloaded video to {category_dir}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to download video {video}. Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred while downloading video {video}. Error: {e}")

# Function to download all videos from Archive.org URL and categorize them
def download_archive_videos(archive_url):
    archive_dir = os.path.join(BASE_DIR, "Archive_Videos")
    os.makedirs(archive_dir, exist_ok=True)
    if any(os.path.isfile(os.path.join(archive_dir, f)) for f in os.listdir(archive_dir)):
        print(f"Videos in {archive_dir} already exist, skipping download.")
        return
    try:
        subprocess.run(['yt-dlp', '--output', os.path.join(archive_dir, '%(title)s.%(ext)s'), archive_url], check=True)
        print(f"Downloaded all videos from {archive_url} to {archive_dir}")

        # Categorize downloaded archive videos
        for file in os.listdir(archive_dir):
            for category in categories.keys():
                if category.lower() in file.lower():
                    category_dir = os.path.join(BASE_DIR, category)
                    os.makedirs(category_dir, exist_ok=True)
                    os.rename(os.path.join(archive_dir, file), os.path.join(category_dir, file))
                    print(f"Moved {file} to {category_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to download videos from {archive_url}. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while downloading from {archive_url}. Error: {e}")

# Function to clone and extract all files from GitHub repository
def download_github_pdfs():
    github_repo = "https://github.com/PR0M3TH3AN/Survival-Data.git"
    github_dir = os.path.join(BASE_DIR, "HOME")
    os.makedirs(github_dir, exist_ok=True)
    
    # Check if all expected files exist
    expected_files = set()
    for root, dirs, files in os.walk(github_dir):
        for name in files:
            expected_files.add(os.path.join(root, name))
    
    if expected_files:
        print(f"All files in {github_dir} already exist, skipping download.")
        return
    
    try:
        subprocess.run(["git", "clone", github_repo, github_dir], check=True)
        print("GitHub repository cloned successfully.")

        # Copy all files and directories from the HOME directory to BASE_DIR
        for root, dirs, files in os.walk(github_dir):
            for name in files:
                src = os.path.join(root, name)
                dst = os.path.join(BASE_DIR, os.path.relpath(src, github_dir))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                print(f"Extracted {name} to {BASE_DIR}")
    except Exception as e:
        print(f"Failed to clone GitHub repository. Error: {e}")

# Function to check for the existence of all files before downloading
def check_files_exist():
    # Check PDFs
    for resource in resources:
        save_path = os.path.join(BASE_DIR, resource['filename'])
        if not os.path.exists(save_path):
            return False

    # Check YouTube videos
    for category, links in categories.items():
        category_dir = os.path.join(BASE_DIR, category)
        for video in links:
            video_path = os.path.join(category_dir, f"{video.split('watch?v=')[-1]}.mp4")
            if not os.path.exists(video_path):
                return False

    # Check Archive.org videos
    archive_dir = os.path.join(BASE_DIR, "Archive_Videos")
    if not any(os.path.isfile(os.path.join(archive_dir, f)) for f in os.listdir(archive_dir)):
        return False

    # Check GitHub files
    github_dir = os.path.join(BASE_DIR, "HOME")
    for root, dirs, files in os.walk(github_dir):
        for name in files:
            src = os.path.join(root, name)
            dst = os.path.join(BASE_DIR, os.path.relpath(src, github_dir))
            if not os.path.exists(dst):
                return False

    return True

# Main function
def main():
    print("Starting download process...")

    # Check for required dependencies
    required_commands = ["yt-dlp", "git"]
    os_type = "windows" if os.name == "nt" else "linux"

    for command in required_commands:
        if not command_exists(command):
            print(f"Command {command} not found, installing...")
            install_package(command, os_type)

    if check_files_exist():
        print("All files already exist, skipping download.")
    else:
        download_pdfs()
        download_youtube_videos()
        download_archive_videos("https://archive.org/details/Survival_Lilly_Archive")
        download_github_pdfs()
        print("Download process completed.")

# Run the main function
if __name__ == "__main__":
    main()
