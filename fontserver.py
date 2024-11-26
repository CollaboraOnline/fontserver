#!/usr/bin/env python3
# -*- tab-width: 4; indent-tabs-mode: nil; py-indent-offset: 4 -*-
#
# Copyright the Collabora Online contributors.
#
# SPDX-License-Identifier: MPL-2.0
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import os
import hashlib
import json
from flask import Flask, send_from_directory, jsonify

app = Flask(__name__)

FONT_DIR = "/app/fonts"
JSON_FILE = "fonts.json"
SERVER_BASE_URL = os.getenv("SERVER_BASE_URL", "https://127.0.0.1:5000")

def generate_md5(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def generate_fonts_json():
    fonts = []
    os.makedirs(FONT_DIR, exist_ok=True)
    for font in os.listdir(FONT_DIR):
        if font.lower().endswith((".ttf", ".otf")):
            font_path = os.path.join(FONT_DIR, font)
            md5_stamp = generate_md5(font_path)
            font_uri = f"{SERVER_BASE_URL}/fonts/{font}"
            fonts.append({"uri": font_uri, "stamp": md5_stamp})

    data = {"kind": "fontconfiguration", "server": SERVER_BASE_URL, "fonts": fonts}

    with open(JSON_FILE, "w") as json_file:
        json_file.write(json.dumps(data, indent=4))

@app.route("/fonts/<path:filename>")
def serve_fonts(filename):
    return send_from_directory(FONT_DIR, filename)

@app.route("/fonts.json")
def serve_fonts_json():
    return send_from_directory(".", JSON_FILE)

if __name__ == "__main__":
    generate_fonts_json()
    app.run(host="0.0.0.0", port=5000, ssl_context=('server.crt', 'server.key'))

# vim: set shiftwidth=4 softtabstop=4 expandtab:
