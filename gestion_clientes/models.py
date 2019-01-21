from django.db import models
from django.utils.timezone import now
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, verbose_name = "Usuario", on_delete = models.SET_NULL, null = True, blank = True)
    MALE = "M"
    FEMALE = "F"
    GENDER_OPTS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    name = models.CharField(max_length = 30, verbose_name = "Nombre")
    middlename = models.CharField(max_length = 40, verbose_name = "Primer apellido")
    lastname = models.CharField(max_length = 40, verbose_name = "Segundo apellido")
    gender = models.CharField(max_length = 1, choices = GENDER_OPTS, default = MALE)
    birthday = models.DateField(verbose_name = "Fecha de nacimiento")
    address = models.CharField(max_length = 80, verbose_name = "Dirección")
    email = models.EmailField(max_length = 254, verbose_name = "Correo electrónico", null = True, blank = True)
    image = models.ImageField(null = True, blank = True, verbose_name= "Foto", upload_to = "gestion_clientes/static/clientes/images/")
    registered = models.DateTimeField(auto_now_add = True, verbose_name= "Fecha de registro")
    updated = models.DateTimeField(auto_now= True, verbose_name = "Fecha de edición")
    # slug = models.SlugField()
    
    # @receiver(post_save, sender=User)
    # def create_user_customer(sender, instance, created, **kwargs):
    #     if created:
    #         Customer.objects.create(user = instance)

    @property
    def edad(self):
        if self.birthday is not None:
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
        ordering = ("name", "birthday", "registered", "updated")


class Review(models.Model):
    title = models.CharField(max_length = 40, verbose_name = "Título")
    content = models.TextField(max_length = 400, verbose_name = "Contenido")
    published = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de publicación")
    valoration = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name = "Valoración")
    edited = models.DateTimeField(auto_now = True, verbose_name = "Fecha de edición")
    author = models.ForeignKey(Customer, on_delete = models.CASCADE, verbose_name = "Escrito por", related_name= "reviews")

    def info(self):
        return "{}, por {}".format(self.title, self.author)

    def __str__(self):
        return "{}".format(self.info())

    class Meta:
        verbose_name = "Opinión"
        verbose_name_plural = "Opiniones"
        ordering = ("title", "published", "edited", "valoration")