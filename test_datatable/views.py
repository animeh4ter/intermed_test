import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from test_datatable.models import Studies, Modalities


def init_db(request):
    return render(request, 'test_datatable/init_db.html')


def get_db_data(request):
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('size', 100)

    # Получаем параметры фильтрации из запроса
    search = request.GET.get('search', '')
    birthdate_search = request.GET.get('birthdateSearch', '')
    study_uid_search = request.GET.get('studyUidSearch', '')
    study_date_search = request.GET.get('studyDateSearch', '')
    modality_search = request.GET.get('modalitySearch', '')
    global_search = request.GET.get('globalSearch', '')

    # Создаем фильтрованный запрос
    studies_data = Studies.objects.select_related('study_modality').all()
    if global_search:
        studies_data = studies_data.filter(
            Q(study_uid__icontains=global_search) |
            Q(patient_fio__icontains=global_search) |
            Q(patient_birthdate__icontains=global_search) |
            Q(study_date__icontains=global_search) |
            Q(study_modality__name__icontains=global_search)
        )
    if search:
        studies_data = studies_data.filter(patient_fio__icontains=search)
    if birthdate_search:
        studies_data = studies_data.filter(
            patient_birthdate__icontains=birthdate_search)
    if study_uid_search:
        studies_data = studies_data.filter(
            study_uid__icontains=study_uid_search)
    if study_date_search:
        studies_data = studies_data.filter(
            study_date__icontains=study_date_search)
    if modality_search:
        studies_data = studies_data.filter(
            study_modality__name__icontains=modality_search)

    paginator = Paginator(studies_data, page_size)
    page_obj = paginator.get_page(page_number)

    data_list = []
    for study in page_obj:
        data_list.append({
            'ФИО пациента': study.patient_fio,
            'Дата рождения пациента': study.patient_birthdate.strftime(
                '%Y-%m-%d'),
            'UUID исследования': str(study.study_uid),
            'Дата исследования': study.study_date.strftime('%Y-%m-%d %H:%M:%S'),
            'Модальность': study.study_modality.name,
        })

    return JsonResponse({
        'data': data_list,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })


@csrf_exempt
def create_new(request):
    try:
        if request.method == 'POST':
            json_str = request.body.decode('utf-8')
            data_dict = json.loads(json_str)

            modality = Modalities.objects \
                .filter(name=data_dict['study_modality'])
            if modality:
                modality = modality.get()
                data_dict['study_modality'] = modality

            new_obj = Studies.objects.create(**data_dict)
            data_list = [{
                'ФИО пациента': new_obj.patient_fio,
                'Дата рождения пациента': new_obj.patient_birthdate,
                'UUID исследования': str(new_obj.study_uid),
                'Дата исследования': new_obj.study_date,
                'Модальность': new_obj.study_modality.name,
            }]

            return JsonResponse({'new_study': data_list})
    except ValidationError:
        return JsonResponse({'error': 'Вы ввели невалидный UUID '
                                      'проверьте данные'}, status=400)
    except Exception:
        return JsonResponse({'error': 'Непредвиденная ошибка'}, status=500)
    