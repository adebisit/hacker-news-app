from django.contrib import admin
from .models import Author, BaseItem


# Register your models here.

class BaseItemInline(admin.TabularInline):
    model = BaseItem


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("username", "created", "karma", "no_submitted")
    inlines = [BaseItemInline]

@admin.register(BaseItem)
class BaseItemAdmin(admin.ModelAdmin):
    list_display = (
        "item_type",
        "created_date",
        "author",
        "url",
        "score"
    )
    inlines = [BaseItemInline]