from datetime import datetime
from django.db import models
from django.urls import *


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('producttype_list', args=[str(self.name)])

    class Meta:
        ordering = ['name']
        verbose_name = 'product type'
        verbose_name_plural = 'product types'


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL,
                                     related_name='products', null=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('merchstore:product_detail', args=[str(self.pk)])

    class Meta:
        ordering = ['name']
        verbose_name = 'product'
        verbose_name_plural = 'products'
