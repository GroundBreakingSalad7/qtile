#!/bin/sh

~/.screenlayout/default &
picom --config ~/.config/qtile/picom.conf &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 & eval $(gnome-keyring-daemon -s --components=pkcs11,secrets,ssh,gpg) &

flameshot &
xfce4-power-manager &
nm-applet --indicator &
nextcloud &

# Keyboard stuff
~/.Xkeys
