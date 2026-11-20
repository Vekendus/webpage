from django.db import migrations, models


def create_contact_link_templates(apps, schema_editor):
    ContactLink = apps.get_model("gallery", "ContactLink")
    database = schema_editor.connection.alias
    labels = ("Website", "Facebook", "TikTok", "WhatsApp", "Pinterest")

    for order, label in enumerate(labels, start=2):
        ContactLink.objects.using(database).get_or_create(
            label=label,
            defaults={
                "url": "",
                "is_published": False,
                "display_order": order,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("gallery", "0009_chapter_cover_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactlink",
            name="url",
            field=models.URLField(
                blank=True,
                default="",
                help_text=(
                    "Lisää koko osoite, esimerkiksi "
                    "https://instagram.com/oma-tili."
                ),
                max_length=500,
                verbose_name="linkin osoite",
            ),
        ),
        migrations.RunPython(
            create_contact_link_templates,
            migrations.RunPython.noop,
        ),
    ]
