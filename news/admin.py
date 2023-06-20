from django.contrib import admin
from .models import Author, Item


class ItemInline(admin.TabularInline):
    model = Item


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("username", "created", "karma", "no_submitted")
    inlines = [ItemInline]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "created_date",
        "author",
        "url",
        "score"
    )
    inlines = [ItemInline]