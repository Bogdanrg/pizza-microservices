from django.contrib import admin
from .models import Order, PizzaType, Pizza
from django.utils.safestring import mark_safe


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_status', 'user')
    list_display_links = ('id', 'order_status', 'user')
    search_fields = ('id', )


class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'pizza_size')
    list_display_links = ('id', 'pizza_size')
    search_fields = ('id', )


class PizzaTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'pizza_type_name', 'get_html_photo')
    list_display_links = ('id', 'pizza_type_name')
    search_fields = ('id', )
    readonly_fields = ('get_html_photo', )

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=50px>')

    get_html_photo.short_description = 'Pizza'



admin.site.register(PizzaType, PizzaTypeAdmin)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Order, OrderAdmin)
