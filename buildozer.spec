[app]
title = Folklore Guide
package.name = folkloreguide
package.domain = org.folklore

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 0.1.0

requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,plyer,sdl2_ttf==2.0.15

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
