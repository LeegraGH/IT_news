from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Appeal(models.Model):
    username = models.CharField(max_length=15)
    # phone=PhoneNumberField(unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    message = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        # return f"{self.phone if self.phone is not None else self.email}: {self.username}"
        return f"{self.email}: {self.username}"

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"
