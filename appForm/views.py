import json
from urllib import request, error
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from appForm.forms import FormCep
from appForm.models import Cep

def appForm(request):
    cepList = Cep.objects.all().values()
    context = {
        'ceps': cepList
    }
    template = loader.get_template("home.html")
    return HttpResponse(template.render(context))


def excluir_cep(request, id_cep):
    cep = Cep.objects.get(id=id_cep)
    cep.delete()
    return redirect('appForm')


def add_cep(request):
    formCep = FormCep(request.POST or None)

    if request.POST:
        if formCep.is_valid():
            cep = formCep.cleaned_data['cep']
            if validar_cep_via_cep(cep):  # Valida o CEP com a API ViaCEP
                formCep.save()
                return redirect('appForm')
            else:
                formCep.add_error('cep', 'O CEP informado não existe. Por favor, insira um CEP válido.')

    context = {
        'form': formCep
    }
    return render(request, 'add_cep.html', context)


def editar_cep(request, id_cep):
    cep = Cep.objects.get(id=id_cep)
    form = FormCep(request.POST or None, instance=cep)

    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('appForm')

    context = {
        'form': form
    }
    return render(request, 'editar_cep.html', context)


def validar_cep_via_cep(cep):
    
    """
    Valida o CEP usando a API ViaCEP.
    Retorna True se o CEP existir, caso contrário, False.
    """
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        with request.urlopen(url, timeout=5) as response:  # Define um timeout de 5 segundos
            if response.status == 200:
                data = json.loads(response.read().decode())
                if "erro" in data:
                    return False
                return True
            return False
    except (error.URLError, error.HTTPError, TimeoutError):
        return False  # Considere adicionar logs ou avisos em produção