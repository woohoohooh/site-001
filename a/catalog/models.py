import re
from django.db import models

def custom_slugify(value):
    value = re.sub(r'[^\w\s\-]', '', value)
    value = re.sub(r'\s+', '-', value)
    value = value.lower()
    return value

class Rubrics(models.Model):
    name_original = models.CharField('Рубрика', max_length=1000, null=True, blank=True, default='')
    visible = models.BooleanField('Отображать', default=False)
    slug = models.SlugField(unique=True, allow_unicode=True, max_length=1000)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = custom_slugify(self.name_original)
        super().save(*args, **kwargs)
    def __str__(self):
        return str(self.name_original)

class Company(models.Model):
    rubrics = models.ManyToManyField(Rubrics, blank=True)
    org_name1 = models.CharField('Название 1', max_length=1000, null=True, blank=True, default='')
    org_name2 = models.CharField('Название 2', max_length=1000, blank=True, default='')
    org_name3 = models.CharField('Название 3', max_length=1000, blank=True, default='')
    mainnew = models.TextField('Адрес', null=True, blank=True, default='')
    address_comment = models.CharField('Комментарий', max_length=1000, null=True, blank=True, default='')
    contact_groups_contacts1_text1 = models.CharField('Контакт', max_length=1000, blank=True, default='')
    contact_groups_contacts1_text2 = models.CharField('Контакт', max_length=1000, blank=True, default='')
    contact_groups_contacts1_text3 = models.CharField('Контакт', max_length=1000, blank=True, default='')
    contact_groups_contacts2_text1 = models.CharField('Контакт', max_length=1000, blank=True, default='')
    contact_groups_contacts2_text2 = models.CharField('Контакт', max_length=1000, blank=True, default='')
    contact_groups_contacts2_text3 = models.CharField('Контакт', max_length=1000, blank=True, default='')
    ads_article = models.CharField('Инфо', max_length=3000, blank=True, default='')
    article_warning = models.CharField('Доп инфо', max_length=1000, blank=True, default='')
    description = models.TextField('Описание', blank=True, default='')
    visible = models.BooleanField('Отображать', default=True, null=True)
    pro = models.BooleanField('PRO', null=True, default=False)
    slug = models.SlugField(unique=True, allow_unicode=True, max_length=1000)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = custom_slugify(self.org_name1)
        super().save(*args, **kwargs)
    def __str__(self):
        return str(self.org_name1)

class CompanyRubrics(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    rubric = models.ForeignKey(Rubrics, on_delete=models.CASCADE)

class Comment(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=300, default='Anonymous')
    content = models.TextField()
    is_positive = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.company}"