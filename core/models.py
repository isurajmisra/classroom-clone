from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Classroom(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='classrooms')
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100,null=True)
    c_code = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.name

class ClassPeople(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='classpeople')
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE,related_name='classpeople')


class Questions(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='questions')
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE,related_name='questions',default="1")
    text = models.TextField()
    answer = models.CharField(max_length=200,null=True)
    created_on = models.DateTimeField(auto_now=True)
    q_type = models.CharField(max_length=50)


class MultipleChoiceQuestions(models.Model):
    question = models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='mcq')
    option = models.CharField(max_length=300)
    answer = models.CharField(max_length=300,null=True)

class Answers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='answers')
    question = models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=True)

class MultipleChoiceAnswer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='mcq_a')
    question = models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='mcq_a')
    option = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=True)


class ClassroomSession(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='class_sessions')
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE,related_name='class_sessions')
    q_list = models.CharField(max_length=300)
    created_on = models.DateTimeField(auto_now=True)


class SessionAnswers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='s_ans')
    class_session = models.ForeignKey(ClassroomSession,on_delete=models.CASCADE,related_name='s_ans')
    question = models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='s_ans')
    answer = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)
    marks = models.IntegerField(default=0)
    

class JoinedUserSession(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='joined_session')
    class_session = models.ForeignKey(ClassroomSession,on_delete=models.CASCADE)
    joined_on = models.DateTimeField(auto_now=True)

# class SessionMarks(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='marks')
#     class_session = models.ForeignKey(ClassroomSession,on_delete=models.CASCADE)
#     marks = models.IntegerField()