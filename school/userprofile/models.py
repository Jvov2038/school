from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django_admin_geomap import GeoItem
from main.fields import WEBPField
import uuid


def image_folder(instance, filename):
    return "photos/{}.webp".format(uuid.uuid4().hex)
    
    
class Location(models.Model, GeoItem):
	name = models.CharField(max_length=255)
	lon = models.FloatField(null=True, blank=True)
	lat = models.FloatField(null=True, blank=True)
	
	def __str__(self):
		return self.name
	
	@property
	def geomap_longitude(self):
		return '' if self.lon is None else str(self.lon)
		
	@property
	def geomap_latitude(self):
		return '' if self.lat is None else str(self.lat)

	@property
	def geomap_popup_view(self):
		return str(self)
		
	@property
	def geomap_popup_edit(self):
		return self.geomap_popup_view
		
	@property
	def geomap_popup_common(self):
		return self.geomap_popup_view
		
	@property
	def geomap_icon(self):
		return self.default_icon
		
	    # Свойство для возвращения координат в формате GeoJSON
	@property
	def geojson_coordinates(self):
		"""Возвращает координаты в формате GeoJSON"""
		if self.lon is not None and self.lat is not None:
			return {
				"type": "Point",
				"coordinates": [self.lon, self.lat]
				
			}
			return None


class SchoolClass(models.Model):
    school_class = models.CharField(max_length=10, null=True, blank=True, verbose_name="Учебный класс")
    grade = models.PositiveIntegerField(verbose_name="Класс")

    def __str__(self):
        return self.school_class

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'


class School(models.Model):
    title = models.CharField(max_length=512, null=True, blank=True, verbose_name="Название")
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="school", verbose_name="Местоположение", blank=True, null=True)
    
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Школа'
        verbose_name_plural = 'Школы'


class District(models.Model):
    district = models.CharField(max_length=100, null=True, blank=True, verbose_name="Муниципалитет")

    def __str__(self):
        return self.district

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'


class UserProfile(models.Model):
	class Genders(models.TextChoices):
		UNDEFINED = 'U', 'не выбран'
		MALE = 'M', 'мужской'
		FEMALE = 'F', 'женский'
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	gender = models.CharField(max_length=1, choices=Genders.choices, default=Genders.UNDEFINED, verbose_name='Пол')
	image = WEBPField(upload_to=image_folder, verbose_name="Фото", null=True, blank=True)
	address = models.CharField(max_length=255, null=True, blank=True)
	phone_number = PhoneNumberField(null=True, blank=True)
	patronymic = models.CharField(max_length=255, null=True, blank=True, verbose_name="Отчество")
	birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
	school_class = models.ForeignKey(SchoolClass, on_delete=models.PROTECT, verbose_name="Класс", null=True, blank=True)
	school = models.ForeignKey(School, on_delete=models.PROTECT, verbose_name="Школа", null=True, blank=True)
	district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name="Муниципалитет", null=True, blank=True)
	merit = models.TextField(blank=True, verbose_name="Заслуги", null=True)
	
	def __unicode__(self):
		return self.user
		
	class Meta:
		verbose_name = 'Профиль'
		verbose_name_plural = 'Профили'

