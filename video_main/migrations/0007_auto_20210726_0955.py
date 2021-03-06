# Generated by Django 3.2.5 on 2021-07-26 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_main', '0006_alter_movie_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ('created_at',)},
        ),
        migrations.AddField(
            model_name='episode',
            name='subtitle_file',
            field=models.FileField(blank=True, null=True, upload_to='episode_subtitles'),
        ),
        migrations.AddField(
            model_name='movie',
            name='subtitle_file',
            field=models.FileField(blank=True, null=True, upload_to='movie_subtitles'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='tags',
            field=models.ManyToManyField(default='Recommended Tag', related_name='movie_tags', to='video_main.Tag'),
        ),
    ]
