from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from .models import Patient

def lista_pacientes(request):
    search_query = request.GET.get('q', '').strip()

    pacientes_ativos = Patient.objects.filter(is_active=True).order_by('name')
    pacientes_historico = Patient.objects.filter(is_active=False).order_by('name')

    # Busca por nome
    if search_query:
        pacientes_ativos = pacientes_ativos.filter(name__incontains=search_query)
        pacientes_historico = pacientes_historico.filter(name__incontains=search_query)

        pacientes_ativos = pacientes_ativos.order_by('name')
        pacientes_historico = pacientes_historico.order_by('name')

    return render(request, 'pacientes/lista.html', {
        'pacientes': pacientes_ativos,
        'pacientes_historico': pacientes_historico,
        'search_query': search_query,
    })

#Alterar status
@require_POST
def mudar_status(request, pk):
    paciente = get_object_or_404(Patient, pk=pk)
    novo_status = request.POST.get('status')

    if novo_status:
        paciente.status = novo_status
        if request.user.is_authenticated:
            paciente.updated_by = request.user
        paciente.save()
        messages.success(request, f"Status de {paciente.name} atualizado.")

        return redirect('paciente:lista')

#Gerar alta paciente
@require_POST
def dar_alta(request, pk):
    paciente = get_object_or_404(Patient, pk=pk)
    paciente.is_active = False
    paciente.status = 'em_alta'
    if request.user.is_authenticated:
        paciente.updated_by = request.user
    paciente.save()
    messages.warning(request, f"Paciente {paciente.name} recebeu alta.")
    return redirect('paciente:lista')

#Retorno de paciente
@require_POST
def retorno_paciente(request, pk):
    paciente = get_object_or_404(Patient, pk=pk)
    paciente.is_active = True
    paciente.status = 'aguardando'
    if request.user.is_authenticated:
        paciente.updated_by = request.user
    paciente.save()
    messages.info(request, f"Paciente {paciente.name} adicionado com sucesso.")
    return redirect('paciente:lista')