from django.contrib import admin
from .models import Company, Rubrics, Comment

class RubricsAdmin(admin.ModelAdmin):
    list_display = ['name_original', 'visible']
    list_editable = ['visible']
    search_fields = ['name_original']

    actions = ['make_all_visible']

    def make_all_visible(modeladmin, request, queryset):
        queryset.update(visible=True)

    make_all_visible.short_description = "Сделать все рубрики видимыми"

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['org_name1', 'slug', 'mainnew', 'org_name2', 'ads_article', 'article_warning', 'description', 'org_name3', 'address_comment']
    search_fields = ['org_name1', 'mainnew']
    actions = ['delete_all']
    ordering = ['slug']
    # list_editable = ['mainnew', 'org_name2', 'ads_article', 'article_warning', 'description', 'org_name3', 'address_comment']
    # list_display_links = None
    # fields = ['org_name1'] + list_display[1:]

    def delete_all(self, request, queryset):
        queryset.delete()
    delete_all.short_description = "Delete all selected items"

admin.site.register(Company, CompanyAdmin)
admin.site.register(Rubrics, RubricsAdmin)
admin.site.register(Comment)
