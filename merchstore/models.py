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
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL,
                                  related_name='products', null=True)
    product_image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    stock = models.PositiveIntegerField()
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('on_sale', 'On Sale'),
        ('out_of_stock', 'Out of Stock'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.status = 'out_of_stock'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('merchstore:product_detail', args=[str(self.pk)])

    class Meta:
        ordering = ['name']
        verbose_name = 'product'
        verbose_name_plural = 'products'

# class Transaction(models.Model):
    # Buyer = models.ForeignKey(Profile, on_delete=models.SET_NULL,
    #                                  related_name='products', null=True)
    # Product = models.ForeignKey(Product, on_delete=models.CASCADE,
    #                                  related_name='transactions', null=True)
    # Amount = models.PositiveIntergerField()
    # STATUS_CHOICES = [
    #     ('on_cart', 'On cart'),
    #     ('to_pay', 'To Pay'),
    #     ('to_ship', 'To Ship'),
    #     ('received', 'Received'),
    #     ('delivered', 'Delivered'),
    # ]

    # status = models.CharField(
    #     max_length=20,
    #     choices=STATUS_CHOICES,
    #     default='on_cart'
    # )
    # Created_On = models.DateTimeField(auto_now_add=True)
