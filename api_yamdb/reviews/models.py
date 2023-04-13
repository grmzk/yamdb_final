from django.contrib.auth.models import AbstractUser
from django.db import models

from api.validators import (max_score_validator, max_year_validator,
                            min_score_validator, min_year_validator,
                            username_me_validator, username_regex_validator)


class RoleChoices(models.TextChoices):
    USR = 'user'
    MDR = 'moderator'
    ADM = 'admin'


class User(AbstractUser):
    username = models.CharField(
        verbose_name='UserName',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=[
            username_regex_validator,
            username_me_validator,
        ],
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Права',
        max_length=9,
        choices=RoleChoices.choices,
        default=RoleChoices.USR,
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    confirmation_code = models.CharField(
        verbose_name='Код для получения токена',
        max_length=40,
        null=True,
        blank=True,
        default=None
    )

    class Meta:
        ordering = ['username']

    @property
    def is_admin(self):
        return self.role == RoleChoices.ADM

    @property
    def is_moderator(self):
        return self.role == RoleChoices.MDR

    @property
    def is_user(self):
        return self.role == RoleChoices.USR


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=256
    )
    slug = models.SlugField(
        "Краткое название категории",
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=256
    )
    slug = models.SlugField(
        'Краткое название жанра',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.slug


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=256,
        blank=False
    )
    description = models.TextField(
        'Описание',
        blank=True
    )
    year = models.IntegerField(
        blank=False,
        validators=[
            min_year_validator,
            max_year_validator,
        ],
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='titles',
        blank=False,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
        blank=False
    )

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return f'Общая информация о произведении {self.name}'


class Review(models.Model):
    """Класс отзывов."""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            min_score_validator,
            max_score_validator,
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(models.Model):
    """Класс комментариев."""
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']
