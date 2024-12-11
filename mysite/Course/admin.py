from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 1


class QuestionsInline(admin.TabularInline):
    model = Questions
    extra = 1


class ExamInline(admin.TabularInline):
    model = Exam
    extra = 1


class CourseMaterialInline(admin.TabularInline):
    model = CourseMaterial
    extra = 1


class LessonAdmin(admin.ModelAdmin):
    inlines = [AssignmentInline]


@admin.register(Course)
class AllAdmin(TranslationAdmin):
    inlines = [QuestionsInline, ExamInline, CourseMaterialInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(Lesson, LessonAdmin)
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Category)
admin.site.register(Student)
admin.site.register(Certificate)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Review)
