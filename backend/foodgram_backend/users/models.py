from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'Аутентифицированный пользователь'),
        (ADMIN, 'Администратор'),
    ]

    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
        validators=[],
    )
    email = models.EmailField(
        'Почта',
        unique=True,
        max_length=254
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=250,
        blank=True,
        default=USER,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_together',
            )
        ]

    @property
    def is_admin(self):
        return (self.role == self.ADMIN or self.is_staff)

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписки на авторов рецептов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique_subscription',
            )
        ]
