from django.db.models import Prefetch
from django.http import JsonResponse

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


def slideshow_photo_list(request):
    photos = SlideshowPhoto.objects.filter(is_published=True)
    data = [
        {
            "id": photo.id,
            "title": photo.title,
            "slot_code": photo.slot_code,
            "image": photo.image.url,
        }
        for photo in photos
    ]
    return JsonResponse(data, safe=False)


def portfolio_gallery(request):
    published_photos = PortfolioPhoto.objects.filter(is_published=True).order_by(
        "display_order", "title"
    )
    chapters = GalleryChapter.objects.filter(is_published=True).prefetch_related(
        Prefetch("photos", queryset=published_photos)
    )
    data = []
    for chapter in chapters:
        photos = [
            {
                "id": photo.id,
                "title": photo.title,
                "description": photo.description,
                "image": photo.image.url,
            }
            for photo in chapter.photos.all()
        ]
        if photos:
            data.append(
                {
                    "id": chapter.id,
                    "title": chapter.title,
                    "description": chapter.description,
                    "photos": photos,
                }
            )
    return JsonResponse(data, safe=False)


def about_content(request):
    content = AboutContent.objects.first()
    if content is None:
        return JsonResponse(
            {"detail": "About page content has not been configured."},
            status=404,
        )

    data = {
        "heading": content.heading,
        "short_text": content.short_text,
        "body": content.body,
        "image": content.image.url if content.image else None,
        "image_alt": content.image_alt,
        "photos": [
            {
                "id": photo.id,
                "image": photo.image_url,
                "alt": photo.alt_text,
                "caption": photo.caption,
            }
            for photo in AboutPhoto.objects.filter(is_published=True)
        ],
    }
    return JsonResponse(data)


def service_list(request):
    services = Service.objects.filter(is_published=True)
    data = [
        {
            "id": service.id,
            "title": service.title,
            "description": service.description,
            "price": service.price,
        }
        for service in services
    ]
    return JsonResponse(data, safe=False)


def other_page_content(request):
    content = OtherPageContent.objects.first()
    if content is None:
        return JsonResponse(
            {"detail": "Other page content has not been configured."},
            status=404,
        )

    data = {
        "gallery": {
            "eyebrow": content.gallery_eyebrow,
            "heading": content.gallery_heading,
            "empty_message": content.gallery_empty_message,
        },
        "services": {
            "heading": content.services_heading,
            "empty_message": content.services_empty_message,
        },
        "about": {
            "eyebrow": content.about_eyebrow,
            "photos_eyebrow": content.about_photos_eyebrow,
            "photos_heading": content.about_photos_heading,
        },
        "contact": {
            "heading": content.contact_heading,
            "intro": content.contact_intro,
            "links": [
                {
                    "id": link.id,
                    "label": link.label,
                    "url": link.url,
                }
                for link in ContactLink.objects.filter(is_published=True)
            ],
        },
    }
    return JsonResponse(data)
