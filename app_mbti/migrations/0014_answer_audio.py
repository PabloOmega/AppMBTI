# Generated by Django 4.2.7 on 2023-11-27 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_mbti', '0013_remove_user_evsi_remove_user_jvsp_remove_user_result_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='audio',
            field=models.FileField(null=True, upload_to='app_mbti/audios'),
        ),
    ]
