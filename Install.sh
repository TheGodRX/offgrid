#!/bin/bash

# Make sure to run this as root (or use sudo)

# Confirm if you want to continue
echo "This will completely wipe your disk /dev/nvme0n1. Are you sure? (y/n)"
read answer
if [[ "$answer" != "y" ]]; then
    echo "Aborting installation."
    exit 1
fi

# Wipe the disk (this will erase everything)
echo "Wiping disk /dev/nvme0n1..."
wipefs --all /dev/nvme0n1
dd if=/dev/zero of=/dev/nvme0n1 bs=1M count=100

# Partition the disk using GPT
echo "Partitioning the disk..."
cfdisk /dev/nvme0n1 << EOF
g
20
2
1
EOF

# Format the partitions
echo "Formatting partitions..."
mkfs.ext4 /dev/nvme0n1p1
mkfs.fat -F32 /dev/nvme0n1p2  # If UEFI, create EFI partition
mkswap /dev/nvme0n1p3
swapon /dev/nvme0n1p3

# Mount the root partition
mount /dev/nvme0n1p1 /mnt
mkdir -p /mnt/boot/efi
mount /dev/nvme0n1p2 /mnt/boot/efi

# Install base system
echo "Installing base system..."
pacstrap /mnt base linux linux-firmware

# Generate fstab
echo "Generating fstab..."
genfstab -U /mnt >> /mnt/etc/fstab

# Chroot into the new system
echo "Chrooting into the new system..."
arch-chroot /mnt /bin/bash <<EOF
# Set the timezone
ln -sf /usr/share/zoneinfo/Region/City /etc/localtime
hwclock --systohc

# Set locale
echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf

# Set the hostname
echo "archbang" > /etc/hostname

# Install and configure GRUB (non-interactive)
pacman -S grub efibootmgr --noconfirm
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GRUB --no-nvram

# Generate GRUB configuration (non-interactive)
grub-mkconfig -o /boot/grub/grub.cfg

# Set up root password
echo "Set the root password:"
passwd

# Create a user
useradd -m -G wheel -s /bin/bash archbanguser
echo "Set the user password for 'archbanguser':"
passwd archbanguser

# Enable the wheel group sudo access
echo "%wheel ALL=(ALL) ALL" > /etc/sudoers.d/90-wheel

EOF

# Exit chroot and unmount
exit

echo "Installation complete. You can now reboot and boot into your new ArchBang system."
