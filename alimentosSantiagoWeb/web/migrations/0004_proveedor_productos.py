# Generated by Django 4.0.4 on 2022-07-07 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_empresa_convenio_restaurant_direccion_repartidor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor_productos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_producto', models.IntegerField()),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='web.producto')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.proveedor')),
            ],
        ),
    ]