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

It will always return data in JSON format, you can then parse it with whatever library/language you're using and use it to
display information about your Pi.

For example, you could use klein and twig:

`bootstrap.php`
```php
<?php

use App\ApiCaller\Monitor;
use Klein\Klein;
use Twig\Environment;
use Twig\Loader\FilesystemLoader;

require __DIR__ . '/../vendor/autoload.php';

$loader = new FilesystemLoader(__DIR__ . '/../resources/views');
$view = new Environment($loader, [
    'cache' => __DIR__ . '/../public/cache',
]);

$router = new Klein();
$monitor = new Monitor();
```

 ```index.php```
 ```php
 <?php

require_once __DIR__ . '/../config/bootstrap.php';

$router->respond('GET', '/', function () use ($monitor, $view)
{
    $response = $monitor->run();

    if ($response && $response->getStatusCode() === 200) {
        $data = toArray(json_decode($response->getBody()->getContents()));
    } else {
        $data = [
            "error" => true,
            "message" => "There was an error fetching data, please check the logs."
        ];
    }
    
    return $view->render('monitor.twig', $data);
});

$router->dispatch();
 ```
 
 ```Monitor.php```
 
 ```php
 <?php

namespace App\PyMonitor;

use GuzzleHttp\Client;
use GuzzleHttp\Exception\GuzzleException;

class Monitor
{

    private $client;

    public function __construct()
    {
        $this->client = new Client([
            'base_uri' => 'http://api.py-monitor.local',
        ]);
    }

    public function run()
    {
        try {
            return $this->client->request('GET', '/monitor');
        } catch (GuzzleException $e) {
            echo $e->getMessage();
            return false;
        }
    }
}
 ```
 
 ```monitor.twig```
 
 ```html
 <!DOCTYPE html>
<html lang="en">
<head>
    <title>Py Monitor | Raspberry Pi System Monitor</title>
    <meta http-equiv="refresh" content="300">

    <link rel="stylesheet" href="css/bundle.min.css">
    <link rel="stylesheet" href="css/app.min.css">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <a class="navbar-brand" href="#">PyMonitor</a>

    <div class="navbar ml-auto">
        <ul class="navbar-nav mr-auto">
            <li class="nav-item">
                <small>
                    {{ data.platform.distro }} ({{ data.platform.kernel }})
                    <br>
                    Uptime: {{ data.uptime.uptime }}
                </small>
            </li>
        </ul>
    </div>
</nav>

<div class="container my-5">
    <div class="row my-5">
        <div class="col-md-6">
            <table class="table table-sm">
                <thead>
                <tr>
                    <th scope="col">CPU Temp</th>
                    <th scope="col">CPU Freq</th>
                    <th scope="col">CPU Usage</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td scope="row">{{ data.cpu.temp|round }}°C</td>
                    <td scope="row">{{ data.cpu.freq }}MHz</td>
                    <td scope="row">{{ data.cpu.usage }}%</td>
                </tr>
                </tbody>
            </table>
        </div>
        <div class="col-md-6">
            <table class="table table-sm">
                <thead>
                <tr>
                    <th scope="col">Disk Used</th>
                    <th scope="col">Disk Free</th>
                    <th scope="col">Disk Total</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td scope="row">{{ data.disk.used|round }}GB</td>
                    <td scope="row">{{ data.disk.free|round }}GB</td>
                    <td scope="row">{{ data.disk.total|round }}GB</td>
                </tr>
                </tbody>
            </table>
        </div>
    </div>
    <div class="row my-5">
        <div class="col-md-12">
            <table class="table table-sm">
                <thead>
                <tr>
                    <th scope="col">Name</th>
                    <th scope="col">PID</th>
                    <th scope="col">User</th>
                    <th scope="col">VMS</th>
                </tr>
                </thead>
                <tbody>
                {% for proc in data.processes %}
                    <tr>
                        <td>{{ proc.name }}</td>
                        <td>{{ proc.pid }}</td>
                        <td>{{ proc.username }}</td>
                        <td>{{ proc.vms}}</td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
<script type="text/javascript" src="js/bundle.min.js"></script>
<script type="text/javascript" src="js/app.min.js"></script>
</body>
</html>
 ```
 
 A working example can be found [here](https://github.com/cversyx/py-monitor).
