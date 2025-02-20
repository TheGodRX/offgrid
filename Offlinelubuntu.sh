#!/bin/bash
set -e  # Exit on error

# Define directories
BASE_DIR="$HOME/offline_survival_resources"
PIP_CACHE="$HOME/.cache/pip"
PACKAGE_CACHE="$HOME/package_cache"
UBUNTU_REPO="$HOME/lubuntu_package_cache"
mkdir -p "$BASE_DIR" "$PIP_CACHE" "$PACKAGE_CACHE" "$UBUNTU_REPO"

# Update and upgrade system
echo "Updating system and installing essential system packages..."
sudo apt update && sudo apt full-upgrade -y

# Install core system tools
SYSTEM_PACKAGES=(
    "build-essential" "linux-headers-generic" "git" "wget" "curl" "rsync" "vim" "nano" "tmux"
    "htop" "ufw" "iptables" "wireguard-tools" "openvpn" "dnsmasq" "nginx" "apache2" "php"
    "mariadb-server" "sqlite3" "isc-dhcp-server" "hostapd" "tor" "i2pd" "mpv" "mplayer" "vlc"
    "ffmpeg" "yt-dlp" "python3" "python3-pip" "python3-requests" "python3-bs4" "python3-lxml"
    "adb" "nmap" "aircrack-ng" "john" "hydra" "hashcat" "metasploit-framework" "radare2"
    "binwalk" "strace" "lsof" "tcpdump" "wireshark" "iperf3" "dnsutils" "whois"
    "netcat-traditional" "socat" "proxychains" "minicom" "mosh" "screen" "autossh" "ansible" "rclone"
    "espeak-ng"
)

# Install system packages
sudo apt install -y "${SYSTEM_PACKAGES[@]}"

# Essential Python packages
PIP_PACKAGES=(
    "requests" "beautifulsoup4" "lxml" "flask" "django" "scapy" "paramiko" "numpy"
    "pandas" "matplotlib" "notebook" "jupyterlab" "sqlalchemy" "pyopenssl" "cryptography"
    "twisted" "meshtastic" "ansible" "tensorflow" "torch" "keras" "opencv-python" "pyserial"
)

# Download and cache Python packages
echo "Downloading Python packages..."
pip3 download --dest "$PIP_CACHE" "${PIP_PACKAGES[@]}"

# Networking and Mesh tools
NETWORK_PACKAGES=(
    "batctl" "cjdns" "yggdrasil" "olsrd" "iperf3" "tcpdump" "wireshark" "babeld" "bird"
    "net-tools" "zabbix-agent"
)

echo "Installing mesh networking tools..."
sudo apt install -y "${NETWORK_PACKAGES[@]}"

# Additional tools for security and offline management
ADDITIONAL_PACKAGES=(
    "darkhttpd" "caddy" "syncthing" "rsnapshot" "restic" "borgbackup" "duplicity"
    "gpg" "ccrypt" "veracrypt" "ranger" "mc" "fzf" "bat" "exa" "tldr" "jq" "yq"
)

echo "Installing additional tools..."
sudo apt install -y "${ADDITIONAL_PACKAGES[@]}"

# **Download all available Lubuntu packages for offline installation**
echo "Downloading all available Lubuntu packages for offline use..."
sudo apt download --yes $(apt list --installed | cut -d/ -f1) -o Dir::Cache="$UBUNTU_REPO"

# **Create a local offline repository**
echo "Creating local Lubuntu repository..."
mkdir -p "$UBUNTU_REPO/dists/stable/main/binary-amd64"
cp "$UBUNTU_REPO"/*.deb "$UBUNTU_REPO/dists/stable/main/binary-amd64"
cd "$UBUNTU_REPO/dists/stable/main/binary-amd64"
dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz
cd ~

# **Configure APT to use the offline repository**
LOCAL_REPO="deb [trusted=yes] file://$UBUNTU_REPO stable main"
if ! grep -q "$LOCAL_REPO" /etc/apt/sources.list; then
    echo "Adding local repository to sources.list..."
    echo "$LOCAL_REPO" | sudo tee -a /etc/apt/sources.list
fi

# **Refresh APT database**
echo "Refreshing APT package database..."
sudo apt update

# Clone survival resources
echo "Cloning survival resources repository..."
git clone --depth=1 "https://github.com/TheGodRX/offgrid.git" "$BASE_DIR/HOME" || { echo "Git clone failed!"; exit 1; }

# Finished
echo "All resources downloaded! You can now install packages offline."
echo "Run 'python3 offgrid1.0.py' to complete resource setup."
