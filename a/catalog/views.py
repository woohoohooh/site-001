from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, Rubrics, Comment
import datetime
from django.db.models import Q
import random
from django.db.models import F

def rubric_detail(request, slug):
    try:
        rubric_obj = Rubrics.objects.get(slug=slug)
        companies_with_rubric = Company.objects.filter(rubrics=rubric_obj, visible=True)
        return render(request, 'catalog/rubric_result.html',
                      context={'rubric': rubric_obj, 'companies': companies_with_rubric})
    except Rubrics.DoesNotExist:
        return HttpResponse('Rubric not found.')

def index(request):
    current_year = datetime.datetime.now().year
    rubrics = Rubrics.objects.filter(visible=True)
    return render(request, 'catalog/index.html',
                  context={'rubrics': rubrics, 'request': request, 'current_year': current_year})

def test(request):
    count = Company.objects.filter(
        Q(mainnew__icontains='Москва') &
        (Q(contact_groups_contacts1_text1__icontains='http') |
         Q(contact_groups_contacts1_text2__icontains='http') |
         Q(contact_groups_contacts1_text3__icontains='http') |
         Q(contact_groups_contacts2_text1__icontains='http') |
         Q(contact_groups_contacts2_text2__icontains='http') |
         Q(contact_groups_contacts2_text3__icontains='http') |
         Q(contact_groups_contacts1_text1__icontains='https') |
         Q(contact_groups_contacts1_text2__icontains='https') |
         Q(contact_groups_contacts1_text3__icontains='https') |
         Q(contact_groups_contacts2_text1__icontains='https') |
         Q(contact_groups_contacts2_text2__icontains='https') |
         Q(contact_groups_contacts2_text3__icontains='https'))
    ).count()

    find = Company.objects.filter(
        Q(mainnew__icontains='Москва') &
        (Q(contact_groups_contacts1_text1__icontains='http') |
         Q(contact_groups_contacts1_text2__icontains='http') |
         Q(contact_groups_contacts1_text3__icontains='http') |
         Q(contact_groups_contacts2_text1__icontains='http') |
         Q(contact_groups_contacts2_text2__icontains='http') |
         Q(contact_groups_contacts2_text3__icontains='http') |
         Q(contact_groups_contacts1_text1__icontains='https') |
         Q(contact_groups_contacts1_text2__icontains='https') |
         Q(contact_groups_contacts1_text3__icontains='https') |
         Q(contact_groups_contacts2_text1__icontains='https') |
         Q(contact_groups_contacts2_text2__icontains='https') |
         Q(contact_groups_contacts2_text3__icontains='https'))
    ).order_by('org_name1').distinct('org_name1')

    return render(request, 'catalog/test.html', {'find': find, 'count': count})

def company_detail(request, slug):
    company = get_object_or_404(Company, slug=slug)
    rubrics = Rubrics.objects.all()
    comments = company.comments.all().order_by('-created_at')
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')
        feedback_type = request.POST.get('feedback_type')
        fake_field = request.POST.get('fake_field', '')
        if fake_field:
            return HttpResponseForbidden('Вы не можете отправлять комментарии.')
        if name and content and feedback_type:
            is_positive = (feedback_type == 'positive')
            comment = Comment(company=company, name=name, content=content, is_positive=is_positive)
            comment.save()
            Comment.objects.filter(pk=comment.pk).update(created_at=F('created_at'))
            comments = company.comments.all().order_by('-created_at')
    return render(request, 'catalog/company_detail.html',
                  context={'company': company, 'rubrics': rubrics, 'comments': comments})

def toggle_visibility(request, pk):
    company = get_object_or_404(Company, pk=pk)
    company.visible = True
    company.save()
    return redirect('company_detail2', pk=pk)

def company_detail2(request, pk):
    company = get_object_or_404(Company, pk=pk)
    rubrics = Rubrics.objects.all()
    comments = company.comments.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')
        feedback_type = request.POST.get('feedback_type')
        fake_field = request.POST.get('fake_field', '')
        if fake_field:
            return HttpResponseForbidden('Вы не можете отправлять комментарии.')
        if name and content and feedback_type:
            is_positive = (feedback_type == 'positive')
            comment = Comment(company=company, name=name, content=content, is_positive=is_positive)
            comment.save()
    return render(request, 'catalog/company_detail2.html',
                  context={'company': company, 'rubrics': rubrics, 'comments': comments})

def add_comment(request, post_id):
    tmp_names = []
    with open('../../names.txt', 'r', encoding='utf8') as f:
        for i in f:
            tmp_names.append(i.replace('\n', ''))
    company = get_object_or_404(Company, pk=post_id)
    # Получаем slug компании
    slug = company.slug
    if request.method == 'POST':
        name = request.POST.get('na')
        content = request.POST.get('re')
        feedback_type = request.POST.get('feedback_type')
        fake_field = request.POST.get('name', '')
        if not name and tmp_names:
            name = random.choice(tmp_names)
        if fake_field:
            return HttpResponseForbidden('Вы не можете отправлять комментарии.')
        if name and content and feedback_type:
            is_positive = (feedback_type == 'positive')
            comment = Comment(company=company, name=name, content=content, is_positive=is_positive)
            comment.save()
            # Перенаправляем на страницу с использованием slug
            return redirect('company_detail', slug=slug)
    # Если что-то пошло не так или это GET-запрос, возвращаемся на страницу с формой
    return redirect('company_detail', slug=slug)

