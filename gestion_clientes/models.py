from django.db import models
from django.utils.timezone import now
from django.utils.text import slugify
import datetime
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
from django.contrib.auth.models import User
# from gestion_restaurante.models import Order
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import reversion
import easy_thumbnails.templatetags.thumbnail

# Create your models here.

@reversion.register()
class Customer(models.Model):
    user = models.OneToOneField(User, verbose_name = "Usuario", on_delete = models.CASCADE)
    MALE = "M"
    FEMALE = "F"
    GENDER_OPTS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    name = models.CharField(max_length = 30, verbose_name = "Nombre")
    middlename = models.CharField(max_length = 40, verbose_name = "Primer apellido")
    lastname = models.CharField(max_length = 40, verbose_name = "Segundo apellido")
    gender = models.CharField(max_length = 1, choices = GENDER_OPTS, default = MALE, verbose_name = "Género", help_text = "Seleccione su sexo")
    birthday = models.DateField(verbose_name = "Fecha de nacimiento", null = True, blank = True)
    address = models.CharField(max_length = 80, verbose_name = "Dirección")
    image = models.ImageField(null = True, blank = True, verbose_name= "Foto", upload_to = "images/")
    registered = models.DateTimeField(auto_now_add = True, verbose_name= "Fecha de registro")
    updated = models.DateTimeField(auto_now= True, verbose_name = "Fecha de edición")
    slug = models.SlugField()

    @property
    def edad(self):
        if self.birthday is not None:
            # Pendiente de convertir el date a string y luego a int
            bd = datetime.date(self.birthday)
            today = datetime.datetime.today()
            
            return today.year - bd.year - (today.month <= bd.month and today.day <= bd.day)
        else:
            return 0

    @property
    def fullname(self):
        return "{} {} {}".format(self.name, self.middlename, self.lastname)
        

    def __str__(self):
        return "{}".format(self.fullname)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ("name", "birthday", "registered", "updated", 'gender')

    def get_absolute_url(self):
        return reverse('customerDetails', kwargs={'id': self.id, 'slug': self.slug})

@receiver(post_save, sender=User)
def create_user_customer(sender, instance, created, **kwargs):
    print("instance: " + str(instance) + ", created: " + str(created) + ", kwargs: " + str(kwargs))
    if created:
        Customer.objects.create(user = instance)

@receiver(post_save, sender=User)
def update_user_customer(sender, instance, **kwargs):
    print("instance updated: " + str(instance) + ", kwargs: " + str(kwargs))
    temp = Customer.objects.filter(user=instance)
    if temp.count() > 0:
        # temp.first().save()
        instance.customer.save()

@receiver(pre_save, sender = Customer)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].fullname)
    kwargs['instance'].slug = slug


@reversion.register()
class Review(models.Model):
    title = models.CharField(max_length = 40, verbose_name = "Título")
    content = models.TextField(max_length = 400, verbose_name = "Contenido")
    published = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de publicación")
    valoration = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name = "Valoración")
    edited = models.DateTimeField(auto_now = True, verbose_name = "Fecha de edición")
    author = models.ForeignKey(Customer, on_delete = models.CASCADE, verbose_name = "Escrito por", related_name= "reviews", null = True, blank = True)

    def info(self):
        return "{}, por {}".format(self.title, self.author)

    @property
    def stars(self):
        if self.valoration > 0:
            return "Valoración ({})".format("*" * self.valoration)
        else:
            return "Valoración (0 estrellas)"

    def __str__(self):
        return "{}".format(self.info())

    class Meta:
        verbose_name = "Opinión"
        verbose_name_plural = "Opiniones"
        ordering = ("title", "published", "edited", "valoration")