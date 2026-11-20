from django.contrib import admin

from .models import (
    AboutContent,
    AboutPhoto,
    ContactLink,
    GalleryChapter,
    OtherPageContent,
    PortfolioPhoto,
    Service,
    SlideshowPhoto,
)

admin.site.site_header = "Hiltunen Photography | Sisällönhallinta"
admin.site.site_title = "Hiltunen Photography"
admin.site.index_title = "Valitse muokattava sisältö"


class PortfolioPhotoInline(admin.TabularInline):
    model = PortfolioPhoto
    verbose_name = "portfolio-kuva"
    verbose_name_plural = "Tämän luvun kuvat"
    fields = ("title", "image", "description", "is_published", "display_order")
    extra = 1
    ordering = ("display_order", "title")


@admin.register(GalleryChapter)
class GalleryChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "display_order")
    list_editable = ("is_published", "display_order")
    list_filter = ("is_published",)
    search_fields = ("title", "description")
    ordering = ("display_order", "id")
    inlines = (PortfolioPhotoInline,)
    fieldsets = (
        ("Kategorian tiedot", {"fields": ("title", "description", "cover_image")}),
        ("Julkaisu ja järjestys", {"fields": ("is_published", "display_order")}),
    )


@admin.register(PortfolioPhoto)
class PortfolioPhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "chapter", "is_published", "display_order")
    list_editable = ("is_published", "display_order")
    list_filter = ("chapter", "is_published")
    search_fields = ("title", "description")
    ordering = ("chapter__display_order", "display_order", "title")
    fieldsets = (
        ("Kuvan tiedot", {"fields": ("title", "image", "description")}),
        (
            "Portfolio-sijainti ja julkaisu",
            {"fields": ("chapter", "is_published", "display_order")},
        ),
    )


@admin.register(SlideshowPhoto)
class SlideshowPhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "slot_code", "is_published")
    list_editable = ("is_published",)
    list_filter = ("is_published",)
    search_fields = ("title",)
    ordering = ("slot_code",)
    fieldsets = (
        ("Diaesityksen kuva", {"fields": ("title", "image", "slot_code")}),
        ("Näkyvyys", {"fields": ("is_published",)}),
    )


@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Esittelytekstit",
            {"fields": ("heading", "short_text", "body")},
        ),
        ("Esittelykuva", {"fields": ("image", "image_alt")}),
    )

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
    fieldsets = (
        ("Palvelun tiedot", {"fields": ("title", "description", "price")}),
        ("Julkaisu ja järjestys", {"fields": ("is_published", "display_order")}),
    )


@admin.register(OtherPageContent)
class OtherPageContentAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Portfolio-sivu",
            {"fields": ("gallery_eyebrow", "gallery_heading", "gallery_empty_message")},
        ),
        ("Palvelusivu", {"fields": ("services_heading", "services_empty_message")}),
        (
            "Minusta-sivu",
            {
                "fields": (
                    "about_eyebrow",
                    "about_photos_eyebrow",
                    "about_photos_heading",
                )
            },
        ),
        ("Yhteystietosivu", {"fields": ("contact_heading", "contact_intro")}),
    )

    def has_add_permission(self, request):
        return not OtherPageContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactLink)
class ContactLinkAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "destination_type",
        "url",
        "phone_number",
        "is_published",
        "display_order",
    )
    list_editable = ("is_published", "display_order")
    list_filter = ("is_published",)
    search_fields = ("label", "url", "phone_number")
    ordering = ("display_order", "id")
    fieldsets = (
        (
            "Yhteydenottotavan tiedot",
            {
                "fields": (
                    "label",
                    "destination_type",
                    "url",
                    "phone_number",
                )
            },
        ),
        ("Julkaisu ja järjestys", {"fields": ("is_published", "display_order")}),
    )