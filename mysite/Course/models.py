from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_name = models.CharField(max_length=32, unique=True)
    ROLE_CHOICES = [
        ('студент', 'студент'),
        ('препадватель', 'преподаватель'),
        ('администратор', 'администратор'),
]
    role = models.CharField(max_length=40, choices=ROLE_CHOICES, default='клиент')

    def __str__(self):
        return f'{self.user_name}'


class Teacher(models.Model):
    teacher_name = models.CharField(max_length=57)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='picture/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_owner')

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
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    create_at = models. DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.course_name}, {self.category}'


class Lesson(models.Model):
    title = models.CharField(max_length=32)
    video_url = models.FileField(upload_to='video/', null=True, blank=True)
    content = models.TextField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE, related_name='course_lesson')

    def __str__(self):
        return f'{self.title}, {self.course}'


class Student(models.Model):
    student_name = models.CharField(max_length=32)
    student_bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_picture/')
    student_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_owner')

    def __str__(self):
        return f'{self.student_bio}, {self.student_owner}'


class Assignment(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    due_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_assignment')
    students = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignment_student')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_assignment')

    def __str__(self):
        return f'{self.title}, {self.course}'


class Questions(models.Model):
    questions_name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.questions_name}'


class Exam(models.Model):
    title = models.CharField(max_length=32)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exam')
    questions = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='questions')
    passing_score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 101)], verbose_name='Баллы')
    duration = models.DateField()

    def __str__(self):
        return f'{self.title}, {self.questions}'


class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_certificate')
    issued_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    certificate = models.CharField(max_length=32)
    certificate_url = models.FileField(upload_to='certificate_video/', null=True, blank=True)

    def __str__(self):
        return f'{self.student}, {self.certificate}'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f'{self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.course}, {self.quantity}'


class Review(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='user')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_review')
    instructor = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_review')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f'{self.user}, {self.course}'
