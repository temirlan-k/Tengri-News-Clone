from django.contrib import admin
from .models import *


class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
class CategoryAdmin(admin.ModelAdmin):
    pass
class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(NewsPost, NewsPostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
