import os
import sys
import platform

#путь к проекту
sys.path.insert(0, '/home/v/vertex9818/school/public_html/')
#путь к фреймворку
sys.path.insert(0, '/home/v/vertex9818/school/public_html/school/')
#путь к виртуальному окружению
sys.path.insert(0, '/home/v/vertex9818/school/public_html/venv/lib/python3.10/site-packages/')
os.environ["DJANGO_SETTINGS_MODULE"] = "school.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
