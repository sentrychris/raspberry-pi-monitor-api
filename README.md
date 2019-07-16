# py-monitor-api

A mini-API for monitoring your raspberry Pi.

## How it works?

It currently only has one endpoint ```http://api.raspberrypi.local/monitor``` which returns the following:

```json
{
    "data": {
        "cpu": {
            "freq": 600,
            "temp": 49.66,
            "usage": 0.3
        },
        "disk": {
            "free": 20.271629333496094,
            "percent": 21.9,
            "total": 27.354976654052734,
            "used": 5.671802520751953
        },
        "platform": {
            "distro": "Raspbian GNU/Linux 10 (buster)",
            "kernel": "4.19.57-v7l+"
        },
        "processes": [
            {
                "name": "apache2",
                "pid": 24070,
                "username": "pi",
                "vms": 278
            },
            {
                "name": "apache2",
                "pid": 24071,
                "username": "www-data",
                "vms": 210
            },
            {
                "name": "apache2",
                "pid": 24072,
                "username": "www-data",
                "vms": 210
            },
            {
                "name": "apache2",
                "pid": 24073,
                "username": "www-data",
                "vms": 210
            },
            {
                "name": "apache2",
                "pid": 24074,
                "username": "www-data",
                "vms": 210
            },
            {
                "name": "apache2",
                "pid": 24075,
                "username": "www-data",
                "vms": 210
            },
            {
                "name": "apache2",
                "pid": 24084,
                "username": "www-data",
                "vms": 210
            },
            {
                "name": "apache2",
                "pid": 24066,
                "username": "root",
                "vms": 209
            },
            {
                "name": "php-fpm7.3",
                "pid": 12851,
                "username": "root",
                "vms": 207
            },
            {
                "name": "php-fpm7.3",
                "pid": 12852,
                "username": "www-data",
                "vms": 207
            }
        ],
        "uptime": {
            "uptime": "2 days, 21 hours, 7 minutes, 21 seconds"
        }
    }
}
```

```
cpu:
    - freq: Current clock speed
    - temp: Current temperature
    - usage: Average system-wide usage
    
disk:
    - free: Free disk space (GB)
    - percent: Percentage in use
    - total: Total disk space (GB)
    - used: Used disk space (GB)
    
 processes:
    - name: Process name
    - pid: Process ID
    - user: Process owner
    - vms: Virtual memory size
uptime:
    - uptime: system uptime in days, hours, minutes and seconds
```

It will always return data in JSON format, you can then parse it with whatever library/language you're using and use it to
display information about your Pi.
 
 A working example client can be downloaded from [here](https://github.com/cversyx/py-monitor).
