from django.test import TestCase

from .models import AboutContent, AboutPhoto, Photo, Service


class PublicContentApiTests(TestCase):
    def test_photo_api_only_returns_published_photos(self):
        Photo.objects.create(title="Julkaistu", image="portfolio/live.jpg")
        Photo.objects.create(
            title="Vain diaesityksessä",
            image="portfolio/hero.jpg",
            slot_code="01",
            show_in_gallery=False,
        )
        Photo.objects.create(
            title="Piilotettu",
            image="portfolio/hidden.jpg",
            is_published=False,
        )

        response = self.client.get("/api/photos/")

        self.assertEqual(response.status_code, 200)
        photos = {photo["title"]: photo for photo in response.json()}
        self.assertEqual(
            set(photos),
            {"Julkaistu", "Vain diaesityksessä"},
        )
        self.assertFalse(photos["Vain diaesityksessä"]["show_in_gallery"])
        self.assertTrue(
            photos["Julkaistu"]["image"].endswith("/media/portfolio/live.jpg")
        )

    def test_about_api_returns_admin_managed_content(self):
        content = AboutContent.objects.get()
        content.heading = "Päivitetty otsikko"
        content.save()

        response = self.client.get("/api/about/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["heading"], "Päivitetty otsikko")
        self.assertIsNone(response.json()["image"])

    def test_about_api_lists_published_photos_in_order(self):
        AboutPhoto.objects.all().delete()
        AboutPhoto.objects.create(
            image_url="https://example.com/second.jpg",
            alt_text="Toinen kuva",
            display_order=2,
        )
        AboutPhoto.objects.create(
            image_url="https://example.com/first.jpg",
            alt_text="Ensimmäinen kuva",
            display_order=1,
        )
        AboutPhoto.objects.create(
            image_url="https://example.com/hidden.jpg",
            alt_text="Piilotettu kuva",
            is_published=False,
            display_order=0,
        )

        response = self.client.get("/api/about/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [photo["alt"] for photo in response.json()["photos"]],
            ["Ensimmäinen kuva", "Toinen kuva"],
        )
        self.assertEqual(
            response.json()["photos"][0]["image"],
            "https://example.com/first.jpg",
        )

    def test_service_api_returns_published_services_in_display_order(self):
        Service.objects.all().delete()
        Service.objects.create(title="Myöhempi", price="20 €", display_order=2)
        Service.objects.create(title="Ensimmäinen", price="10 €", display_order=1)
        Service.objects.create(
            title="Piilotettu",
            price="30 €",
            is_published=False,
            display_order=0,
        )

        response = self.client.get("/api/services/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [service["title"] for service in response.json()],
            ["Ensimmäinen", "Myöhempi"],
        )
        self.assertEqual(response.json()[0]["price"], "10 €")
