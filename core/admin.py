from django.contrib import admin
from .models import (Classroom, ClassPeople, Questions, MultipleChoiceQuestions, Answers, 
MultipleChoiceAnswer,ClassroomSession, JoinedUserSession, SessionAnswers)
# Register your models here.

admin.site.register(Classroom)
admin.site.register(ClassPeople)
admin.site.register(Questions)
admin.site.register(Answers)
admin.site.register(MultipleChoiceQuestions)
admin.site.register(MultipleChoiceAnswer)
admin.site.register(ClassroomSession)
admin.site.register(JoinedUserSession)
admin.site.register(SessionAnswers)
