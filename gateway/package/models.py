from django.db import models

class Package(models.Model):
    title = models.CharField(max_length=50)
    price = models.PositiveBigIntegerField()
    description = models.TextField(blank=True)
    days = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title