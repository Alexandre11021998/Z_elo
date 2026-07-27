from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from .models import Pacientes
from datetime import datetime
import csv
import io

@require_POST
def importar_csv(request):
    csv_file = request.FILES.get('csv_file')

    if not csv_file:
        messages.error(request, 'Por favor, selecione um arquivo CSV.')
        return redirect('pacientes:lista')
    if not csv_file.name.endswith(('.csv', '.txt')):
        messages.error(request, 'Formato inválido! Envia um arquivo com extensão .csv ou .txt.')
        return redirect('pacientes:lista')
    try:
        #ler o arquvio enviado
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)

        #detecta o delimitador
        sample = decoded_file[:2048]
        delimiter = ';' if ';' in sample else ','

        reader = csv.reader(io_string, delimiter=delimiter)

        #ignorar cabeçalho
        header = next(reader, None)

        novos_pacientes = []
        erros = 0

        for row in reader:
            if len(row) >= 2:
                nome = row[0].strip().strip('"\'')
                data_str = row[1].strip().strip('"\'')

                if not nome or not data_str:
                    continue

                #Formatação de datas
                data_nascimento = None
                if '/' in data_str:
                    try:
                        data_nascimento = datetime.strptime(data_str, '%d/%m/%Y').date()
                    except ValueError:
                        erros += 1
                        continue
                    else:
                        try:
                            data_nascimento = datetime.strptime(data_str, '%Y-%m-%d').date()
                        except ValueError:
                            erros += 1
                            continue

                    if data_nascimento:
                        novos_pacientes.append(Pacientes(name=nome, data_nascimento=data_nascimento))

                if novos_pacientes:
                    #Criar pacientes no banco
                    Pacientes.objects.bulk_create(novos_pacientes)
                    messages.success(request, f'{len(novos_pacientes)} paciente(s) importado(s) com sucesso!')
                else:
                    messages.warning(request, 'Nenhuma paciente válido foi encontrado no arquivo')
                if erros > 0:
                    messages.info(request, f'{erros} linha(s) foram ignoradas devido a erros!')

    except Exception as e:
        messages.error(request, f'Erro ao precessar arquivo:{str(e)}')

    return redirect('pacientes:lista')

                        


def lista_pacientes(request):
    search_query = request.GET.get('q', '').strip()

    pacientes_ativos = Pacientes.objects.filter(is_active=True).order_by('name')
    pacientes_historico = Pacientes.objects.filter(is_active=False).order_by('name')

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
    paciente = get_object_or_404(Pacientes, pk=pk)
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
    paciente = get_object_or_404(Pacientes, pk=pk)
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
    paciente = get_object_or_404(Pacientes, pk=pk)
    paciente.is_active = True
    paciente.status = 'aguardando'
    if request.user.is_authenticated:
        paciente.updated_by = request.user
    paciente.save()
    messages.info(request, f"Paciente {paciente.name} adicionado com sucesso.")
    return redirect('paciente:lista')

#Acompanhamento do Paciente
def acompanhar_paciente(request, pk):
    Pacientes = get_object_or_404(Pacientes, pk=pk)

    steps = []
    for index, (code, label) in enumerate(Pacientes.STATUS_CHOICES):
        steps.append({
            'code': code,
            'label': label,
            'index': index,
            'is_completed': index < Pacientes.current_step_index,
            'is_current': index == Pacientes.current_step_index
        })
    return render(request, 'pacientes/acompanhar.html', {
        'pacientes': Pacientes,
        'steps': steps,
    })