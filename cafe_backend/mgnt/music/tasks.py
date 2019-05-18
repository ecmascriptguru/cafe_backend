from celery import shared_task
from .models import Music


@shared_task
def grab_music_to_s3(music_ids):
    total = len(music_ids)
    count = 0
    for pk in music_ids:
        music = Music.objects.get(pk=pk)
        try:
            music.process()
            count += 1
        except Exception as e:
            pass
    return total, count


@shared_task(bind=True)
def check_invalid_musics(self):
    musics = [item['pk'] for item in Music.get_invalid_musics().values('pk')]
    return grab_music_to_s3(musics)
