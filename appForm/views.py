from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from appForm.forms import FormCep
from appForm.models import Cep
import requests

def registrar_cep(request):
    if request.method == 'POST':
        cep = request.POST.get('cep')

        # Validar e salvar no banco de dados
        novo_cep = CepModel.objects.create

        # Disparar a DAG do Airflow
        url = 'http://localhost:8080/api/v1/dags/django_cep_dag/dagRuns'
        headers = {'Authorization': 'Basic base64usuario:senha'}  # Substitua pelo seu usuário e senha
        response = requests.post(url, json={}, headers=headers)

        if response.status_code == 200:
            return JsonResponse({'status': 'sucesso'})
        else:
            return JsonResponse({'status': 'erro'})

    return render(request, 'registrar_cep.html')


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