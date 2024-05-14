#users/admin.py
from django.contrib import admin

# Register your models here.
class admin:
    def __init__(self):
        pass
    def register(self, model):
        admin.site.register(model)
