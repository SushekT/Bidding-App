from django.db import models
from account.models import Account
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from datetime import datetime, timezone

product_status = (('Pending', 'Pending'), ('Accept', 'Accept'), ('Reject', 'Reject'))


from ckeditor.fields import RichTextField

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField()
    image = models.ImageField(upload_to = 'category/')
    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=100)
    minimumprice = models.FloatField()
    postdate = models.DateTimeField(auto_now=True, null=True)
    lastbiddate = models.DateTimeField()
    cover_image = models.ImageField(upload_to = 'coverimage/')
    dayused = models.PositiveIntegerField(null=True)
    description = RichTextField()
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def post_duration(self):
        diff = datetime.now(timezone.utc)-self.postdate
        total_seconds = diff.total_seconds()
        if total_seconds<60:
            return "few seconds ago"
        elif total_seconds<3600:
            min = total_seconds/60;
            return str(int(min))+ " minutes ago"
        elif total_seconds<86400:
            hrs = (total_seconds/60)/60
            return str(int(hrs)) + " hours ago"
        elif total_seconds<2592000:
            day = ((total_seconds/60)/60)/60
            return str(int(day)) + " days ago"
        elif total_seconds<31104000:
            month = (((total_seconds/60)/60)/60)/30
            return str(int(month)) + " months ago"
        else:
            year = ((((total_seconds/60)/60)/60)/30)/12
            return str(int(year)) + " years ago"

    def __str__(self):
        return self.title



class ProdoctImage(models.Model):
    imageURL = models.ImageField(upload_to='product/')
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.imageURL

class Bidding(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    bidingprice = models.FloatField()
    date = models.DateField(auto_now=True)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=product_status, default='Pending')
    first_time = models.BooleanField(default=True)

    def __str__(self):
        return self.post.title

    class Meta:
        unique_together = ('post','user')
