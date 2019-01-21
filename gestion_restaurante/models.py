from django.db import models
from gestion_clientes.models import Review, Customer
from django.core.validators import DecimalValidator

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
    weigth = models.DecimalField(verbose_name="Peso", blank=True, null=True, validators=[DecimalValidator(7, 2)])

    def __str__(self):
        return "Producto: {}".format(self.name)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ('name',)



class Order(models.Model):
    order_ref = models.BigIntegerField(max_length = 20)
    products = models.ManyToManyField(Product, verbose_name=_("Productos"))

    def __str__(self):
        return "Pedido # {}".format(self.order_ref)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ('order_ref',)



class NUSE(models.Model):
    pass



class Restaurant(models.Model):
    name = models.CharField(max_length = 35, verbose_name = "Nombre")
    place = models.OneToOneField(Place, on_delete = models.DO_NOTHING, verbose_name = "Ubicación")

    def __str__(self):
        return "{} - {}".format(self.name, self.place)

    class Meta:
        verbose_name = "Restaurante"
        verbose_name_plural = "Restaurantes"
        ordering = ('name',)
