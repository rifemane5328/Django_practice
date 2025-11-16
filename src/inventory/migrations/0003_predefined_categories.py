import json
from pathlib import Path
from django.db import migrations

def load_categories(apps, schema_editor):
    Category = apps.get_model('inventory', 'Category')
    app_dir = Path(__file__).resolve().parents[1]
    json_path = app_dir / 'fixtures' / 'categories.json'

    with json_path.open(encoding='utf-8') as file:
        data = json.load(file)

    categories = []
    for i in data:
        categories.append(Category(code=i['code'], name=i['name']))

    Category.objects.bulk_create(categories)


def unload_categories(apps, schema_editor):
    Categories = apps.get_model('inventory', 'Category')
    Categories.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_category'),
    ]

    operations = [migrations.RunPython(load_categories, unload_categories)]
