from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from .models import *


class UserResource(resources.ModelResource):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'userprofile__image', 'userprofile__address', 
        			'userprofile__phone_number', 'userprofile__patronymic', 'userprofile__birth', 'userprofile__school_class', 
        			'userprofile__school', 'userprofile__district', 'userprofile__merit',
        			)


class UserResource2(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name',)
        

class LocationResource(resources.ModelResource):
    class Meta:
        model = Location
        fields = ('id', 'name', 'lon', 'lat')
        import_id_fields = ('id',)  # Используем id для обновления существующих записей


class SchoolResource(resources.ModelResource):
    location = fields.Field(
        column_name='location',
        attribute='location',
        widget=ForeignKeyWidget(Location, 'id')  # ищем по ID
    )

    class Meta:
        model = School
        fields = ('id', 'title', 'location',)
        import_id_fields = ('id',)  # обновляем по id
        use_bulk = True  # ускоряет импорт
        batch_size = 1000  # регулируй при необходимости