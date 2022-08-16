from distutils.command.upload import upload
from operator import le
from django.db import models
from django.db.models import *
from django.utils import  timezone
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
import stripe
from allauth.account.signals import email_confirmed
from django.conf import settings
User = get_user_model()
stripe.api_key=settings.STRIPE_SECRET_KEY

def user_directory_path(instance, filename):
    title = instance.title
    return 'courses/{0}/{1}'.format(title.replace(':',' '), filename)


def chapter_directory_path(instance, filename):
    title = instance.title

    return 'courses/{0}/{1}/{2}'.format(instance.course.title.replace(':',' '), title.replace(':',' '), filename)

def lesson_directory_path(instance, filename):
    return 'courses/{0}/{1}/Lesson #{2}:{3}/{4}'.format(instance.course, instance.chapter, instance.lesson_number,instance.title, filename)

class Author(Model):
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Pricing(Model):
    name = CharField(max_length=100)
    slug = SlugField(unique=True)
    stripe_price_id = CharField(max_length=50)
    price = DecimalField(decimal_places=2, max_digits=5)
    currency = CharField(max_length=50)

    def __str__(self):
        return self.name


class Subscription(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    price = ForeignKey(Pricing, on_delete=CASCADE, related_name='subscriptions') 
    created = DateTimeField(auto_now_add=True)
    stripe_subscription_id = CharField(max_length=50)
    status = CharField(max_length=100)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.user.email

    @property
    def is_active(self):
        return self.status == "active" or self.status == "trialing"


class Course(Model):
    authors = ManyToManyField(Author)
    pricing_tiers = ManyToManyField(Pricing, blank=True)
    title = CharField(max_length=100)
    subtitle = TextField()
    thumbnail = ImageField(upload_to = user_directory_path, blank = True, null = True)
    video = FileField(upload_to = user_directory_path)
    vimeo_video = CharField(verbose_name='Vimeo Video ID (optional)', max_length=100, blank=True, null=True)
    slug = SlugField(max_length=250,unique_for_date='published', null=False, unique=True)
    published = DateTimeField(default=timezone.now)
    is_active = BooleanField(default=True)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title    
    
    def get_absolute_url(self):
        return reverse("courses:detail", kwargs={
            'slug': self.slug
        })

def post_email_corfirmed(request, email_address, *args, **kwargs):
    user = User.objects.get(email = email_address.email)
    free_trial_pricing = Pricing.objects.get(name='Free Trial')
    subscription = Subscription.objects.create(user=user, price= free_trial_pricing)

    #Crear cliente en Stripe
    stripe_customer = stripe.Customer.create(
        email = user.email
    )
    stripe_subscription = stripe.Subscription .create(
        customer=stripe_customer["id"],
        items=[{'price':'price_1LWvwlAScEOg6Mo2eIeB2fuL'}],
        trial_period_days=7 
    )

    subscription.status = stripe_subscription["status"]
    subscription.stripe_subscription_id = stripe_subscription["id"]
    subscription.save()
    
    user.stripe_customer_id = stripe_customer["id"]
    user.save()


class Chapter(Model):
    course = ForeignKey(Course, on_delete=CASCADE, blank=True, null=True)
    chapter_number = IntegerField(blank=True,null=True)
    title = CharField(max_length=100)
    thumbnail = ImageField(upload_to = chapter_directory_path, blank =  True, null = True)
    video = FileField(upload_to = user_directory_path)
    vimeo_video = CharField(verbose_name='Vimeo Video ID (optional)', max_length=100, blank=True, null=True)
    content = TextField(blank=True, null=True)

    def __str__(self):
     return self.title  

    def get_absolute_url(self):
        return reverse("courses:chapter-detail", kwargs={
            'course_slug': self.course.slug,
            'chapter_number': self.chapter_number,
        })


class Lesson(Model):
    course = ForeignKey(Course, on_delete=CASCADE, blank=True, null=True)
    chapter = ForeignKey(Chapter, on_delete=CASCADE, blank=True, null=True)
    lesson_number = IntegerField(blank=True,null=True)
    title = CharField(max_length=100)
    thumbnail = ImageField(upload_to = chapter_directory_path, blank =  True, null = True)
    video = FileField(upload_to = user_directory_path)
    vimeo_video = CharField(verbose_name='Vimeo Video ID (optional)', max_length=100, blank=True, null=True)
    content = TextField(blank=True, null=True)

    def __str__(self):
        return self.title  
    
    def get_absolute_url(self):
        return reverse("courses:lesson-detail", kwargs={
            "course_slug": self.chapter.course.slug,
             'chapter_number': self.chapter.chapter_number,
             'lesson_number': self.lesson_number
             })
    
email_confirmed.connect(post_email_corfirmed) 