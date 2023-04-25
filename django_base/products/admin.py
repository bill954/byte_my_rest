from django.contrib import admin
from products.models import Product, ExtraImage

class ExtraImageInLine(admin.TabularInline):
    model = ExtraImage
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ExtraImageInLine,]
    
admin.site.register(Product, ProductAdmin)