from django.db import models
from django.core.exceptions import ValidationError
import random


class Source(models.Model):
    SOURCE_TYPES = [
        ('movie', 'Фильм'),
        ('book', 'Книга'),
        ('other', 'Другое'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название")
    type = models.CharField(max_length=10, choices=SOURCE_TYPES, default='other', verbose_name="Тип")

    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"

    def quote_count(self):
        return self.quotes.count()

    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источники"


class Quote(models.Model):
    text = models.TextField(verbose_name="Текст цитаты", unique=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="quotes", verbose_name="Источник")
    weight = models.PositiveIntegerField(default=1, verbose_name="Вес")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    likes = models.PositiveIntegerField(default=0, verbose_name="Лайки")
    dislikes = models.PositiveIntegerField(default=0, verbose_name="Дизлайки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.text[:50]}..."

    def clean(self):
        # Проверка на максимальное количество цитат у источника
        if self.source.quote_count() >= 3 and not self.pk:
            raise ValidationError(f"У источника не может быть больше 3 цитат")

        # Проверка на дубликаты
        if Quote.objects.filter(text=self.text).exclude(pk=self.pk).exists():
            raise ValidationError("Цитата с таким текстом уже существует")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def get_random(cls):
        # Выбор случайной цитаты с учетом веса
        quotes = list(cls.objects.all())
        if not quotes:
            return None

        weights = [quote.weight for quote in quotes]
        return random.choices(quotes, weights=weights, k=1)[0]

    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"