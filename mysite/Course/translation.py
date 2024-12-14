from .models import Course, Category, Lesson, Exam
from modeltranslation.translator import TranslationOptions, register


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('course_name', 'description')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(Lesson)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(Exam)
class ProductComboTranslationOptions(TranslationOptions):
    fields = ('title',)
