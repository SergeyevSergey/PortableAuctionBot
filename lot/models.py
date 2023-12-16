from django.db import models
# from celery import Celery
from django.utils import timezone
from datetime import timedelta
import threading
# Create your models here.
# app = Celery('config')


class CustomUser(models.Model):
    user_id = models.CharField(verbose_name='User id', max_length=20)

    class Meta:
        verbose_name = 'Custom user'
        verbose_name_plural = 'Custom users'

    def __str__(self) -> str:
        return f'{self.user_id}'


class Lot(models.Model):
    user_id = models.CharField(verbose_name='User id', max_length=20)
    description = models.TextField(verbose_name='Description', max_length=250)
    start_price = models.DecimalField(verbose_name='Start Price', max_digits=12, decimal_places=2)
    image_url = models.CharField(verbose_name='Image Url', max_length=200)
    expiration_hours = models.PositiveSmallIntegerField(default=24)
    current_applicant = models.CharField(verbose_name='Current Applicant', max_length=100)
    current_price = models.DecimalField(verbose_name='Current Price', max_digits=12, decimal_places=2)
    bidders = models.ManyToManyField(CustomUser, through='UserBid', related_name='bids')

    class Meta:
        verbose_name = 'Lot'
        verbose_name_plural = 'Lots'

    def __str__(self) -> str:
        return f'{self.user_id, self.description[:15]}'


class UserBid(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='User', on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, verbose_name='Lot', on_delete=models.CASCADE)
    bid_cost = models.DecimalField(verbose_name='Bid cost', max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'User bid'
        verbose_name_plural = 'User bids'
        unique_together = ('user', 'lot')

    def __str__(self) -> str:
        return f'{self.pk, self.user, self.lot}'

