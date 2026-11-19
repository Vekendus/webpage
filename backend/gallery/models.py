from django.db import models


class Photo(models.Model):
    title = models.CharField("otsikko", max_length=150)
    slot_code = models.CharField(
        "etusivun diaesityksen paikka",
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        help_text="Valitse 01–04, jos kuva näytetään etusivun diaesityksessä.",
    )
    image = models.ImageField("kuva", upload_to="portfolio/")
    description = models.TextField("kuvausteksti", blank=True)
    is_published = models.BooleanField(
        "julkaistu sivustolla",
        default=True,
        help_text="Poista valinta piilottaaksesi kuvan myös etusivun diaesityksestä.",
    )
    show_in_gallery = models.BooleanField("näytä portfoliossa", default=True)
    display_order = models.PositiveIntegerField("järjestys", default=0)

    class Meta:
        verbose_name = "portfolio-kuva"
        verbose_name_plural = "portfolio-kuvat"

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
