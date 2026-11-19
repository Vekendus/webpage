from django.http import JsonResponse

from .models import AboutContent, AboutPhoto, Photo, Service


def photo_list(request):
    photos = Photo.objects.filter(is_published=True).order_by(
        "display_order", "title"
    )
    data = [
        {
            "id": photo.id,
            "title": photo.title,
            "slot_code": photo.slot_code,
            "description": photo.description,
            "image": request.build_absolute_uri(photo.image.url),
            "show_in_gallery": photo.show_in_gallery,
        }
        for photo in photos
    ]
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
        "image": (
            request.build_absolute_uri(content.image.url)
            if content.image
            else None
        ),
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
