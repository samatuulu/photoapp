from django.db import models


STATUS_CHOICES = (
    ('publish', 'Publish'),
    ('unpublish', 'Unpublish')
)


class Photo(models.Model):
    photo = models.ImageField(upload_to='uploads')
    caption = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('-created_at',)
