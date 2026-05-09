from .models import Product, Transaction
from accounts.models import Profile

class ProductFilterStrategy:
    def filter(self, user):
        raise NotImplementedError

class OwnProductsStrategy(ProductFilterStrategy):
    def filter(self, user):
        profile = Profile.objects.get(user=user)
        return Product.objects.filter(owner=profile)

class OtherProductsStrategy(ProductFilterStrategy):
    def filter(self, user):
        profile = Profile.objects.get(user=user)
        return Product.objects.exclude(owner=profile)

class AllProductsStrategy(ProductFilterStrategy):
    def filter(self, user):
        return Product.objects.all()