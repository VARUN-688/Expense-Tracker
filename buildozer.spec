[app]
title = YourAppName
package.name = yourapp
package.domain = org.example
source.dir = app  # Ensure this matches your app folder
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3, kivy, kivy-garden, pandas, numpy, matplotlib
orientation = portrait
fullscreen = 1
android.api = 33
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.minapi = 21
android.packaging_mode = default
android.permissions = INTERNET, STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
