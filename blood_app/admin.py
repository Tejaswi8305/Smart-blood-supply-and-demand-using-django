from django.contrib import admin
from .models import Donor, Hospital, BloodRequest, BloodStock, UserProfile

admin.site.register(Donor)
admin.site.register(Hospital)
admin.site.register(BloodRequest)
admin.site.register(BloodStock)
admin.site.register(UserProfile)