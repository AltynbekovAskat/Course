from .models import *
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'



class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    av_rating = serializers.SerializerMethodField
    total_person = serializers.SerializerMethodField

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'price', 'category', 'av_rating', 'total_person']


        def get_av_rating(self, obj):
            return obj.get_av_rating()

        def get_total_person(self, obj):
            return obj.get_total_person()


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    course_assignment = AssignmentSerializer()
    exam = ExamSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['course_name', 'description', 'category', 'level', 'created_by', 'course_assignment', 'exam']

