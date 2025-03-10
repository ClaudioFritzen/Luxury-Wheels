from django.shortcuts import render

# Create your views here.
def lista_carros(request):
    carros = {
    "Toyota": "Corolla",
    "Ford": "Mustang",
    "Chevrolet": "Camaro",
    "Honda": "Civic",
    "BMW": "Série 3",
    "Mercedes-Benz": "Classe C",
    "Audi": "A4",
    "Tesla": "Model 3",
    "Volkswagen": "Golf",
    "Mazda": "CX-5"
}
    return render(request, "carros/carros.html")