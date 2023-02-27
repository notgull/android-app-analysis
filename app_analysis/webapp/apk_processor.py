# GNU AGPL v3 License
# Written by John Nunley
# Process APK files to find the vulnerabilities

import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
from gplaycli.gplaycli import GPlaycli
from os import path

# Download the APK file from Google Play
def download_apk(app_id):
    gplaycli = GPlaycli(
        config_file=path.join(path.dirname(__file__), "gplaycli.conf")
    )
    gplaycli.download([(app_id, f"{app_id}.apk")])

if __name__ == "__main__": 
    download_apk("com.zhiliaoapp.musically")
