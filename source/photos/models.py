from django.db import models
from rest_framework.exceptions import ValidationError

STATUS_CHOICES = (
    ('publish', 'Publish'),
    ('unpublish', 'Unpublish')
)


class Photo(models.Model):
    photo = models.ImageField(upload_to='uploads')
    caption = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    author = models.ForeignKey('auth.User', related_name='photo', on_delete=models.CASCADE,
                               null=True, blank=True, verbose_name='Author')
    tags = models.ManyToManyField('photos.Tag', blank=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        limit = 2 * 1024 * 1024
        if self.photo.size > limit:
            raise ValidationError('File too large. Note: Size should not exeed 2Mb.')
        super(Photo, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created_at',)


class Tag(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.name
