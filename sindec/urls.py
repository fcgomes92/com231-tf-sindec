from django.conf.urls import url
from sindec.views import csv

urlpatterns = [
    url(r'^csv_init/$', csv.csv_test, name="dbinti"),
]
