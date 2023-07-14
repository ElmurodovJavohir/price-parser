# Generated by Django 4.0 on 2023-04-13 07:08

from django.db import migrations, models
import django.utils.timezone
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competitor', '0011_remove_productpricehistory_created_at_and_more'),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name='competitorproduct',
            name='track_price_product_update',
        ),
        pgtrigger.migrations.RemoveTrigger(
            model_name='competitorproduct',
            name='track_price_product_insert',
        ),
        migrations.AddField(
            model_name='productpricehistory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='competitorproduct',
            trigger=pgtrigger.compiler.Trigger(name='track_price_product_update', sql=pgtrigger.compiler.UpsertTriggerSql(func='\n                    INSERT INTO competitor_productpricehistory(product_id, price,created_at)\n                    SELECT\n                        new_values.id AS product_id,\n                        new_values.price AS price,\n                        NOW()\n                    FROM new_values;            \n                    RETURN NULL;', hash='9d9529c4ff5a0982b8a44b423bad4f8f579bfbba', level='STATEMENT', operation='UPDATE', pgid='pgtrigger_track_price_product_update_07210', referencing='REFERENCING NEW TABLE AS new_values ', table='competitor_competitorproduct', when='AFTER')),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='competitorproduct',
            trigger=pgtrigger.compiler.Trigger(name='track_price_product_insert', sql=pgtrigger.compiler.UpsertTriggerSql(func='\n                    INSERT INTO competitor_productpricehistory(product_id, price,created_at)\n                    SELECT\n                        new_values.id AS product_id,\n                        new_values.price AS price,\n                        NOW()\n                    FROM new_values;            \n                    RETURN NULL;', hash='deee1613d401874a2fe6f560859f4eea559bd0b5', level='STATEMENT', operation='INSERT', pgid='pgtrigger_track_price_product_insert_e69e5', referencing='REFERENCING NEW TABLE AS new_values ', table='competitor_competitorproduct', when='AFTER')),
        ),
    ]