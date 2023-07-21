def create_server_other_details(server, boot_time, user):
    from .models import OtherDetail
    OtherDetail.objects.create(
            server=server,
            boot_time=boot_time,
            user=user
    )


def create_server_detail_according_to_class(klass, server, data):
    klass.objects.create(
        server=server,
        **data
    )
    

def pretty_display_specs(value):
        value = round(value / (1024 * 1024), 2)
        return f"{value} MB" if value < 1000 else f"{round(value/1024, 2)} GB"
    
    
def get_class_name_from_instance(instance):
    return instance._meta.object_name


def stringify_time(seconds):
    """Converts seconds into hour minute seconds
    
    Example: 
        input = 12122
        output = 3 hours 22 minutes 2 seconds
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    mapper = {
        "hours": h,
        "minutes": m,
        "seconds": s
    }
    out = ""
    for key, val in mapper.items():
        if val:
            if val == 1:
                key = key.replace("s", "")
            out += f"{val} {key} "
    return out


def humanize_interval(interval):
    if not interval:
        return "N/A"
    elif isinstance(interval, float):
        return stringify_time(int(interval))
    elif isinstance(interval, int):
        return stringify_time(interval)
    return interval
