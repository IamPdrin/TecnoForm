from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from appForm.forms import FormCep
from appForm.models import Cep


def appForm(request):

    cepList = Cep.objects.all().values()

    context = {
        'ceps' : cepList
    }

    template = loader.get_template("home.html")

    return HttpResponse(template.render(context))


def excluir_cep(request, id_cep):
    cep = Cep.objects.get(id = id_cep)

    cep.delete()

    return redirect('appForm')


def add_cep(request):
    formCep = FormCep(request.POST or None)

    if request.POST:
        if formCep.is_valid(): #Além de verificar se é válido, criar código de consumo de API que verifique se o CEP existe (por meio da ViaCep) e depois a pipeline odeio lies of p, furia primordial and jojo
            formCep.save()

            return redirect('appForm')

    context = {
        'form' : formCep
    }

    return render(request, 'add_cep.html', context)


def editar_cep(request, id_cep):
    cep = Cep.objects.get(id = id_cep)

    form = FormCep(request.POST or None, instance=cep)

    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('appForm')
    context = {
        'form' : form
    }

    return render(request, 'editar_cep.html', context)