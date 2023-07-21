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
    

def pretty_display(value):
        value = round(value / (1024 * 1024), 2)
        return f"{value} MB" if value < 1000 else f"{round(value/1024, 2)} GB"
