from django.db import models


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = 'product type'
        verbose_name_plural = 'product types'


class Product(models.Model):
    prod_name = models.CharField(max_length=255)
    type = models.ForeignKey(
        ProductType,
        null=True,
        on_delete=models.SET_NULL,
    )
    prod_desc = models.TextField()
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    def __str__(self):
        return self.prodname
    
    class Meta:
        ordering = ["prod_name"]
        verbose_name = 'product'
        verbose_name_plural = 'products'
