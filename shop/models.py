from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=20, default='')
    product_desc = models.TextField(default='')
    product_date = models.DateField()
    product_image = models.ImageField(upload_to="shop1")
    product_price = models.CharField(max_length=10, default='')
    product_views = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name


class contacts(models.Model):
    id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000, default='')
    name = models.CharField(max_length=30, default='')
    password = models.CharField(max_length=40, default='')
    address = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=20, default='')
    state = models.CharField(max_length=40, default='')
    zip = models.CharField(max_length=7, default='')

    def __str__(self):
        return str(self.id)


class orderupdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default='')
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)


class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=13)
    slug = models.CharField(max_length=130)
    timestamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title


class Blogcomment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    # post = models.ForeignKey(product, on_delete=models.CASCADE,null=True)
    user = models.CharField(max_length=200,default="")
    post = models.CharField(max_length=200,default="")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment
