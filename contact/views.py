from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    c = Contact.objects.filter(show=True)

    paginator = Paginator(c, 10)  # Show 10 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    contexto = { 
        "title": "Página Inicial",
        "page_obj": page_obj
        }
    return render (
        request,

        'contact/index.html',
        contexto
    )

def contact(request, contact_id):
    # c = Contact.objects.filter(id=contact_id, show=True).first()
    c = get_object_or_404(Contact.objects, id=contact_id, show=True)
    contexto = { 
        "title": "Dados do contato",
        "contact": c
        }
    return render (
        request,
        'contact/contact.html',
        contexto
    )

def search(request):
    search_value = request.GET.get('caixa_pesquisa').strip()

    if search_value == '':
        return redirect('contact:index')
    
    contacts = Contact.objects.filter(show=True) \
                    .filter(Q(first_name__icontains=search_value) | Q(last_name__icontains=search_value))\
                    .order_by('-id')
    
    paginator = Paginator(contacts, 10)  # Show 10 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    contexto = {
        'page_obj': page_obj,
        'title': 'Contatos encontrados'
    }

    return render (
        request,
        'contact/index.html',
        contexto
    )

