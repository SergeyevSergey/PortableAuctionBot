from celery import Celery
from django.utils import timezone
# from .models import Lot
from datetime import timedelta

app = Celery('config')


@app.task
def delete_expired_lots():
    now = timezone.now()
    expired_lots = Lot.objects.filter(expiration_hours__isnull=False, created__lt=now - timedelta(hours=1))
    for lot in expired_lots:
        print(f"Expired lot with id {lot.id}")
        lot.delete()
        print('deleted')
