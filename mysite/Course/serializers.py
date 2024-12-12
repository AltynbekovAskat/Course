from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class TeacherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['teacher_name']


class TeacherDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['teacher_name', 'bio']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class CourseMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseMaterial
        fields = ['courses', 'course_material', 'description']


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


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text', 'option_1', 'option_2', 'option_3', 'option_4']


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
        fields = ['user', 'course_review', 'instructor', 'rating', 'comment']


class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    avg_rating = serializers.SerializerMethodField()
    total_people = serializers.SerializerMethodField()
    count_rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'price', 'category', 'avg_rating', 'total_people', 'count_rating']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_total_people(self, obj):
        return obj.get_total_people()

    def get_count_rating(self, obj):
        return obj.get_count_rating()


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    #`course_assignment = AssignmentSerializer()
    exam = ExamSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    total_people = serializers.SerializerMethodField()
    course_reviews = ReviewSerializer(many=True, read_only=True)
    owner = UserSimpleSerializer()
    created_by = TeacherListSerializer()
    materials = CourseMaterialSerializer(many=True, read_only=True)
    teacher_review = ReviewSerializer(many=True, read_only=True)
    question = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['course_name', 'category', 'description', 'created_by', 'avg_rating', 'total_people', 'update_at',
                  'materials', 'teacher_review', 'exam', 'question', 'course_reviews', 'owner']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_total_people(self, obj):
        return obj.get_total_people()
