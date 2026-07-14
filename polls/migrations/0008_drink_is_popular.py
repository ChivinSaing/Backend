# Generated manually for Drink.is_popular

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0007_drink_price_l_drink_price_m_drink_price_s"),
    ]

    operations = [
        migrations.AddField(
            model_name="drink",
            name="is_popular",
            field=models.BooleanField(
                default=False,
                help_text="If checked, this drink appears in the homepage carousel.",
            ),
        ),
    ]
