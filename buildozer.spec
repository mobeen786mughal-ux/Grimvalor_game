[app]
title = Grimvalor Game
package.name = grimvalor
package.domain = com.mobeen.grimvalor
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = landscape
fullscreen = 0

[buildozer]
log_level = 2

[app:android]
android.accept_sdk_license_agreement = True
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
p4a.bootstrap = sdl2
