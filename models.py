from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import uuid
from mptt.models import MPTTModel
from django.db import models
from django.utils.html import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.forms import ModelForm, TextInput, Textarea
from django.contrib.auth.models import User
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.db.models import Avg, Count
# Create your models here.
import uuid
from instructor.models import Instructor_Profile



class Profile(models.Model):
    uid = models.UUIDField(default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,related_name='profile')
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    role = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=50, null=True)
    address = models.CharField(blank=True, max_length=150)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=50)
    otp = models.CharField(max_length=6,null=True,blank=True)
    image = models.ImageField(upload_to='Students/User-Profile', null=True)


    def __str__(self):
        return self.first_name


class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(blank=True,max_length=20)
    email = models.CharField(blank=True,max_length=50)
    message = models.TextField(blank=True,max_length=255)
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name






# class FAQ_Category(models.Model):
#     slug = models.CharField(max_length=100, null=False, unique=True)
#     faq_category = models.CharField(max_length=100, default=" ", blank=True)
#     status = models.BooleanField(default="", help_text="0=default, 1=Hidden")
#     create_at = models.DateTimeField(auto_now_add=True,)
#     update_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name_plural = '6.FAQ Category'
#
#     def __str__(self):
#         return self.faq_category
#
#
# class FAQ(models.Model):
#     STATUS = (
#         ('True', 'True'),
#         ('False', 'False'),
#     )
#     faq_category = models.ForeignKey(FAQ_Category, on_delete=models.CASCADE)
#     question = models.CharField(max_length=200)
#     answer = RichTextUploadingField()
#     status = models.CharField(max_length=10, choices=STATUS)
#     create_at = models.DateTimeField(auto_now_add=True)
#     update_at = models.DateTimeField(auto_now=True)
#
#
#     class Meta:
#         verbose_name_plural = '7.FAQ'
#
#     def __str__(self):
#         return self.question
#





class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    company_name = models.CharField(max_length=50)
    company_logo = models.ImageField(upload_to='Students/Company-Setting-Image', blank=True)
    company_description = models.CharField(max_length=255)
    address = models.CharField(blank=True,max_length=100)
    map_link = models.CharField(blank=True,max_length=100)
    phone_1 = models.CharField(blank=True,max_length=15)
    phone_2 = models.CharField(blank=True,max_length=15)
    email = models.CharField(blank=True,max_length=50)
    copy_right = models.CharField(blank=True,max_length=100)
    about_us = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    privacy_policy = RichTextUploadingField(blank=True)
    terms_of_Service = RichTextUploadingField(blank=True)
    Purchase_guide = RichTextUploadingField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


class Social_Media(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    name = models.CharField(max_length=50)
    icon = models.CharField(blank=True, max_length=50)
    link = models.CharField(blank=True, max_length=50)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Settings_Home(models.Model):
    main_title = models.CharField(blank=True, max_length=50)
    main_title_paragraph = models.CharField(blank=True, max_length=100)
    heading_1 = models.CharField(blank=True, max_length=50)
    paragraph_1 = models.CharField(blank=True, max_length=100)
    heading_2 = models.CharField(blank=True, max_length=50)
    paragraph_2 = models.CharField(blank=True, max_length=100)
    heading_3 = models.CharField(blank=True, max_length=50)
    paragraph_3 = models.CharField(blank=True, max_length=100)
    trending_heading_course = models.CharField(blank=True, max_length=100)
    trending_paragraph_course = models.CharField(blank=True, max_length=100)
    student_heading = models.CharField(blank=True, max_length=100)
    student_paragraph = models.CharField(blank=True, max_length=100)
    trending_category_heading = models.CharField(blank=True, max_length=100)
    trending_category_paragraph = models.CharField(blank=True, max_length=100)
    popular_heading = models.CharField(blank=True, max_length=100)
    popular_paragraph = models.CharField(blank=True, max_length=100)
    price_heading = models.CharField(blank=True, max_length=100)
    price_paragraph = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.main_title

