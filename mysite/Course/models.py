from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    user_name = models.CharField(max_length=32)
    ROLE_CHOICES = [
        ('студент', 'студент'),
        ('препадватель', 'преподаватель'),
        ('администратор', 'администратор'),
    ]

    role = models.CharField(max_length=40, choices=ROLE_CHOICES, default='студент')

    def __str__(self):
        return f'{self.user_name}'


class Teacher(models.Model):
    teacher_name = models.CharField(max_length=57)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='picture/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_owner')
    phone_number = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return f'{self.teacher_name}, {self.owner}'


class Category(models.Model):
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f'{self.category_name}'


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    LEVEL_CHOICES = [
        ('начальный', 'начальный'),
        ('cредний', 'cредний'),
        ('продвинутый', 'продвинутый')
    ]
    level = models.CharField(max_length=55, choices=LEVEL_CHOICES)
    price = models.PositiveIntegerField(null=True, blank=True)
    detail_price = models.PositiveIntegerField(null=True, blank=True)
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='created_by')
    create_at = models. DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True)
    language = models.CharField(max_length=32)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_user')

    def get_avg_rating(self):
        ratings = self.course_reviews.all()
        if ratings.exists():
            return round(sum(i.rating for i in ratings) / ratings.count(), 1)
        return 0

    def get_total_people(self):
        ratings = self.course_reviews.all()
        if ratings.exists():
            if ratings.count() > 3:
                return f'3+'
            return ratings.count()
        return 0

    def get_count_rating(self):
        ratings = self.course_reviews.all()
        if ratings.exists():
            return ratings.count()
        return 0

    def __str__(self):
        return f'{self.course_name}, {self.category}'


class CourseMaterial(models.Model):
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    course_material = models.FileField(upload_to='material/')
    description = models.TextField()




class Lesson(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField()
    course_lesson = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_lessons')

    def __str__(self):
        return f'{self.title}, {self.course_lesson}'


class LessonVideo(models.Model):
    video = models.FileField(upload_to='lesson_video/', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='video')


class LessonFile(models.Model):
    file = models.FileField(upload_to='lesson_file/', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='files')


class Student(models.Model):
    student_name = models.CharField(max_length=32)
    student_bio = models.TextField()
    phone_number = PhoneNumberField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_picture/')
    student_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_owner')

    def __str__(self):
        return f'{self.student_bio}, {self.student_owner}'


class Assignment(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    due_date = models.DateTimeField(auto_now_add=True)
    course_assignment = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_assignment')
    students = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignment_student')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_assignment')

    def __str__(self):
        return f'{self.title}, {self.course_assignment}'


class Exam(models.Model):
    title = models.CharField(max_length=32)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exam')
    passing_score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 101)], verbose_name='Баллы')
    duration = models.DateField()

    def __str__(self):
        return f'{self.title}, {self.passing_score}'

    # models.py


class Question(models.Model):
    text = models.CharField(max_length=255)  # Текст вопроса
    option_1 = models.CharField(max_length=255)  # Вариант ответа 1
    option_2 = models.CharField(max_length=255)  # Вариант ответа 2
    option_3 = models.CharField(max_length=255)  # Вариант ответа 3
    option_4 = models.CharField(max_length=255)  # Вариант ответа 4
    correct_option = models.IntegerField()  # Индекс правильного ответа (от 1 до 4)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='question')

    def __str__(self):
        return f'{self.text}'

    def check_answer(self, answer_index):
        """Проверка, является ли выбранный ответ правильным"""
        return answer_index == self.correct_option


class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')
    course_certificate = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_certificates')
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate = models.CharField(max_length=32)
    certificate_url = models.FileField(upload_to='PDF/', null=True, blank=True)


    def __str__(self):
        return f'{self.student}, {self.certificate}'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        total_price = sum(item.get_total_price() for item in self.items.all())
        discount = 0

        final_price = total_price * (1 - discount)
        return final_price


class CarItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='item', on_delete=models.CASCADE)
    course_item = models.ForeignKey(Course, related_name='course', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_total_price(self):
        return self.course_item.price * self.quantity


    def __str__(self):
        return f'{self.course_item}, {self.quantity}'


class Review(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='user')
    course_review = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_reviews')
    instructor = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_review')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f'{self.user}, {self.course_review}'
