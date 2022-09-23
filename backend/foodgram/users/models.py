from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint

class User(AbstractUser):
    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True
    )
    firs_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    username = models.CharField(
        'Юзернейм',
        max_length=150,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_pular = 'Пользователи'
        ordering = ['-pk']
    
    def __str__(self):
        return self.username[:30]


class Subscription(models.model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        related_name='author',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_usre_author'
            )
        ]
    def __str__(self):
        return f'Пользователь {self.user} подписалься на {self.author}'