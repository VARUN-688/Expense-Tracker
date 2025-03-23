[app]
title = Mobile Expense Tracker
package.name = mobileexpensetracker
package.domain = com.example
source.dir = .
version = 1.0
requirements = python3,kivy,kivy-garden,pandas,numpy,matplotlib
android.api = 31
android.archs = arm64-v8a,armeabi-v7a
android.ndk = 23b
android.minapi = 21
android.gradle_dependencies = com.android.support:multidex:1.0.3
p4a.branch = master
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
