import requests
from django.conf import settings
from django.db import migrations


def fill_apartment_data(apps, schema_editor):
    r = requests.get(f"{settings.ASSETS_BASE}apartments.json")
    apartments = r.json()

    Apartment = apps.get_model("api", "Apartment")
    for apartment_data in apartments:
        track = Apartment.objects.create(
            id=apartment_data["id"],
            rooms=apartment_data["rooms"],
            floor=apartment_data["floor"],
            area=apartment_data["area"],
            rent=apartment_data["rent"],
            latitude=apartment_data["latitude"],
            longitude=apartment_data["longitude"],
            description=apartment_data["description"],
        )
        track.save()


class Migration(migrations.Migration):
    dependencies = [("api", "0001_initial")]

    operations = [
        migrations.RunPython(fill_apartment_data),
    ]
