[app]
title = Mobile Expense Tracker
package.name = expense_tracker
package.domain = com.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,kivy-garden,pandas,numpy,matplotlib,sqlite3,plyer
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 34
android.minapi = 21
android.ndk = 25.2.9519653
android.archs = arm64-v8a, armeabi-v7a
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.gradle_dependencies = "androidx.appcompat:appcompat:1.2.0"

[build]
exclude_exts = spec
