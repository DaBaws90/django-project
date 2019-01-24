import sys
from django.db import models
from gestion_clientes.models import Review, Customer
from django.core.validators import DecimalValidator, MinValueValidator
import time

# Create your models here.

class Place(models.Model):
    address = models.CharField(max_length = 40, verbose_name = "Dirección")
    zipCode = models.IntegerField(verbose_name= "Código postal", null= True, blank= True)
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


class Product(models.Model):
    name = models.CharField(max_length = 30, verbose_name = "Producto")
    description = models.TextField(max_length = 80, verbose_name = "Descripción")
    stock = models.IntegerField(verbose_name= "Unidades", blank=True, null=True)
    weigth = models.DecimalField(verbose_name="Peso", blank=True, null=True, validators=[DecimalValidator],max_digits = 7 , decimal_places = 2)
    created = models.DateTimeField(auto_now_add= True, verbose_name= "Fabricado el")
    updated = models.DateTimeField(auto_now= True, verbose_name= "Modificado el")

    def __str__(self):
        return "Producto: {}".format(self.name)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ('name','stock','weigth', 'created', 'updated')



class Order(models.Model):
    # order_ref = models.AutoField(verbose_name= "ID Referencia", editable=False)
    product = models.ForeignKey(Product, verbose_name = "Productos", on_delete = models.CASCADE, related_name= "productOrder")
    customer = models.ForeignKey(Customer, verbose_name = "Cliente", on_delete = models.CASCADE, related_name= "customerOrder")
    date = models.DateTimeField(auto_now_add=True, verbose_name= "Fecha")
    comment = models.CharField(max_length = 150, verbose_name = "Comentario")

    @property
    def order_ref(self):
        return int(round(time.time() * 1000))

    def __str__(self):
        return "Pedido # {}, at {}".format(self.order_ref, self.date)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ('date',)



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
