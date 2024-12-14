from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserProSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age', 'phone_number', 'status',
                  'date_registered']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_date):
        user = User.objects.create_user(**validated_date)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),

        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Не верный пароль или логин ")


    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),

        }



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
        fields = ['id', 'course_name', 'price', 'detail_price', 'category', 'avg_rating', 'total_people',
                  'count_rating']

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
                  'materials', 'teacher_review', 'exam', 'question', 'course_reviews', 'owner', 'price', 'detail_price']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_total_people(self, obj):
        return obj.get_total_people()





class CarItemSerializer(serializers.ModelSerializer):
    course_item = CourseListSerializer()
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True,
                                                   source='courses')

    class Meta:
        model = CarItem
        fields = ['id', 'course_item', 'course_id', 'quantity', 'get_total_price']


class CartSerializer(serializers.ModelSerializer):
    item = CarItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Mate:
        model = Cart
        fields = ['id', 'user', 'item', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()

