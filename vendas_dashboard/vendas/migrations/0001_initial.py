# Generated by Django 4.2.16 on 2024-10-18 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('total_vendas', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
