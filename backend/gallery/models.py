from django.core.exceptions import ValidationError
from django.db import models


class GalleryChapter(models.Model):
    title = models.CharField("otsikko", max_length=150)
    description = models.TextField("kuvaus", blank=True)
    cover_image = models.ImageField(
        "kansikuva",
        upload_to="portfolio/covers/",
        blank=True,
    )
    is_published = models.BooleanField("julkaistu", default=True)
    display_order = models.PositiveIntegerField("järjestys", default=0)

    class Meta:
        verbose_name = "portfolio-luku"
        verbose_name_plural = "portfolio-luvut"
        ordering = ("display_order", "id")

    def __str__(self):
        return self.title


class PortfolioPhoto(models.Model):
    chapter = models.ForeignKey(
        GalleryChapter,
        on_delete=models.PROTECT,
        related_name="photos",
        verbose_name="portfolio-luku",
    )
    title = models.CharField("otsikko", max_length=150)
    image = models.ImageField("kuva", upload_to="portfolio/")
    description = models.TextField("kuvausteksti", blank=True)
    is_published = models.BooleanField("julkaistu", default=True)
    display_order = models.PositiveIntegerField("järjestys", default=0)

    class Meta:
        verbose_name = "portfolio-kuva"
        verbose_name_plural = "portfolio-kuvat"
        ordering = ("display_order", "title")

    def __str__(self):
        return self.title


class SlideshowPhoto(models.Model):
    SLOT_CODE_CHOICES = (
        ("01", "01"),
        ("02", "02"),
        ("03", "03"),
        ("04", "04"),
    )

    title = models.CharField("otsikko", max_length=150)
    slot_code = models.CharField(
        "diaesityksen paikka",
        max_length=2,
        choices=SLOT_CODE_CHOICES,
        unique=True,
        help_text="Valitse diaesityksen paikka 01–04.",
    )
    image = models.ImageField("kuva", upload_to="slideshow/")
    is_published = models.BooleanField("julkaistu", default=True)

    class Meta:
        verbose_name = "diaesityksen kuva"
        verbose_name_plural = "diaesityksen kuvat"
        ordering = ("slot_code",)

    def __str__(self):
        return self.title


class AboutContent(models.Model):
    heading = models.CharField("otsikko", max_length=160)
    short_text = models.TextField(
        "lyhyt teksti etusivulle",
        help_text="Tämä teksti näytetään etusivun esittelyssä.",
    )
    body = models.TextField(
        "esittelyteksti",
        help_text="Erota kappaleet toisistaan tyhjällä rivillä.",
    )
    image = models.ImageField("esittelykuva", upload_to="about/", blank=True)
    image_alt = models.CharField("kuvan vaihtoehtoinen teksti", max_length=200, blank=True)

    class Meta:
        verbose_name = "esittelyteksti"
        verbose_name_plural = "esittelyteksti"

    def __str__(self):
        return "About page content"


class AboutPhoto(models.Model):
    image_url = models.URLField("kuvan URL", max_length=500)
    alt_text = models.CharField("kuvan vaihtoehtoinen teksti", max_length=250)
    caption = models.CharField("kuvateksti", max_length=160, blank=True)
    is_published = models.BooleanField("julkaistu", default=True)
    display_order = models.PositiveIntegerField("järjestys", default=0)

    class Meta:
        verbose_name = "minusta-sivun kuva"
        verbose_name_plural = "minusta-sivun kuvat"
        ordering = ("display_order", "id")

    def __str__(self):
        return self.caption or self.alt_text


class Service(models.Model):
    title = models.CharField("palvelun nimi", max_length=150)
    description = models.CharField("kuvaus", max_length=200, blank=True)
    price = models.CharField(
        "hinta",
        max_length=100,
        help_text="Esimerkiksi 89 € tai Hinta sovitaan asiakkaan kanssa.",
    )
    is_published = models.BooleanField("julkaistu", default=True)
    display_order = models.PositiveIntegerField("järjestys", default=0)

    class Meta:
        verbose_name = "kuvauspalvelu"
        verbose_name_plural = "kuvauspalvelut"
        ordering = ("display_order", "title")

    def __str__(self):
        return self.title


class OtherPageContent(models.Model):
    gallery_eyebrow = models.CharField(
        "portfoliosivun yläteksti",
        max_length=80,
        default="GALLERIA",
    )
    gallery_heading = models.CharField(
        "portfoliosivun otsikko",
        max_length=200,
        default="Valokuvia, joissa on tunnetta.",
    )
    gallery_empty_message = models.CharField(
        "portfoliosivun tyhjän gallerian teksti",
        max_length=200,
        default="Portfolio-kuvia ei ole vielä julkaistu.",
    )
    services_heading = models.CharField(
        "palvelusivun otsikko",
        max_length=160,
        default="Palvelut",
    )
    services_empty_message = models.CharField(
        "palvelusivun tyhjän listan teksti",
        max_length=200,
        default="Palveluiden tietoja ei ole vielä lisätty.",
    )
    about_eyebrow = models.CharField(
        "minusta-sivun yläteksti",
        max_length=100,
        default="HILTUNEN PHOTOGRAPHY",
    )
    about_photos_eyebrow = models.CharField(
        "minusta-sivun kuvien yläteksti",
        max_length=100,
        default="HILTUNEN PHOTOGRAPHY",
    )
    about_photos_heading = models.CharField(
        "minusta-sivun kuvien otsikko",
        max_length=160,
        default="Kuvia minusta",
    )
    contact_heading = models.CharField(
        "yhteystietosivun otsikko",
        max_length=160,
        default="Yhteystiedot",
    )
    contact_intro = models.TextField(
        "yhteystietosivun esittelyteksti",
        blank=True,
        default="",
    )

    class Meta:
        verbose_name = "muiden sivujen tekstisisältö"
        verbose_name_plural = "muiden sivujen tekstisisältö"

    def __str__(self):
        return "Other page text and headings"


class ContactLink(models.Model):
    class DestinationType(models.TextChoices):
        URL = "url", "Verkko- tai someosoite"
        WHATSAPP = "whatsapp", "WhatsApp-puhelinnumero"

    label = models.CharField("linkin teksti", max_length=100)
    destination_type = models.CharField(
        "kohteen tyyppi",
        max_length=20,
        choices=DestinationType.choices,
        default=DestinationType.URL,
    )
    url = models.URLField(
        "verkko- tai someosoite",
        max_length=500,
        blank=True,
        default="",
        help_text="Käytä tätä kenttää verkko- ja someosoitteille.",
    )
    phone_number = models.CharField(
        "WhatsApp-puhelinnumero",
        max_length=30,
        blank=True,
        default="",
        help_text=(
            "Lisää maatunnuksella, esimerkiksi +358 40 123 4567. "
            "WhatsApp-linkki muodostetaan numerosta automaattisesti."
        ),
    )
    is_published = models.BooleanField("julkaistu", default=True)
    display_order = models.PositiveIntegerField("järjestys", default=0)

    class Meta:
        verbose_name = "yhteystietolinkki"
        verbose_name_plural = "yhteystietolinkit"
        ordering = ("display_order", "id")

    def __str__(self):
        return self.label

    @property
    def public_url(self):
        if self.destination_type == self.DestinationType.WHATSAPP:
            digits = "".join(
                character
                for character in self.phone_number
                if character in "0123456789"
            )
            return f"https://wa.me/{digits}" if digits else ""
        return self.url

    def clean(self):
        super().clean()
        if self.destination_type == self.DestinationType.WHATSAPP:
            digits = "".join(
                character
                for character in self.phone_number
                if character in "0123456789"
            )
            if self.is_published and not digits:
                raise ValidationError(
                    {
                        "phone_number": (
                            "Anna julkaistulle WhatsApp-linkille puhelinnumero."
                        )
                    }
                )
            if digits and not 8 <= len(digits) <= 15:
                raise ValidationError(
                    {
                        "phone_number": (
                            "Anna WhatsApp-numero maatunnuksella "
                            "(8–15 numeroa)."
                        )
                    }
                )
