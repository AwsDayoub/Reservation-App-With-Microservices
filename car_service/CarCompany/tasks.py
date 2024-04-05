from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Car
from .serializer import CarSerializer


@shared_task
def change_car_status(car_id):
    try:
        car = Car.objects.get(id=car_id)
        if car.reserved:
            car.reserved = False
            car.save()
            serializer = CarSerializer(data=car)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "car_status",
                {
                    "type": "car_status_changed",
                    "message": serializer.data,  
                },
            )
            return f"Car {car_id} status changed to available"
        else:
            return f"Car {car_id} is already available"
    except Car.DoesNotExist:
        return f"Car {car_id} not found"