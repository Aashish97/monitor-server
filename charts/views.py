import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Server, CPUDetail, RAMDetail, SwapDetail, DiskUsageDetail, NetworkUsage, OtherDetail
from .helpers import create_server_detail_according_to_class, create_server_other_details


def show_stats(request):
    context = {
        "servers": Server.objects.all(),
    }
    return render(request, 'charts/stats.html', context=context)


def show_server_detail(request, pk):
    server = get_object_or_404(Server, pk=pk)
    cpu_detail  = CPUDetail.objects.filter(server=server).latest('created_at')
    ram_usage  = RAMDetail.objects.filter(server=server).latest('created_at')
    swap_usage  = SwapDetail.objects.filter(server=server).latest('created_at')
    disk_usage  = DiskUsageDetail.objects.filter(server=server).latest('created_at')
    other_detail  = OtherDetail.objects.filter(server=server).latest('created_at')
    network_detail = NetworkUsage.objects.filter(server=server).latest('created_at')
    context = {
        "server_name": server.name,
        "server_ip": server.ip_address,
        "current_user": other_detail.user,
        "boot_time": other_detail.boot_time,
        "cpu_usage": {
            "User Time": cpu_detail.user_time,
            "System Time": cpu_detail.system_time,
            "Idle Time": cpu_detail.idle_time,
            "Core Count": cpu_detail.cpu_count,
            'CPU usage percent': cpu_detail.cpu_percentage
        },
        "ram_usage": {
            "Total RAM": ram_usage.display_total,
            "Used": ram_usage.display_used,
            "Free": ram_usage.display_free,
            "Percent": ram_usage.percent,
            "Available": ram_usage.display_available
        },
        "swap_usage": {
            "Total Swap": swap_usage.display_total,
            "Used": swap_usage.display_used,
            "Free": swap_usage.display_free,
            "Percent": swap_usage.percent
        },
        "disk_usage": {
            "Total Disk": disk_usage.display_total,
            "Used": disk_usage.display_used,
            "Free": disk_usage.display_free,
            "Percent": disk_usage.percent,
            "Location": disk_usage.location
        },
        "network_usage": {
            "Byte Sent": network_detail.byte_sent,
            "Byte Received": network_detail.bytes_received,
            "Packet Sent": network_detail.packet_sent,
            "Packet Received": network_detail.packet_received,
            "IP Address": network_detail.ip_address
        }
    }
    return render(request, 'charts/server-detail.html', context=context)
  
@csrf_exempt
def server_details(request):
    if request.method.upper() == "POST":
        data = json.loads(request.body)
        server_name = data.get('server')
        server = get_object_or_404(Server, name=server_name)
        boot_time = data.get('boot_time', "N/A")
        user = data.get("user", "N/A")
            
        klasses_mapper = {
            CPUDetail: data.get('cpu_details', {}),
            RAMDetail: data.get('ram_usage', {}),
            SwapDetail: data.get('swap_usage', {}),
            NetworkUsage: data.get('network_usage', {}),
            DiskUsageDetail: data.get('disk_usage', {})
        }
        for klass, data in klasses_mapper.items():
            create_server_detail_according_to_class(klass, server, data)
        create_server_other_details(server, boot_time, user)
    return render(request, 'charts/stats.html')
