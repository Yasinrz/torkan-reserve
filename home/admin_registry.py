from notifications.admin_site import custom_admin_site
from home.admin import (
    Time, TimeAdmin,
    RequestReservation, RequestReservationAdmin,
    Operation, OperationAdmin,
)

custom_admin_site.register(Time, TimeAdmin)
custom_admin_site.register(RequestReservation, RequestReservationAdmin)
custom_admin_site.register(Operation, OperationAdmin)
