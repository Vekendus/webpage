from django.contrib.auth import get_user_model
from django.test import Client, TestCase

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


class PublicContentApiTests(TestCase):
    def test_slideshow_api_only_returns_published_photos_in_slot_order(self):
        SlideshowPhoto.objects.create(
            title="Dia kaksi",
            image="portfolio/02.jpg",
            slot_code="02",
        )
        SlideshowPhoto.objects.create(
            title="Dia yksi",
            image="portfolio/01.jpg",
            slot_code="01",
        )
        SlideshowPhoto.objects.create(
            title="Piilotettu dia",
            image="portfolio/hidden.jpg",
            slot_code="03",
            is_published=False,
        )

        response = self.client.get("/api/slideshow/")

        self.assertEqual(response.status_code, 200)
        photos = response.json()
        self.assertEqual(
            [photo["title"] for photo in photos],
            ["Dia yksi", "Dia kaksi"],
        )
        self.assertEqual([photo["slot_code"] for photo in photos], ["01", "02"])
        self.assertEqual(
            photos[0]["image"],
            "/media/portfolio/01.jpg",
        )

    def test_portfolio_api_groups_published_photos_by_chapter(self):
        PortfolioPhoto.objects.all().delete()
        GalleryChapter.objects.all().delete()

        later_chapter = GalleryChapter.objects.create(
            title="Perhekuvat",
            display_order=2,
        )
        first_chapter = GalleryChapter.objects.create(
            title="Hääkuvat",
            display_order=1,
            cover_image="portfolio/covers/wedding-cover.jpg",
        )
        GalleryChapter.objects.create(
            title="Parikuvat",
            display_order=3,
        )
        hidden_chapter = GalleryChapter.objects.create(
            title="Piilotettu luku",
            is_published=False,
        )
        PortfolioPhoto.objects.create(
            chapter=later_chapter,
            title="Perhekuva",
            image="portfolio/family.jpg",
        )
        PortfolioPhoto.objects.create(
            chapter=first_chapter,
            title="Hääkuva",
            image="portfolio/wedding.jpg",
        )
        PortfolioPhoto.objects.create(
            chapter=first_chapter,
            title="Piilotettu kuva",
            image="portfolio/hidden.jpg",
            is_published=False,
        )
        PortfolioPhoto.objects.create(
            chapter=hidden_chapter,
            title="Piilotetun luvun kuva",
            image="portfolio/hidden-chapter.jpg",
        )

        response = self.client.get("/api/portfolio/")

        self.assertEqual(response.status_code, 200)
        chapters = response.json()
        self.assertEqual(
            [chapter["title"] for chapter in chapters],
            ["Hääkuvat", "Perhekuvat", "Parikuvat"],
        )
        self.assertEqual(
            [photo["title"] for photo in chapters[0]["photos"]],
            ["Hääkuva"],
        )
        self.assertEqual(
            chapters[0]["cover_image"],
            "/media/portfolio/covers/wedding-cover.jpg",
        )
        self.assertEqual(
            chapters[1]["cover_image"],
            "/media/portfolio/family.jpg",
        )
        self.assertIsNone(chapters[2]["cover_image"])
        self.assertEqual(chapters[2]["photos"], [])
        self.assertEqual(
            chapters[0]["photos"][0]["image"],
            "/media/portfolio/wedding.jpg",
        )

    def test_about_api_returns_admin_managed_content(self):
        content = AboutContent.objects.get()
        content.heading = "Päivitetty otsikko"
        content.image = "about/profile.jpg"
        content.save()

        response = self.client.get("/api/about/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["heading"], "Päivitetty otsikko")
        self.assertEqual(response.json()["image"], "/media/about/profile.jpg")

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

    def test_other_page_content_and_contact_links_are_admin_managed(self):
        content = OtherPageContent.objects.get()
        content.gallery_heading = "Uusi portfoliosivun otsikko"
        content.services_heading = "Uudet palvelut"
        content.about_photos_heading = "Uusi kuvagallerian otsikko"
        content.contact_heading = "Ota yhteyttä"
        content.contact_intro = "Olen täällä."
        content.save()

        self.assertEqual(
            ContactLink.objects.get(label="Instagram").url,
            "https://www.instagram.com/hiltunenphotography/",
        )
        self.assertEqual(
            list(
                ContactLink.objects.filter(
                    url="",
                    is_published=False,
                ).values_list("label", flat=True)
            ),
            ["Website", "Facebook", "TikTok", "WhatsApp", "Pinterest"],
        )
        ContactLink.objects.all().delete()
        ContactLink.objects.create(
            label="Myöhempi",
            url="https://example.com/later",
            display_order=2,
        )
        ContactLink.objects.create(
            label="Instagram",
            url="https://example.com/instagram",
            display_order=1,
        )
        ContactLink.objects.create(
            label="Piilotettu",
            url="https://example.com/hidden",
            is_published=False,
            display_order=0,
        )
        ContactLink.objects.create(
            label="Osoitteeton",
            url="",
            is_published=True,
            display_order=0,
        )

        response = self.client.get("/api/pages/")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(
            data["gallery"]["heading"],
            "Uusi portfoliosivun otsikko",
        )
        self.assertEqual(data["services"]["heading"], "Uudet palvelut")
        self.assertEqual(
            data["about"]["photos_heading"],
            "Uusi kuvagallerian otsikko",
        )
        self.assertEqual(data["contact"]["heading"], "Ota yhteyttä")
        self.assertEqual(data["contact"]["intro"], "Olen täällä.")
        self.assertEqual(
            [link["label"] for link in data["contact"]["links"]],
            ["Instagram", "Myöhempi"],
        )


class AdminDashboardTests(TestCase):
    def test_dashboard_shows_task_links_for_site_content(self):
        admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="test-password",
        )
        self.client.force_login(admin_user)

        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tervetuloa sisällönhallintaan")
        self.assertContains(response, "Etusivun kuvat")
        self.assertContains(response, "Portfolion kategoriat ja kansikuvat")
        self.assertContains(response, "Kaikki hallintanäkymät")

    def test_admin_login_accepts_the_site_proxy_origin(self):
        client = Client(enforce_csrf_checks=True)
        login_page = client.get("/admin/login/")
        csrf_token = login_page.cookies["csrftoken"].value

        response = client.post(
            "/admin/login/",
            {
                "username": "not-a-user",
                "password": "not-a-password",
                "csrfmiddlewaretoken": csrf_token,
            },
            HTTP_ORIGIN="http://127.0.0.1:5173",
        )

        self.assertEqual(response.status_code, 200)
