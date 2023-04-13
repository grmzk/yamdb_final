import datetime as dt

from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from rest_framework import serializers

from reviews import models

username_regex_validator = RegexValidator(
    regex=r'^[\w@+\-.]+$',
    message='<username> может состоять только из '
            'букв, цифр и символов: .@+-_'
)
min_score_validator = MinValueValidator(
    limit_value=1,
    message='Введенная оценка ниже допустимой'
)
max_score_validator = MaxValueValidator(
    limit_value=10,
    message='Введенная оценка выше допустимой'
)
min_year_validator = MinValueValidator(
    limit_value=1,
    message='Год должен быть не меньше 1'
)
max_year_validator = MaxValueValidator(
    limit_value=dt.date.today().year,
    message='Нельзя добавлять произведения из будущего'
)


def username_me_validator(username):
    if username == 'me':
        raise serializers.ValidationError('Запрещено использовать <me> '
                                          'в качестве username!')


def username_uniq_validator(username):
    if models.User.objects.filter(username=username).exists():
        raise serializers.ValidationError('Пользователь с '
                                          f'<username={username}> '
                                          'уже зарегистрирован!')


def email_uniq_validator(email):
    if models.User.objects.filter(email=email).exists():
        raise serializers.ValidationError('Пользователь с '
                                          f'<email={email}> '
                                          'уже зарегистрирован!')
