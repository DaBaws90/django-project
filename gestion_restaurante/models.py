import sys
from django.db import models
from gestion_clientes.models import Review, Customer
from django.core.validators import DecimalValidator, MinValueValidator, MaxValueValidator
import time
from django.db.models.signals import pre_save
from django.dispatch import receiver
import reversion

# Create your models here.

@reversion.register()
class Place(models.Model):
    address = models.CharField(max_length = 40, verbose_name = "Dirección")
    zipCode = models.IntegerField(verbose_name= "Código postal", null= True, blank= True, 
        validators=[MinValueValidator(0, message='El valor mínimo es de 1.'), MaxValueValidator(99999, message="No más de 5 cifras")])
    city = models.CharField(max_length = 30, verbose_name = "Ciudad")
    country = models.CharField(max_length = 30, verbose_name = "País")

    @property
    def full_address(self):
        return "{}, in {} ({}), with ZIP Code {}".format(self.address, self.city, self.country, self.zipCode)

    def __str__(self):
        return "{}".format(self.full_address)

    class Meta:
        verbose_name = "Lugar"
        verbose_name_plural = "Lugares"
        ordering = ('address', 'city', 'country', 'zipCode')


@reversion.register()
class Product(models.Model):
    name = models.CharField(max_length = 30, verbose_name = "Producto")
    description = models.TextField(max_length = 120, verbose_name = "Descripción", null= True, blank= True)
    created = models.DateTimeField(auto_now_add= True, verbose_name= "Fabricado el")
    updated = models.DateTimeField(auto_now= True, verbose_name= "Modificado el")

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ('name', 'created', 'updated')


@reversion.register()
class Order(models.Model):
    order_ref = models.BigIntegerField(verbose_name= "ID Referencia", editable=False)
    product = models.ForeignKey(Product, verbose_name = "Productos", on_delete = models.CASCADE, related_name= "productOrder")
    customer = models.ForeignKey(Customer, verbose_name = "Cliente", on_delete = models.CASCADE, related_name= "customerOrder", 
        null = True, blank = True)
    date = models.DateTimeField(auto_now_add=True, verbose_name= "Fecha")
    weigth = models.DecimalField(verbose_name="Peso", blank=True, null=True, validators=[MinValueValidator(0.01)], max_digits=7, decimal_places=2)
    stock = models.IntegerField(verbose_name= "Unidades", blank=True, null=True)
    comment = models.CharField(max_length = 150, verbose_name = "Comentario", null = True, blank = True)

    def __str__(self):
        return "Pedido # {}".format(self.order_ref)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ('date', 'product', 'customer', 'stock', 'weigth')

@receiver(pre_save, sender = Order)
def pre_save_ref(sender, **kwargs):
    if not kwargs['instance'].order_ref:
        ref = int(round(time.time() * 1000))
        kwargs['instance'].order_ref = ref


@reversion.register()
class Restaurant(models.Model):
    name = models.CharField(max_length = 35, verbose_name = "Nombre")
    place = models.OneToOneField(Place, on_delete = models.CASCADE, verbose_name = "Ubicación", primary_key = True)
    built = models.DateField(verbose_name= "Contruido el ")
    capacity = models.IntegerField(verbose_name= "Aforo", validators=[MinValueValidator(0)])

    def __str__(self):
        return "{} - {}".format(self.name, self.place)

    class Meta:
        verbose_name = "Restaurante"
        verbose_name_plural = "Restaurantes"
        ordering = ('name', 'built', 'capacity')

@receiver(pre_save, sender = Restaurant)
def pre_save_place(sender, **kwargs):
    place = Place.objects.get(id = kwargs['instance'].place.id)
    Restaurant.objects.filter(name = kwargs['instance'].name).update(place = place)