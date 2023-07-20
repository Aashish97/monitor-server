from .models import OtherDetail


def create_server_other_details(server, boot_time, user):
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
