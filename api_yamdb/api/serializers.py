from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from reviews.models import Category, Comment, Genre, Review, Title, User

from .validators import (email_uniq_validator, max_score_validator,
                         max_year_validator, min_score_validator,
                         min_year_validator, username_me_validator,
                         username_regex_validator, username_uniq_validator)


class AuthSignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=150,
                                     validators=[
                                         username_regex_validator,
                                         username_me_validator,
                                     ])
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        fields = ['username', 'email']
        model = User

    def validate(self, attrs):
        username = attrs['username']
        email = attrs['email']
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.email != email:
                raise serializers.ValidationError(
                    f'Для пользователя <{username}> '
                    'не правильно указана почта!'
                )
        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f'Почта <{email}> уже зарегистрирована '
                'для другого пользователя!'
            )
        return attrs


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150,
                                     validators=[
                                         username_regex_validator,
                                         username_me_validator,
                                     ])
    confirmation_code = serializers.CharField(required=True, max_length=40)

    def validate(self, attrs):
        username = attrs['username']
        confirmation_code = attrs['confirmation_code']
        user = get_object_or_404(User, username=username)
        user_confirmation_code = user.confirmation_code
        user.confirmation_code = default_token_generator.make_token(user)
        user.save()
        if user_confirmation_code != confirmation_code:
            raise serializers.ValidationError('Неверный confirmation_code!')
        return attrs


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=150,
                                     validators=[
                                         username_regex_validator,
                                         username_me_validator,
                                         username_uniq_validator,
                                     ])
    email = serializers.EmailField(required=True, max_length=254,
                                   validators=[
                                       email_uniq_validator,
                                   ])

    class Meta:
        fields = ['username', 'email', 'first_name', 'last_name',
                  'bio', 'role']
        model = User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['id']


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    year = serializers.IntegerField(required=True,
                                    validators=[
                                        min_year_validator,
                                        max_year_validator,
                                    ])

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ['id', 'rating']


class TitleListSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField(required=True,
                                     validators=[
                                         min_score_validator,
                                         max_score_validator,
                                     ])

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        read_only_fields = ['id', 'author', 'pub_date']

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы не можете добавить более'
                                      'одного отзыва на произведение')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']
        read_only_fields = ['id', 'author', 'pub_date']
