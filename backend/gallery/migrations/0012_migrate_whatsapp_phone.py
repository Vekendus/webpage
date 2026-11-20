import re

from django.db import migrations


def migrate_whatsapp_phone(apps, schema_editor):
    ContactLink = apps.get_model("gallery", "ContactLink")
    database = schema_editor.connection.alias

    links = ContactLink.objects.using(database).filter(label__icontains="WhatsApp")
    for link in links:
        if link.destination_type != "url" or link.url:
            continue

        match = re.search(r"\+\s*\d[\d\s().-]*\d", link.label)
        if match:
            phone_number = match.group(0).strip()
            digits = "".join(
                character
                for character in phone_number
                if character.isdigit()
            )
            if not 8 <= len(digits) <= 15:
                continue
            link.label = "WhatsApp"
            link.phone_number = phone_number

        link.destination_type = "whatsapp"
        link.save(
            using=database,
            update_fields=("label", "destination_type", "phone_number"),
        )


class Migration(migrations.Migration):

    dependencies = [
        ("gallery", "0011_contact_whatsapp_phone"),
    ]

    operations = [
        migrations.RunPython(
            migrate_whatsapp_phone,
            migrations.RunPython.noop,
        ),
    ]
