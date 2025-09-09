from django.contrib import admin
from .models import Quote, Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'quote_count']
    list_filter = ['type']


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['text_short', 'source', 'weight', 'views', 'likes', 'dislikes']
    list_editable = ['weight']
    list_filter = ['source']

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_short.short_name = 'Текст'