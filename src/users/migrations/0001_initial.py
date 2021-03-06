# Generated by Django 2.2.4 on 2019-09-13 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=200, unique=True)),
                ('source', models.CharField(max_length=200)),
                ('priority', models.IntegerField(default=0)),
                ('similar_keywords', models.CharField(blank=True, max_length=1000)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'db_table': 'keywords',
            },
        ),
    ]
