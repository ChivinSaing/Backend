# Replace manual is_popular with view_count for carousel ranking.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0008_drink_is_popular"),
    ]

    operations = [
        migrations.AddField(
            model_name="drink",
            name="view_count",
            field=models.PositiveIntegerField(
                default=0,
                help_text="Number of times customers opened this drink’s detail page; homepage carousel shows most-viewed drinks.",
            ),
        ),
        migrations.RemoveField(
            model_name="drink",
            name="is_popular",
        ),
    ]
