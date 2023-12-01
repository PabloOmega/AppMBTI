# Generated by Django 4.2.7 on 2023-11-23 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_mbti', '0003_alter_user_date_alter_user_evsi_alter_user_jvsp_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1024)),
                ('order', models.PositiveIntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='answer_1',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='answer_2',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='answer_3',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='answer_4',
            field=models.TextField(null=True),
        ),
    ]