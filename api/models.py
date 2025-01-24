from django.db import models


class Users(models.Model):
    """Модель для пользователя"""

    chat_id = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.chat_id


class WhitelistedUsers(models.Model):
    """Модель для белого списка пользователей"""

    chat_id = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Список"
        verbose_name_plural = "Списки"

    def __str__(self):
        return self.chat_id
