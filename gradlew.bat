@echo off
setlocal
set "ROOT=%~dp0"
set "VER=8.13"
set "CACHE=%ROOT%.gradle-bootstrap\gradle-%VER%"
if exist "%CACHE%\bin\gradle.bat" goto run
if not exist "%ROOT%.gradle-bootstrap" mkdir "%ROOT%.gradle-bootstrap"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://services.gradle.org/distributions/gradle-%VER%-bin.zip' -OutFile '%ROOT%.gradle-bootstrap\gradle.zip'"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Force '%ROOT%.gradle-bootstrap\gradle.zip' '%ROOT%.gradle-bootstrap\unpack'"
move "%ROOT%.gradle-bootstrap\unpack\gradle-%VER%" "%CACHE%"
rmdir /s /q "%ROOT%.gradle-bootstrap\unpack"
del "%ROOT%.gradle-bootstrap\gradle.zip"
:run
call "%CACHE%\bin\gradle.bat" %*
