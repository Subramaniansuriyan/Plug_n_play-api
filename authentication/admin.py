from django.contrib import admin
from authentication.models import Otp

# Register your models here.



class OtpAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    search_fields = ('otp', 'user')
    list_display = ('otp', 'user')
admin.site.register(Otp,OtpAdmin)