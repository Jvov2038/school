from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import School, Location

class LocationResource(resources.ModelResource):
    class Meta:
        model = Location
        fields = ('id', 'name', 'lon', 'lat')
        import_id_fields = ('id',)  # Используем id для обновления существующих записей


class SchoolResource(resources.ModelResource):
    # Поле location как ForeignKey
    location = fields.Field(
        column_name='location',
        attribute='location',
        widget=ForeignKeyWidget(Location, 'name')  # Используем поле 'name' для поиска
    )

    class Meta:
        model = School
        fields = ('id', 'title', 'site', 'email', 'address', 'location')
        import_id_fields = ('id',)  # Используем id для обновления существующих записей

    def before_import_row(self, row, **kwargs):
        """
        Обрабатываем location перед импортом.
        Если location не существует, создаём его.
        """
        location_name = row.get('location')
        if location_name:
            Location.objects.get_or_create(name=location_name)