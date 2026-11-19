from django.contrib import admin

from .models import AboutContent, AboutPhoto, Photo, Service


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slot_code",
        "is_published",
        "show_in_gallery",
        "display_order",
    )
    list_editable = ("is_published", "show_in_gallery", "display_order")
    list_filter = ("is_published", "show_in_gallery")
    search_fields = ("title", "description")
    ordering = ("display_order", "title")


@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not AboutContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AboutPhoto)
class AboutPhotoAdmin(admin.ModelAdmin):
    list_display = ("alt_text", "caption", "is_published", "display_order")
    list_editable = ("is_published", "display_order")
    list_filter = ("is_published",)
    ordering = ("display_order", "id")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "is_published", "display_order")
    list_editable = ("is_published", "display_order")
    list_filter = ("is_published",)
    search_fields = ("title", "description")
    ordering = ("display_order", "title")