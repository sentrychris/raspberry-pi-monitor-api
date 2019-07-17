import os
import sys
import subprocess
import psutil
import datetime

def get_network_info():
    info = {}
    info["ssid"] = get_ssid()
    info["interfaces"] = get_interface_stats()
    info["connections"] = get_connections()

    return info

def get_ssid():
    ssid = subprocess.check_output('iwgetid -r', shell=True).decode().rstrip()

    return ssid

def get_interface_stats():
    interfaces = {}
    for inet,stat in psutil.net_io_counters(pernic=True).items():
        interfaces[inet] = {
            'mb_sent': stat.bytes_sent / (1024.0 * 1024.0),
            'mb_received': stat.bytes_recv / (1024.0 * 1024.0),
            'pk_sent': stat.packets_sent,
            'pk_received': stat.packets_recv,
            'error_in': stat.errin,
            'error_out': stat.errout,
            'dropout': stat.dropout,
        }
    
    return interfaces


def get_connections():
    connections = {}

    for sconn in psutil.net_connections(kind='inet'):
        if sconn.laddr.port == 22 and sconn.status == 'ESTABLISHED':
            connections["ssh"] = {
                "local_port": sconn.laddr.port,
                "remote_ip": sconn.raddr.ip,
            }
    
    return connections
