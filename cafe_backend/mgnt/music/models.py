from django.db import models
from django.core.validators import ValidationError
from model_utils.models import TimeStampedModel
from cafe_backend.libs.ting.api import TingMusicAPI as Ting


class Music(TimeStampedModel):
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=32)
    url = models.URLField(verbose_name='Music URL')
    external_id = models.CharField(max_length=32, unique=True)
    pic_url = models.URLField(verbose_name='Picture URL')

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return "<Music(%d):%s>" % (self.pk, self.title)

    @classmethod
    def external_search(cls, keyword):
        response = Ting.search_music(keyword)
        return response

    @classmethod
    def find_music(cls, external_id):
        exist, instance = cls.exists(external_id)
        if exist:
            return True, instance
        else:
            instance = cls(
                external_id=external_id)
            is_valid = instance.clean()
            if is_valid:
                instance.save()
            return is_valid, instance

    def clean(self):
        super(Music, self).clean()
        external_id = self.external_id
        response_data = Ting.retrieve_music(external_id)

        if not response_data.get('songinfo'):
            return False
        else:
            self.title = response_data['songinfo']['title']
            self.author = response_data['songinfo']['author']
            self.url = response_data['bitrate']['show_link']
            self.pic_url = response_data['songinfo']['pic_small']
            return True

    @classmethod
    def exists(cls, external_id):
        qs = cls.objects.filter(external_id=external_id)
        if qs.exists():
            return True, qs.first()
        else:
            return False, None


class Playlist(TimeStampedModel):
    table = models.ForeignKey(
        'users.Table', on_delete=models.SET_DEFAULT, null=True,
        related_name='playlist', default=None)
    music = models.ForeignKey(
        Music, on_delete=models.CASCADE, related_name='playlist')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "<Playlist(%d):%s>" % (self.pk, self.music.title)

    class Meta:
        ordering = ('created', )

    def get_customer_name(self):
        return self.table.name

    def get_title(self):
        return self.music.title

    def get_url(self):
        return self.music.url

    def get_pic_url(self):
        return self.music.pic_url
