[app]

# (str) Title of your application
title = Easy Worship App

# (str) Package name
package.name = easyworshipapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.easyworship

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.1.0,requests,beautifulsoup4,lxml,html5lib

# (str) Supported orientation (landscape, sensorLandscape, portrait, all)
orientation = all

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 23b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable tablet support and optimization
android.supports_screens = small,normal,large,xlarge

# (str) Android theme
android.theme = "@android:style/Theme.NoTitleBar"

# (list) Android application meta-data to set
android.meta_data = 

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Enable Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for backup rules (Android API >=23)
android.backup_rules =

# (str) If you need to insert variables into your AndroidManifest.xml file,
# you can do so with the following syntax:
# android.manifest.placeholders = holo_blue_bright:#0099CC

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
bin_dir = ./bin
