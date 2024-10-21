from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    cover = models.ImageField(upload_to='cover/')
    pdf = models.FileField(upload_to='pdf/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_books')

    def delete(self, *args, **kwargs):
        self.cover.delete()
        self.pdf.delete()
        super(Book, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title

# Create your models here.
class user_details(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.first_name



class items(models.Model):
    item_name = models.CharField(max_length=100)
    item_pic = models.ImageField(upload_to='images/')
    price = models.IntegerField()

class review(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    item = models.ForeignKey(items, on_delete=models.CASCADE)
    review_desp = models.CharField(max_length=100)
    rating = models.IntegerField()

class BookRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        unique_together = ('user', 'book')

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    class Meta:
        app_label = 'upload'


class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']

    def __str__(self):
        return f"{self.user.username} favorited {self.book.title} at {self.added_at}"
    



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_uploaded_book = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()