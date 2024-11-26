
# Simple Fontserver for Collabora Online

This is a simple Flask-based application that serves font files for Collabora Online's [remote font configuration](https://sdk.collaboraonline.com/docs/installation/Configuration.html#enable-download-and-availability-of-more-fonts-by-pointing-to-a-font-configuration-file) feature. It is intended to run this application as a docker container. The app generates a `fonts.json` and the webserver serves it. This file contains metadata about the available fonts, including the font file URIs and MD5 hashes.

**Note:** This application is not for production, only for development and testing.

## Build and Run:

### Step 1: Copy font files to `fonts/` subdirectory.
TrueType and OpenType fonts are supported. The file names and file extensions are case-insensitive, so e.g. both `TTF` and `ttf` extensions are allowed.

### Step 2: Copy SSL certificate files to the work directory
Collabora Online production builds do not allow remote configuration over plain HTTP protocol. HTTPS is required. Therefore either you should copy `server.crt` and `server.key` files from a trusted Certificate Authority (CA) to the work directory, or you can generate a self signed certificate with the following commands:

```bash
openssl genpkey -algorithm RSA -out server.key
openssl req -new -key server.key -out server.csr
openssl x509 -req -in server.csr -signkey server.key -out server.crt
```

### Step 3: Build the Docker image
To build the Docker image, run the following command:

```bash
docker build -t fontserver .
```

### Step 4: Run the Docker container
To run the container and mount your `fonts/` directory, use the following command:

```bash
docker run -d -p 5000:5000 -v $(pwd)/fonts:/app/fonts fontserver
```

This will:
- Start the Flask application on port 5000.
- Mount the `fonts/` directory from your host to `/app/fonts` in the container.

Optionally:
- You can pass `SERVER_BASE_URL` environment variable. The built-in value is `https://127.0.0.1:5000`. For example:

```bash
docker run -d -p 5000:5000 -e SERVER_BASE_URL=https://192.168.100.60:5000 -v $(pwd)/fonts:/app/fonts fontserver
```

### Step 5: Set up Collabora Online to use this fontserver
- Either in `/etc/coolwsd/coolwsd.xml` set the `<remote_font_config>`, for example:

```xml
<remote_font_config>
    <url desc="URL of optional JSON file that lists fonts to be included in Online" type="string" default="">https://192.168.100.60:5000/fonts.json</url>
</remote_font_config>
```

- Or pass this setting in the command line, for example when you start a `collabora/code` container, in the `extra_params` environment variable add:

```
--o:remote_font_config.url=https://192.168.100.60:5000/fonts.json
```

---

## License
This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at [http://mozilla.org/MPL/2.0/](http://mozilla.org/MPL/2.0/).
