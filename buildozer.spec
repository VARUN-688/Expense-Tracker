[app]
# (str) Title of your application
title = Mobile Expense Tracker

# (str) Package name
package.name = mobileexpensetracker

# (str) Package domain (must be unique)
package.domain = com.example

# (str) Source code directory
source.dir = .

# (str) The entry Python file of the application (e.g., main.py)
source.entrypoint = main.py

# (list) Extensions to include in the source distribution
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 1.0.0

# (list) Application requirements
requirements = python3, kivy, kivy-garden, garden.matplotlib, pandas, numpy, matplotlib, plyer, requests

# (list) Permissions for Android
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Fullscreen mode (1 = enable, 0 = disable)
fullscreen = 0

# (str) Icon filename (must be in the root directory)
icon.filename = icon.png

# (str) Android orientation (landscape, portrait, sensor, etc.)
android.orientation = portrait

# (bool) Enable Android hardware acceleration
android.hardware.accelerated = True

# (str) Application platform (android, ios, etc.)
p4a.branch = master

# (str) Minimum API level required (21 = Android 5.0+)
android.minapi = 21

# (str) Architecture to support (arm64-v8a = 64-bit)
android.archs = arm64-v8a, armeabi-v7a


# (bool) Enable keyboard mode
input.enable = True

# (bool) Indicate if the app should be built in release mode
release = False

# (list) Additional Java classes to include
android.add_jars = 

# (list) Additional files to include in the APK
android.include_exts = 

# (bool) Allow compilation on root (0 = no, 1 = yes)
warn_on_root = 1

[buildozer]
# (int) Log level (0 = silent, 1 = error, 2 = warning, 3 = info, 4 = debug)
log_level = 2
