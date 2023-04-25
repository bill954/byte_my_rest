from django.db import models
from admin_settings.models import Color, MeasureUnit, Category, SubCategory
from users.models import User

class Product(models.Model):
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    
    name = models.CharField(max_length=100)
    SKU = models.CharField(max_length=20)
    price = models.FloatField()
    descritpion = models.TextField()
    image = models.ImageField(upload_to='product/images')
    
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    measure_unit = models.ForeignKey(MeasureUnit, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    
    def __str__(self):
        return self.owner.get_full_name() + '-' + self.name
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
class ExtraImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='product/extra-images/')

    def __str__(self):
            return self.product.name + '-' + str(self.id)
        
    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'