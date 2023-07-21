import psutil, datetime, requests

def get_cpu_details():
    cpu_times = psutil.cpu_times()
    return {
        "user_time": getattr(cpu_times, 'user', None),
        "system_time": getattr(cpu_times, 'system', None),
        "idle_time": getattr(cpu_times, 'idle', None),
        "cpu_percentage": psutil.cpu_percent(interval=1, percpu=True),
        "cpu_count": psutil.cpu_count()
    }
    
    
def get_ram_usage():
    ram_usage = psutil.virtual_memory()
    return {
        'total': getattr(ram_usage, 'total', None),
        'available': getattr(ram_usage, 'available', None),
        'percent': getattr(ram_usage, 'percent', None),
        'used': getattr(ram_usage, 'used', None),
        'free': getattr(ram_usage, 'free', None)
    }
    

def get_swap_usage():
    swap_usage = psutil.swap_memory()
    return {
        'total': getattr(swap_usage, 'total', None),
        'used': getattr(swap_usage, 'used', None),
        'free': getattr(swap_usage, 'free', None),
        'percent': getattr(swap_usage, 'percent', None),
    }
    
    
def get_disk_usage():
    disk_usage = psutil.disk_usage("/")
    return {
        "location": "home",
        "total": getattr(disk_usage, 'total', None),
        "used": getattr(disk_usage, 'used', None),
        "free": getattr(disk_usage, 'free', None),
        "percent": getattr(disk_usage, 'percent', None)
    }
    

def get_boot_time():
    return datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    

def get_users():
    return psutil.users()[0].name
    
def get_network_usage():
    net_io_counters = psutil.net_io_counters()
    net_connection = psutil.net_connections()
    ip_address = ''
    if net_connection:
        ip_address = net_connection[0].laddr.ip
    return {
        'byte_sent': net_io_counters.bytes_sent,
        'bytes_received': net_io_counters.bytes_recv,
        'packet_sent': net_io_counters.packets_sent,
        'packet_received': net_io_counters.packets_recv,
        'ip_address': ip_address
    }
    

def get_process():
    return {p.pid: p.info for p in psutil.process_iter(['name', 'username'])}
    

def monitor_server():
    URL = "http://127.0.0.1:8085/server-details"
    data = {
        "server": "Localhost",     
        "cpu_details": get_cpu_details(),
        "ram_usage": get_ram_usage(),
        "swap_usage": get_swap_usage(),
        "disk_usage": get_disk_usage(),
        "network_usage": get_network_usage(),
        "boot_time": get_boot_time(),
        "user": get_users(),
        #"processes": get_process()
    }
    requests.post(URL, json=data)
    

if __name__ == "__main__":
    monitor_server()
