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
from course.models import Level,Language,Category
from django.db.models import Avg, Count
# Create your models here.
import uuid

class Instructor_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=100, default=" ", blank=True)
    last_name = models.CharField(max_length=100, default=" ", blank=True)
    phone_number = models.IntegerField(default=" ", blank=True)
    email = models.CharField(max_length=100, default=" ", blank=True)
    password = models.CharField(max_length=100, default=" ", blank=True)
    image = models.ImageField(upload_to='Students/Instructor-image', blank=True)
    skill = models.CharField(max_length=100, default="", blank=True)
    instructor_dic = RichTextUploadingField(default="", blank=True)
    facebook_link = models.CharField(max_length=100, default="", blank=True)
    twitter_link = models.CharField(max_length=100, default="", blank=True)
    instagram_link = models.CharField(max_length=100, default="", blank=True)
    linkedin_link = models.CharField(max_length=100, default="", blank=True)
    status = models.BooleanField(help_text="0=default, 1=Hidden", null=True)
    trending = models.BooleanField(help_text="0=default, 1=Hidden",null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    class Meta:
        verbose_name_plural = '4.Instructor Profile'

    def __str__(self):
        return self.first_name





class Course(models.Model):
    STATUS = (
        ('Publish', 'Publish'),
        ('Draft', 'Draft'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    instructor = models.ForeignKey(Instructor_Profile, on_delete=models.CASCADE,null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE,null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE,null=True)
    slug = models.CharField(max_length=100, null=True, unique=True)
    course_name = models.CharField(max_length=100, null=True,)
    description = RichTextUploadingField(null=True)
    # requirement = RichTextUploadingField(null=True)
    # what_you_learn = RichTextUploadingField(null=True)
    status = models.CharField(choices=STATUS,max_length=10,null=True)
    trending = models.BooleanField(help_text="0=default, 1=Hidden",null=True)
    featured_course = models.BooleanField(help_text="0=default, 1=Hidden",null=True)
    original_price = models.FloatField(default=0)
    selling_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='Students/Course', blank=True)
    video = models.FileField(upload_to='Students/Course-Video', blank=True)
    deadline = models.CharField(max_length=10000, blank=True)
    certificate = models.CharField(default="False",max_length=10, null=True)

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
        else:
            return ""

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})

    def avaregereview(self):
        reviews = ReviewRating.objects.filter(course=self,status='Show').aggregate(avarage=Avg('rating'))
        avg=0
        if reviews["avarage"] is not None:
            avg=float(reviews["avarage"])
        return avg

    def countreview(self):
        reviews = ReviewRating.objects.filter(course=self,status='Show',).aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    class Meta:
        verbose_name_plural = '5. Course'

    def __str__(self):
        return self.course_name



class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor_Profile, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200,null=True)

    class Meta:
        verbose_name_plural = 'Lesson'

    def __str__(self):
        return self.name + " - " + self.course.course_name


class Course_Video(models.Model):
    STATUS = (
        ('Publish', 'Publish'),
        ('Draft', 'Draft'),
    )

    serial_number = models.IntegerField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,null=True)
    instructor = models.ForeignKey(Instructor_Profile, on_delete=models.CASCADE,null=True)
    caption = models.CharField(max_length=100,null=True)
    thumbnail = models.ImageField(upload_to='Students/Video-thumbnail', null=True)
    video = models.FileField(upload_to='Students/Course-Video', null=True)
    time_duration = models.IntegerField(null=True)
    preview = models.CharField(choices=STATUS,max_length=10,null=True)

    class Meta:
        verbose_name_plural = 'Video'

    def __str__(self):
        return self.caption


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + " - " + self.course.course_name

    @property
    def selling_price(self):
        return (self.course.selling_price)



class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    admin_note = models.CharField(blank=True,max_length=100)
    payment_mode = models.CharField(blank=True, max_length=150)
    payment_id = models.CharField(max_length=12, blank=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    phone = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=150)
    state = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    total = models.FloatField()
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['admin_note','payment_id','first_name','last_name','email','phone','city','state','country','note']


class UserCourse(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Approve', 'Approve'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    selling_price = models.FloatField(null=True)
    certificate = models.CharField(max_length=10, choices=STATUS, default='Pending')
    create_at = models.DateTimeField(auto_now_add=True,null=True)
    update_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.user.first_name + " - " + self.course.course_name




class ReviewRating(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Show','Show')

    )
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=500, blank=True)
    review = models.CharField(max_length=2500,blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10,choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class QuizQuestion(models.Model):
    course_video = models.ForeignKey(Course_Video, on_delete = models.CASCADE,null=True)
    question = models.TextField()
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models. CharField(max_length=200)
    level = models.ForeignKey(Level, on_delete=models.CASCADE,null=True)
    time_limit = models.IntegerField()
    right_option = models.CharField(max_length=200)

    def _str_(self):
        return self.question



class UserSubmittedAnswer(models.Model):
    question = models.TextField(null=True)
    questions = models.ForeignKey(QuizQuestion, on_delete = models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    right_answer = models.CharField(max_length=200)


class UserSubmittedAttempts(models.Model):
    course_video = models.ForeignKey(Course_Video, on_delete = models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.course_video



class Assignment(models.Model):
    STATUS = (
        ('Publish', 'Publish'),
        ('Draft', 'Draft'),
    )

    serial_number = models.IntegerField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,null=True)
    question = models.CharField(max_length=100,null=True)
    time_limit = models.IntegerField(null=True)
    preview = models.CharField(choices=STATUS,max_length=10,null=True)

    class Meta:
        verbose_name_plural = 'Assignment'

    def __str__(self):
        return self.question


class AssignmentSubmissions(models.Model):
    STATUS = (
        ('Publish', 'Publish'),
        ('Draft', 'Draft'),
    )
    question = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=100,null=True,blank=True,default="")


    class Meta:
        verbose_name_plural = 'Assignment Submission'


