# Generated by Django 2.1.8 on 2019-10-07 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Seller', '0002_valid_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=32)),
                ('goods_num', models.IntegerField()),
                ('goods_price', models.FloatField()),
                ('goods_photo', models.CharField(max_length=32)),
                ('goods_total', models.FloatField()),
                ('goods_id', models.IntegerField()),
                ('cart_user', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_id', models.IntegerField()),
                ('goods_photo', models.CharField(max_length=32)),
                ('goods_name', models.CharField(max_length=32)),
                ('goods_count', models.IntegerField()),
                ('goods_price', models.FloatField()),
                ('goods_total', models.FloatField()),
                ('goods_status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PayOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.CharField(max_length=32)),
                ('order_date', models.DateTimeField(auto_now=True)),
                ('order_status', models.IntegerField()),
                ('order_total', models.FloatField(blank=True, null=True)),
                ('order_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.User')),
            ],
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.PayOrder'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='store_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.User'),
        ),
    ]
