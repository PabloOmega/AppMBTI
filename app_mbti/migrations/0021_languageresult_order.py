# Generated by Django 4.2.7 on 2023-12-01 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_mbti', '0020_alter_question_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='languageresult',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
