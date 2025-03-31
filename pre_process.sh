#!/bin/bash

wget https://github.com/ungoogled-software/ungoogled-chromium-binaries/releases/download/114.0.5735.133-1/chromium_114.0.5735.133-1.1_amd64.deb
dpkg -x chromium_*.deb /tmp/chromium
mv /tmp/chromium/usr/lib/chromium/* /usr/bin/


wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d /usr/bin/
chmod +x /usr/bin/chromedriver

pip install -r requirements.txt