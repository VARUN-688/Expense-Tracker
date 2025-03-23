[app]
# App details
title = Mobile Expense Tracker
package.name = mobileexpensetracker
package.domain = com.example
source.include_exts = py,png,jpg,kv,atlas
source.entrypoint = main.py
version = 1.0.0

# Dependencies
requirements = python3, kivy, kivy-garden, garden.matplotlib, pandas, numpy, matplotlib, plyer, requests

# Android permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Orientation
android.orientation = portrait

# Icon and splash screen (if applicable)
icon.filename = icon.png

# Hide the title bar
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app.android]
# Increase min API level if needed (default: 21)
android.minapi = 21

# Package format
android.arch = arm64-v8a
