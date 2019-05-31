from sorl.thumbnail import ImageField, get_thumbnail
from ...core.constants.sizes import DEFAULT_IMAGE_SIZE


class ImageThumbnailMixin(object):
    image_file_field_name = 'file'

    def get_thumbnail_image(self, size):
        measure = getattr(DEFAULT_IMAGE_SIZE, size)
        size_string = "x".join([str(measure[0]), str(measure[1])])
        return get_thumbnail(
            getattr(self, self.image_file_field_name), size_string,
            crop='center')

    @property
    def small_image(self):
        im = self.get_thumbnail_image('small')
        return im

    @property
    def small(self):
        return self.small_image.url

    @property
    def tiny_image(self):
        im = self.get_thumbnail_image("tiny")
        return im

    @property
    def tiny(self):
        return self.tiny_image.url

    @property
    def normal_image(self):
        im = self.get_thumbnail_image("normal")
        return im

    @property
    def normal(self):
        return self.normal_image.url

    @property
    def big_image(self):
        im = self.get_thumbnail_image("big")
        return im

    @property
    def big(self):
        return self.big_image.url
