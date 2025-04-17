from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils import timezone
from import_export.admin import ImportExportModelAdmin

from .models import (
    Section, CategoryNews, News,
    CategoryLecture, Lecture,
    CategoryProg, Prog,
    Documents, Subscriber,
    ContactGroup, Contact, ContactRequest
)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(CategoryNews)
class CategoryNewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(News)
class NewsAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'get_photo', 'time_create', 'time_update', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width=50>")
        return None
    get_photo.short_description = 'Фото'


@admin.register(CategoryLecture)
class CategoryLectureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}


@admin.register(CategoryProg)
class CategoryProgAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Prog)
class ProgAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'get_photo', 'supervisor', 'time_create', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    filter_horizontal = ('registration',)
    prepopulated_fields = {"slug": ("title",)}

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width=50>")
        return None
    get_photo.short_description = 'Фото'


@admin.register(Documents)
class DocumentsAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'name_pdffile', 'is_published')
    list_display_links = ('id', 'title', 'is_published')
    search_fields = ('title',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    list_display_links = ('id', 'email')
    search_fields = ('email',)


@admin.register(ContactGroup)
class ContactGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'contacts_count')
    list_editable = ('order',)
    ordering = ('order',)

    def contacts_count(self, obj):
        return obj.contacts.count()
    contacts_count.short_description = "Кол-во контактов"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'phone', 'email', 'is_main', 'order')
    list_filter = ('group', 'is_main')
    list_editable = ('is_main', 'order')
    search_fields = ('name', 'phone', 'email')
    fieldsets = (
        (None, {
            'fields': ('group', 'name', 'is_main', 'order')
        }),
        ('Контактная информация', {
            'fields': ('phone', 'email', 'address', 'description')
        }),
    )


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact_link', 'created_at', 'is_new')
    list_filter = ('created_at', 'contact__group')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    def contact_link(self, obj):
        if obj.contact:
            return format_html('<a href="/admin/contacts/contact/{}/change/">{}</a>', obj.contact.id, obj.contact.name)
        return "-"
    contact_link.short_description = "Контакт"

    def is_new(self, obj):
        return obj.created_at.date() == timezone.now().date()
    is_new.boolean = True
    is_new.short_description = "Новый?"


# Настройки интерфейса админки
admin.site.site_title = 'Администрирование сайта'
admin.site.site_header = 'Администрирование сайта'
