from django.db import models
from django.contrib.auth.models import User

class hero_area(models.Model):
    hero_background_banner = models.ImageField(upload_to='hero_area')
    hero_title = models.CharField(max_length=100)
    para = models.CharField(max_length=200)

    def __str__(self):
        return self.hero_title
    
class forget_password_token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class TokenInfo(models.Model):
    token = models.CharField(max_length=1000)
    last_generation_date = models.DateField()
    def __str__(self):
        return f"Last Generation Date: {self.last_generation_date}"

class Markup(models.Model):
    markup_percentage = models.FloatField()

    def __str__(self):
        return str(self.markup_percentage)
    