from django.contrib import admin
from scheduling.models import *


class TimeFrameInline(admin.TabularInline):
    model = TimeFrame
    extra = 2


class ShiftAdmin(admin.ModelAdmin):
    fieldset = [
        (None, {'fields': ['name']}),
    ]
    inlines = [TimeFrameInline]


class ScheduleAdmin(admin.ModelAdmin):
    fieldset = [
        (None, {'fields': ['name']}),
    ]


class ServiceAdmin(admin.ModelAdmin):
    fieldset = [
        (None, {'fields': ['testing_wat']}),
    ]


class EmployeeAdmin(admin.ModelAdmin):
    fieldset = [
        (None, {'fields': ['testing_wat']}),
    ]


class AppointmentAdmin(admin.ModelAdmin):
    fieldset = [
        (None, {'fields': ['testing_wat']}),
    ]


class CompanyAdmin(admin.ModelAdmin):
    fieldset = [
        (None, {'fields': ['testing_wat']}),
    ]


admin.site.register(Shift, ShiftAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Company, CompanyAdmin)

