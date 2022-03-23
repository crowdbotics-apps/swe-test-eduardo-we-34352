from django.db import models
from django.contrib.auth import get_user_model

class App(models.Model):
    TYPE_CHOICES = (
        ('Web', 'Web'),
        ('Mobile', 'Mobile'),
    )
    FRAMEWORK_CHOICES = (
        ('Django', 'Django'),
        ('React Native', 'React Native'),
    )

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')
    type = models.CharField(choices=TYPE_CHOICES, max_length=15)
    framework = models.CharField(choices=FRAMEWORK_CHOICES, max_length=15)
    domain_name = models.CharField(max_length=50, blank=True, default='')
    screenshot = models.URLField(blank=True, default='')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    active = models.BooleanField(default=True)
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    app = models.OneToOneField('App', on_delete=models.SET_NULL)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
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