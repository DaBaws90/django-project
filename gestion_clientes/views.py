from django.shortcuts import render, get_object_or_404, get_list_or_404
from gestion_clientes.models import Customer, Review

# Create your views here.
def index(request):
    return render(request, "base/index.html")

def listCustomers(request):
    customers = get_list_or_404(Customer.objects.order_by("name"))
    context = {'customers': customers}
    return render(request, "clientes/index.html", context)

def customerDetails(request, customer_id):
    customer = get_object_or_404(Customer, id = customer_id)
    reviews = Review.objects.filter(author = customer) # Inyectamos la "relación" o lo recuperamos en el template 
        # desde el objeto customer (for X in customer.review_set.all)
    return render(request, "clientes/details.html", {'customer': customer, 'reviews': reviews}) # This is the context

def listReviews(request):
    reviews = get_list_or_404(Review.objects.order_by("valoration"))
    context = {'reviews': reviews}
    return render(request, "reviews/index.html", context)

def reviewDetails(request, review_id):
    # En una sola línea de código, aunque es menos legible (a veces menos es más, y viceversa)
    return render(request, "reviews/details.html", {'review': get_object_or_404(Review, id = review_id)})
