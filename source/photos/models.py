from django.db import models
from PIL import Image

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

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        super().save()
        image = Image.open(self.photo.path)

        if image.height > 1000 or image.width > 1000:
            output_size = (1000, 1000)
            image.thumbnail(output_size)
            image.save(self.photo.path)

    class Meta:
        ordering = ('-created_at',)
