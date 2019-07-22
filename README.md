# py-monitor-api

A simple API for monitoring your raspberry Pi.

## How it Works

It's incredibly simple, just submit a GET request to your chosen endpoint to receive data, which will always be returned in JSON format, then you can consume that data with whatever library/language you're using and use it to display information about your Pi.

## Endpoints

#### GET `/system`
Returns a JSON object containing core system information, including:

- **CPU**: temperature, clock speed (frequency) and system-wide usage as a percentage.
- **Disk**: total size (GB), used amount (GB), remaining space (GB) and usage as a percentage.
- **Processes**: top ten processes by memory usage, process information includes name, PID, username and memory (MB).
- **Platform**: distribution name and kernel version.
- **Uptime**: system uptime represented in format "_n_ days, _n_ hours, _n_ minutes and _n_ seconds".

Please refer to the [`system.json`](https://github.com/cversyx/py-monitor/blob/master/tests/system.json) test file for a detailed example.

### GET `/network`
Returns a JSON object containing network information, including:

- **connections**: established UNIX socket connections.
- **interfaces**: network interfaces and send/receive, error and dropout statistics.
- **wifi**: wireless SSID, host MAC address, channel, encryption, signal strength, and quality as a percentage.

Please refer to the [`network.json`](https://github.com/cversyx/py-monitor/blob/master/tests/network.json) test file for a detailed example.

### GET `/network/counter/<interface>`
(e.g. /network/counter/wlan0)

Streams a JSON representation of kB/s sent/received for the chosen interface

## Apache Configuration
Firstly, make sure you have `libapache2-mod-wsgi` installed:

```bash
$ sudo apt install libapache2-mod-wsgi
```

Then create and enable your new virtualhost configuration:

```conf
<VirtualHost *>
    ServerName api.raspberrypi.local

    WSGIDaemonProcess application user=pi group=pi threads=5
    WSGIScriptAlias / /var/www/flaskapps/pymonitorapi/pymonitorapi.wsgi

    <Directory /var/www/flaskapps/pymonitorapi>
        WSGIProcessGroup application
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Require all granted
    </Directory>
</VirtualHost>
```

```bash
$ sudo a2ensite api.raspberrypi.local.conf
$ sudo systemctl reload apache2
```
 
A working example client can be downloaded from [here](https://github.com/cversyx/py-monitor).
