from django.db import models
from django.contrib.auth.models import User

class Quote(models.Model):
    text = models.TextField(unique=True)
    source = models.CharField(max_length=255)
    weight = models.PositiveIntegerField(default=1)
    views = models.PositiveIntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.text[:60]}..."

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['text'], name='unique_quote_text')
        ]

class Vote(models.Model):
    VOTE_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=7, choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'quote')
