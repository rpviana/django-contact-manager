from django.contrib import admin
from contact import models

# Register your models here.
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display =('name',)
    ordering = ('name',)

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','phone')
    ordering = ('-first_name',)
    list_filter = ('created_date',)
    search_fields = ('first_name','phone',)
    list_per_page = 10 # Nº de contatos por página
    list_max_show_all = 200
    list_display_links = ('first_name',)