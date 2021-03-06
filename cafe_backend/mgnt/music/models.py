import os
import boto3
import datetime
from urllib import request
from django.conf import settings
from django.db import models
from django.core.validators import ValidationError
from django.utils.translation import ugettext_lazy as _
from django_fsm import FSMField, transition
from django.contrib.postgres.fields import JSONField
from model_utils.models import TimeStampedModel
from cafe_backend.libs.ting.api import TingMusicAPI as Ting
from cafe_backend.libs.spotify.api import Spotify
from cafe_backend.core.constants.states import (
    MUSIC_STATE, MUSIC_PLAYLIST_STATE)
from cafe_backend.core.constants.types import MUSIC_PROVIDER


MUSIC_STATE_CHOICES = (
    (MUSIC_STATE.default, _('Not available')),
    (MUSIC_STATE.downloading, _('Downloading')),
    (MUSIC_STATE.uploading, _('Uploading')),
    (MUSIC_STATE.ready, _('Ready')),
)


MUSIC_PROVIDER_CHOICES = (
    (MUSIC_PROVIDER.ting, _('Ting')),
    (MUSIC_PROVIDER.kugou, _('KuGou')),
    (MUSIC_PROVIDER.spotify, _('Spotify'))
)


class Music(TimeStampedModel):
    title = models.CharField(max_length=64, verbose_name=_('Title'))
    author = models.CharField(max_length=32, verbose_name=_('Author'))
    url = models.URLField(verbose_name=_('Music url'))
    external_id = models.CharField(
        max_length=32, unique=True, verbose_name=_('External ID'))
    pic_url = models.URLField(verbose_name=_('Picture URL'))
    provider = FSMField(
        choices=MUSIC_PROVIDER_CHOICES, default=MUSIC_PROVIDER.ting,
        verbose_name=_('Music Provider'))
    state = FSMField(
        choices=MUSIC_STATE_CHOICES, default=MUSIC_STATE.default,
        verbose_name=_('State'))
    details = JSONField(default={}, verbose_name=_('Details'))

    class Meta:
        ordering = ('title', )
        verbose_name = _('Music')
        verbose_name_plural = _('Musics')

    def __str__(self):
        return "<%s(%d):%s>" % (_('Music'), self.pk, self.title)

    @classmethod
    def external_search(cls, keyword):
        # response = Ting.search_music(keyword)
        response = Spotify.search(keyword)
        return response

    @classmethod
    def find_music(cls, external_id, provider=MUSIC_PROVIDER.spotify):
        exist, instance = cls.exists(external_id, provider=provider)
        if exist:
            return True, instance
        else:
            instance = cls(
                external_id=external_id, provider=provider)
            is_valid = instance.clean()
            if is_valid:
                instance.save()
            return is_valid, instance

    def clean(self):
        super(Music, self).clean()
        external_id = self.external_id

        if self.provider == MUSIC_PROVIDER.ting:
            response_data = Ting.retrieve_music(external_id)

            if not response_data.get('songinfo'):
                return False
            else:
                self.title = response_data['songinfo']['title']
                self.author = response_data['songinfo']['author']
                self.url = response_data['bitrate']['show_link']
                self.pic_url = response_data['songinfo']['pic_big']
                return True
        else:
            response_data = Spotify.retrieve_music(external_id)
            self.title = response_data['name']
            self.author = response_data['author']
            self.url = response_data['url']
            self.pic_url = response_data['pic_url']
            self.state = MUSIC_STATE.ready
            return True

    @classmethod
    def exists(cls, external_id, provider=MUSIC_PROVIDER.spotify):
        qs = cls.objects.filter(external_id=external_id, provider=provider)
        if qs.exists():
            return True, qs.first()
        else:
            return False, None

    @property
    def music_file_extension(self):
        return self.url.split('?')[0].split('/')[-1].split('.')[-1]

    @property
    def picture_file_extension(self):
        return self.pic_url.split('?')[0].split('/')[-1].split('.')[-1]

    @property
    def download_file_path(self):
        return "%s/%s.%s" % (
            settings.MUSIC_DOWNLOAD_PATH, self.external_id,
            self.music_file_extension)

    @property
    def picture_download_file_path(self):
        return "%s/%s.%s" % (
            settings.MUSIC_DOWNLOAD_PATH, self.external_id,
            self.picture_file_extension)

    @property
    def upload_key(self):
        return "media/music/%s/%s.%s" % (
            self.external_id, self.external_id, self.music_file_extension)

    @property
    def picture_upload_key(self):
        return "media/music/%s/%s.%s" % (
            self.external_id, self.external_id, self.picture_file_extension)

    @property
    def music_url(self):
        return "http://%s/%s" % (
            settings.AWS_S3_CUSTOM_DOMAIN, self.upload_key)

    @property
    def picture_url(self):
        return "http://%s/%s" % (
            settings.AWS_S3_CUSTOM_DOMAIN, self.picture_upload_key)

    @classmethod
    def get_invalid_musics(cls):
        return cls.objects.filter(
            modified__date__lte=datetime.datetime.now().date())

    @transition(
        field='state',
        source=MUSIC_STATE.default, target=MUSIC_STATE.downloading)
    def download(self):
        request.urlretrieve(self.url, self.download_file_path)
        request.urlretrieve(self.pic_url, self.picture_download_file_path)

    @transition(
        field='state',
        source=MUSIC_STATE.downloading, target=MUSIC_STATE.uploading)
    def upload(self):
        s3 = boto3.client(
            's3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        s3.upload_file(
            self.download_file_path, bucket_name,
            self.upload_key)
        s3.upload_file(
            self.picture_download_file_path, bucket_name,
            self.picture_upload_key)

    @transition(
        field='state',
        source=MUSIC_STATE.uploading, target=MUSIC_STATE.ready)
    def approve(self):
        if os.path.exists(self.download_file_path):
            os.remove(self.download_file_path)
        if os.path.exists(self.picture_download_file_path):
            os.remove(self.picture_download_file_path)

    def process(self):
        self.download()
        self.upload()
        self.approve()
        self.save()

    @classmethod
    def spotify_musics(cls):
        return cls.objects.filter(provider=MUSIC_PROVIDER.spotify)


MUSIC_PLAYLIST_STATE_CHOICES = (
    (MUSIC_PLAYLIST_STATE.default, _('Requested')),
    (MUSIC_PLAYLIST_STATE.ready, _('Availiable')),
)


class Playlist(TimeStampedModel):
    table = models.ForeignKey(
        'users.Table', on_delete=models.SET_DEFAULT, null=True,
        related_name='playlist', default=None, verbose_name=_('Requester'))
    music = models.ForeignKey(
        Music, on_delete=models.CASCADE, related_name='playlist',
        verbose_name=_('Music'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active?'))
    state = FSMField(
        choices=MUSIC_PLAYLIST_STATE_CHOICES,
        default=MUSIC_PLAYLIST_STATE.default)

    def __str__(self):
        return "<%s(%d):%s>" % (_('Playlist'), self.pk, self.music.title)

    class Meta:
        ordering = ('created', )
        verbose_name = _('Playlist')
        verbose_name_plural = _('Playlist')

    def get_customer_name(self):
        if self.table is None:
            return None
        return self.table.name

    @property
    def title(self):
        return self.get_title()

    def get_title(self):
        return self.music.title

    @property
    def url(self):
        return self.get_url()

    def get_url(self):
        return self.music.music_url

    @property
    def pic_url(self):
        return self.get_pic_url()

    def get_pic_url(self):
        return self.music.picture_url

    @property
    def artist(self):
        return self.music.author

    @property
    def identifier(self):
        return self.music.external_id

    @classmethod
    def pendings(cls):
        return cls.objects.filter(
            state=MUSIC_PLAYLIST_STATE.default, is_active=True,
            music__provider=MUSIC_PROVIDER.spotify,
            music__state=MUSIC_STATE.ready)
