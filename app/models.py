from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save


# class User(AbstractUser):
#     friends = models.ManyToManyField('self')



#Tạo 1 bảng profile với các thuộc tính như bên dưới
#Lúc này class UserProfile sẽ kế thừa lại từ class django.db.models.Model
#Bản thân mỗi thuộc tính đều là 1 class
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(upload_to='static/images', blank=True, default='1.png')


    def __str__(self):
        return self.user.username



#class UserProfileManager(models.Model)

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
