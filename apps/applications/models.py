from django.db import models
from django.contrib.auth import get_user_model

class App(models.Model):
    TYPE_CHOICES = (
        (1, 'Web'),
        (2, 'Mobile'),
    )
    FRAMEWORK_CHOICES = (
        (1, 'Django'),
        (2, 'React Native'),
    )

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')
    type = models.IntegerField(choices=TYPE_CHOICES)
    framework = models.IntegerField(choices=FRAMEWORK_CHOICES)
    domain_name = models.CharField(max_length=50, blank=True, default='')
    screenshot = models.URLField(blank=True, default='')
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    active = models.BooleanField(default=True)
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    app = models.ForeignKey('App', on_delete=models.CASCADE)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name