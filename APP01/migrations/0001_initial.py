# Generated by Django 2.2 on 2019-05-15 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('email', models.CharField(default='', max_length=20)),
                ('pwd', models.CharField(default='123', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Foods',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('mname', models.CharField(max_length=20)),
                ('intro', models.TextField()),
                ('time', models.DateTimeField()),
                ('yingting', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('num', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('intro', models.TextField()),
                ('price', models.IntegerField()),
                ('num', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Goods_type',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Huiyuan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('pwd', models.CharField(default='123', max_length=20)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('addr', models.CharField(default='三里屯', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('pwd', models.CharField(default='123', max_length=20)),
                ('email', models.CharField(default='1', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('price', models.IntegerField()),
                ('foods', models.ManyToManyField(to='APP01.Foods')),
                ('goods', models.ManyToManyField(to='APP01.Goods')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APP01.Huiyuan')),
            ],
        ),
        migrations.AddField(
            model_name='goods',
            name='type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APP01.Goods_type'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('foods', models.ManyToManyField(to='APP01.Foods')),
                ('goods', models.ManyToManyField(to='APP01.Goods')),
                ('owner', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='APP01.UserInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Book2',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, unique=True)),
                ('publisher_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APP01.Publisher')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, unique=True)),
                ('publisher_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APP01.Publisher')),
            ],
        ),
    ]
