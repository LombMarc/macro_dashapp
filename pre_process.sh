#!/bin/bash
mkdir -p /tmp/chromium_bin

wget https://github.com/ungoogled-software/ungoogled-chromium-binaries/releases/download/114.0.5735.133-1/chromium_114.0.5735.133-1.1_amd64.deb
dpkg -x chromium_*.deb /tmp/chromium
mv /tmp/chromium/usr/lib/chromium/* /tmp/chromium_bin/

wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d /tmp/chromium_bin/
chmod +x /tmp/chromium_bin/chromedriver

pip install -r requirements.txt