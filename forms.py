from django import forms
from contact.models import Contact
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True,min_length=3,error_messages={'required': 'Esqueceu de preencher o primeiro nome!'},)
    last_name = forms.CharField(required=True,min_length=3,error_messages={'required': 'Esqueceu de preencher o último nome!'},)
    email = forms.EmailField(required=True,error_messages={'required': 'Esqueceu de preencher o email!'},)
    username = forms.CharField(required=True,min_length=3,error_messages={'required': 'Esqueceu de preencher o nome do utilizador!'},)

    class Meta:
        model = User
        fields = ('first_name','last_name','email','username',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Se existir algum utilizador com este mail
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Já existe um utilizador com este email'),
            )
        return email

class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget = forms.FileInput(attrs={'accept': 'image/*'})
    )
    class Meta:
        model = Contact
        fields = ('first_name','last_name','phone','email','description','category','picture')
        widgets = { 
                    'first_name': forms.TextInput(
                        attrs={'class': 'class-a', 'placeholder': 'Escreva o seu primeiro nome'}
                        )
                    }

    # def clean(self):
    #     cleaned_data = self.cleaned_data # Guarda os valores em um dicionário
    #     print(cleaned_data)
    #     # Simular um erro
    #     self.add_error(
    #         'first_name',
    #         ValidationError(
    #             'Dados em falta ou inválidos',
    #             code='invalid'
    #         )
    #     )
    #     return super().clean()

def create(request):
    form_action = reverse('contact:create')
    # print(form_action)
    if request.method == 'POST':
        form = ContactForm(request.POST,request.FILES)
    
        if form.is_valid():
            contact = form.save()
            return redirect('contact:update', contact_id = contact.id)
    else:
        form = ContactForm()

    contexto = { 'form': form, 'form_action': form_action }
    return render(request,'contact/create.html',contexto)

def update(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, show=True)
    form_action = reverse('contact:update', kwargs={'contact_id':contact_id})
    # print(form_action)
    if request.method == 'POST':
        form = ContactForm(request.POST,request.FILES,instance=contact)
    
        if form.is_valid():
            contact = form.save()
            return redirect('contact:update', contact_id = contact.id)
    else:
        form = ContactForm(instance=contact)

    contexto = { 'form': form, 'form_action': form_action }
    return render(request,'contact/create.html',contexto)

def delete(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    confirmation = request.POST.get('confirmation','no')
    if confirmation == 'yes':
        contact.delete()
        return redirect('contact:index')
    else:
        contexto = { 'contact': contact, 'confirmation': confirmation}
        return render(request,'contact/contact.html',contexto)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
        return render(request,'contact/register.html',{'form': form})
    form = RegisterForm()
    return render(request,'contact/register.html',{'form': form})