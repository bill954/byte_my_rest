from django.db import models
from admin_settings.models import Color, MeasureUnit, Category, SubCategory
from users.models import User

class Product(models.Model):
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    
    name = models.CharField(max_length=100)
    SKU = models.CharField(max_length=20)
    price = models.FloatField()
    descritpion = models.TextField()
    image = models.ImageField(upload_to='product/images')
    
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    measure_unit = models.ForeignKey(MeasureUnit, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    
    # The right thing would be not to add null and blank True, but I did it like this and prefer not to change de db now.
    creation_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    is_banned = models.BooleanField(default = False)
    is_distinguished = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
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

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders')
    creation_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    
    mercado_link = models.CharField(max_length=250, null=True, blank=True)
    remainder_sended = models.BooleanField(default=False)
    
    def __str__(self):
        return self.buyer.get_full_name() + 'order' + str(self.id)
    
    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Ordenes'