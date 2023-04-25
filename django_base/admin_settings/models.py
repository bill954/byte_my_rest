from django.db import models

class Color(models.Model):
    name = models.CharField(max_length=70)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colores'
        
class MeasureUnit(models.Model):
    name = models.CharField(max_length=70)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Unidad de medida'
        verbose_name_plural = 'Unidades de medida'
        
class Category(models.Model):
    name = models.CharField(max_length=70)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        
class SubCategory(models.Model):
    name = models.CharField(max_length=70)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category')
    
    def __str__(self):
        return self.category.name + '-' + self.name
    
    class Meta:
        verbose_name = 'SubCategoría'
        verbose_name_plural = 'SubCategorías'