# Generated by Django 4.0 on 2023-03-30 05:05

from django.db import migrations, models
import django.db.models.deletion
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('competitor', '0002_alter_competitor_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitorProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('url', models.CharField(max_length=512)),
                ('name', models.CharField(blank=True, max_length=512, null=True)),
                ('image', models.CharField(blank=True, max_length=512, null=True)),
                ('price', models.IntegerField(blank=True, default=0, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('competitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='competitor.competitor', verbose_name='Конкурент')),
            ],
            options={
                'unique_together': {('competitor', 'url')},
            },
        ),
        migrations.AlterModelOptions(
            name='competitorurls',
            options={'verbose_name': 'URL конкурентов', 'verbose_name_plural': 'URL конкурентов'},
        ),
        migrations.AlterField(
            model_name='competitorsetting',
            name='competitor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='competitor.competitor', verbose_name='Конкурент'),
        ),
        migrations.AlterField(
            model_name='competitorsetting',
            name='sitemaps_urls',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=256, null=True), blank=True, null=True, size=None, verbose_name='URL-адреса Sitemap'),
        ),
        migrations.AlterField(
            model_name='competitorurls',
            name='competitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urls', to='competitor.competitor', verbose_name='URL-адреса Sitemap'),
        ),
        migrations.AlterField(
            model_name='competitorurls',
            name='type',
            field=models.CharField(choices=[('category', 'Category url'), ('product', 'Product url')], max_length=25, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='competitorurls',
            name='url',
            field=models.CharField(max_length=512, unique=True, verbose_name='URL-адрес'),
        ),
        migrations.CreateModel(
            name='ProductPriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('price', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='competitor.competitorproduct')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
