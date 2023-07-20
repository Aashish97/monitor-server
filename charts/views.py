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
        "current_user": other_detail.user,
        "boot_time": other_detail.boot_time,
        "cpu_usage": {
            "user_time": cpu_detail.user_time,
            "system_time": cpu_detail.system_time,
            "idle_time": cpu_detail.idle_time,
            "cpu_count": cpu_detail.cpu_count,
            'cpu_percentage': cpu_detail.cpu_percentage
        },
        "ram_usage": {
            "total_ram": ram_usage.total,
            "used": ram_usage.used,
            "free": ram_usage.free,
            "percent": ram_usage.percent,
            "available": ram_usage.available
        },
        "swap_usage": {
            "total_swap": swap_usage.total,
            "used": swap_usage.used,
            "free": swap_usage.free,
            "percent": swap_usage.percent
        },
        "disk_usage": {
            "total_disk_usage": disk_usage.total,
            "used": disk_usage.used,
            "free": disk_usage.free,
            "percent": disk_usage.percent,
            "location": disk_usage.location
        },
        "network_usage": {
            "byte_sent": network_detail.byte_sent,
            "bytes_received": network_detail.bytes_received,
            "packet_sent": network_detail.packet_sent,
            "packet_received": network_detail.packet_received,
            "ip_address": network_detail.ip_address
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
