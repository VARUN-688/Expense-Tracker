[app]
title = Mobile Expense Tracker
package.name = expense_tracker
package.domain = com.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3, kivy, kivy-garden, pandas, numpy, matplotlib, pillow
orientation = portrait
fullscreen = 1
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1

[app.android]
android.minapi = 21
android.sdk = 31
android.ndk = 21.4.7075529
android.build_tools = 31.0.0
