#!/bin/bash
set -e  # Exit on error

# Define directories
BASE_DIR="$HOME/offline_survival_resources"
PIP_CACHE="$HOME/.cache/pip"
PACKAGE_CACHE="$HOME/package_cache"
ARCH_REPO="$HOME/archbang_package_cache"
mkdir -p "$BASE_DIR" "$PIP_CACHE" "$PACKAGE_CACHE" "$ARCH_REPO"

# Essential system tools (explicitly choose netcat version, and fix `fastboot` and `espeak`)
SYSTEM_PACKAGES=(
    "base-devel" "linux-headers" "git" "wget" "curl" "rsync" "vim" "nano" "pluma" "tmux"
    "htop" "ufw" "iptables" "wireguard-tools" "openvpn" "dnsmasq" "nginx" "apache" "php"
    "mariadb" "sqlite" "dhcp" "hostapd" "tor" "i2pd" "mpv" "mplayer" "vlc" "ffmpeg"
    "yt-dlp" "python" "python-pip" "python-requests" "python-beautifulsoup4" "python-lxml"
    "android-tools" "nmap" "aircrack-ng" "john" "hydra" "hashcat" "metasploit" "radare2"
    "binwalk" "strace" "lsof" "tcpdump" "wireshark-cli" "iperf3" "dnsutils" "whois"
    "gnu-netcat" "socat" "proxychains-ng" "minicom" "mosh" "screen" "autossh" "ansible" "rclone"
    "espeak-ng"  # `espeak-ng` instead of `espeak`
)

# Install system packages and cache updates
echo "Updating system and installing essential system packages..."
sudo pacman -Syu --noconfirm
sudo pacman -S --noconfirm "${SYSTEM_PACKAGES[@]}"
sudo pacman -Syw --cachedir "$PACKAGE_CACHE"

# Essential Python packages
PIP_PACKAGES=(
    "requests" "beautifulsoup4" "lxml" "flask" "django" "scapy" "paramiko" "numpy"
    "pandas" "matplotlib" "notebook" "jupyterlab" "sqlalchemy" "pyopenssl" "cryptography"
    "twisted" "meshtastic" "ansible" "tensorflow" "torch" "keras" "opencv-python" "pyserial"
)

# Download and cache Python packages
echo "Downloading Python packages..."
pip download --dest "$PIP_CACHE" "${PIP_PACKAGES[@]}"

# Networking and Mesh tools
NETWORK_PACKAGES=(
    "batman-adv" "cjdns" "badvpn" "yggdrasil" "freifunk-watchdog" "mesh11sd" "olsrd"
    "olsrd-gui" "iperf3" "tcpdump" "wireshark-cli" "babeld" "bird" "babeltrace"
    "net-tools" "zabbix-agent"
)

echo "Installing mesh networking tools..."
sudo pacman -S --noconfirm "${NETWORK_PACKAGES[@]}"

# Additional tools for security and offline management
ADDITIONAL_PACKAGES=(
    "darkhttpd" "caddy" "syncthing" "iperf3" "autossh" "rsnapshot" "restic" "borg"
    "duplicity" "gpg" "ccrypt" "veracrypt" "ranger" "mc" "fzf" "bat" "exa" "tldr"
    "jq" "yq"
)

echo "Installing additional tools..."
sudo pacman -S --noconfirm "${ADDITIONAL_PACKAGES[@]}"

# **Download all available ArchBang packages for offline installation**
echo "Downloading all available ArchBang packages for offline use..."
sudo pacman -Syw --cachedir "$ARCH_REPO" --noconfirm $(pacman -Sqq)

# **Set up a local repository**
echo "Creating local ArchBang repository..."
repo-add "$ARCH_REPO/custom.db.tar.gz" "$ARCH_REPO"/*.pkg.tar.zst

# **Configure pacman to use the offline repo**
PACMAN_CONF="/etc/pacman.conf"
if ! grep -q "\[custom\]" "$PACMAN_CONF"; then
    echo "Adding local repository to pacman.conf..."
    echo -e "\n[custom]\nSigLevel = Optional TrustAll\nServer = file://$ARCH_REPO" | sudo tee -a "$PACMAN_CONF"
fi

# **Refresh pacman database**
echo "Refreshing pacman database..."
sudo pacman -Sy

# Ensure git is installed and cloning the repository
echo "Ensure Git is installed and cloning the survival resources from GitHub..."
git clone --depth=1 "https://github.com/TheGodRX/offgrid.git" "$BASE_DIR/HOME" || { echo "Git clone failed!"; exit 1; }

# Finished
echo "All resources downloaded and system ready for offline use!"
echo "Proceed to run python3 offgrid1.0.py to complete resource grabbing."
