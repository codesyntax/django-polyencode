from django.contrib import admin
from .models import Place, Polygon


class PolygonInline(admin.TabularInline):
    model = Polygon
    fields = ('limits', 'encode_points',)
    extra = 1


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'geotype', 'parent', 'countPolygonsEx', 'countPolygonsIn', 'countPoints')
    list_display_links = ('name',)
    ordering = ('name', 'geotype')
    search_fields = ['name', ]
    list_filter = ('geotype',)
    inlines = [PolygonInline, ]

admin.site.register(Place, PlaceAdmin)
