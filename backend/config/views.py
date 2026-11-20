from django.conf import settings
from django.http import FileResponse, Http404


def frontend_app(_request):
    index_path = settings.BASE_DIR.parent / "dist" / "index.html"
    if not index_path.is_file():
        raise Http404("The frontend build is missing.")
    return FileResponse(index_path.open("rb"), content_type="text/html")
