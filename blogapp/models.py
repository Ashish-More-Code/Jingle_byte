from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Recipepost(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='userid')
    title=models.CharField(max_length=200)
    content=models.TextField()
    createdate=models.DateTimeField()
    type=models.IntegerField()
    pimage=models.ImageField(upload_to='image/')
    likecount = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self): 
        return self.title

class Like(models.Model):
    Recipepost = models.ForeignKey(Recipepost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('Recipepost', 'user')

class comments(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='userid')
    bid=models.ForeignKey(Recipepost,on_delete=models.CASCADE,db_column='blogid')
    comment=models.TextField()

