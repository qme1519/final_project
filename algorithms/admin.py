from django.contrib import admin
from algorithms.models import Category, Algorithm

class AlgorithmAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Algorithm, AlgorithmAdmin)
admin.site.register(Category, CategoryAdmin)
