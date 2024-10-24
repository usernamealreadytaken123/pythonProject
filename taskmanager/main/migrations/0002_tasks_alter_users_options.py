# Generated by Django 5.1.2 on 2024-10-24 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('time', models.CharField(max_length=255, verbose_name='time')),
                ('stand', models.CharField(max_length=255, verbose_name='stand')),
                ('work_type', models.CharField(max_length=255, verbose_name='work_type')),
            ],
            options={
                'verbose_name': 'task',
                'verbose_name_plural': 'tasks',
                'db_table': 'my_table_1',
            },
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]