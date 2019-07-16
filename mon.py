import os
import platform
import psutil
import datetime

# Get system information
def get_system_info():
    info = {}
    info["cpu"] = get_cpu_info()
    info["disk"] = get_disk_info()
    info["uptime"] = get_system_uptime()
    info["platform"] = get_platform_info()

    info["processes"] = []
    processes = get_processes()
    for process in processes[:10]:
        info["processes"].append((process))

    return info

def get_platform_info():
    info = {}
    info["distro"] = os.popen('cat /etc/*-release | awk NR==1 | cut -c 13-').read().replace('"', '').rstrip()
    info["kernel"] = platform.release()

    return info

# Get system uptime
def get_system_uptime():
    info = {}
    try:
        f = open( "/proc/uptime" )
        contents = f.read().split()
        f.close()
    except:
        return "Cannot open uptime file: /proc/uptime"

    total_seconds = float(contents[0])
    days    = int(total_seconds / 86400)
    hours   = int((total_seconds % 86400) / 3600)
    minutes = int((total_seconds % 3600) / 60)
    seconds = int(total_seconds % 60)

    info["uptime"] = ""
    if days > 0:
        info["uptime"] += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
    if len(info["uptime"]) > 0 or hours > 0:
        info["uptime"] += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
    if len(info["uptime"]) > 0 or minutes > 0:
        info["uptime"] += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
    info["uptime"] += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )

    return info

# Get CPU usage
def get_cpu_info():
    info = {}
    info['usage'] = psutil.cpu_percent(interval=1)
    info["temp"] = psutil.sensors_temperatures()['cpu-thermal'][0].current
    info['freq'] = psutil.cpu_freq().current

    return info

# Get disk information
def get_disk_info():
    info = {}
    disk = psutil.disk_usage('/')

    info["total"] = disk.total / (1024.0 ** 3)
    info["used"] = disk.used / (1024.0 ** 3)
    info["free"] = disk.free / (1024.0 ** 3)
    info["percent"] = disk.percent

    return info

# Get processes sorted by memory
def get_processes():
    processes = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
            processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    processes = sorted(processes, key=lambda procObj: procObj['vms'], reverse=True)

    return processes
