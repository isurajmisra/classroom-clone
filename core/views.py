from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .forms import UserRegistrationForm, CreateClass
from django.core.mail import send_mail
from .utils import randomword
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate,login
from collections import Counter
from django.db.models import Sum, Avg, Count
import json
from core.forms import CreateClass

# Create your views here.

def home_view(request):
    if request.user.is_authenticated:
        user = request.user
        classrooms = user.classrooms.all
        joined_class = ClassPeople.objects.filter(user=user)
        form = CreateClass()
        context = {
            'classrooms' : classrooms,
            'joined_class': joined_class,
            'form':form,
    
        }
        return render(request,'core/home.html',context)
    else:
        return redirect("login")


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account created successfully!!")
            return redirect('login')

    else:
        form = UserRegistrationForm()
    return render(request,'core/register.html',{'form':form})

def profile(request):
    sessions = request.user.joined_session.all()
    context={
        'sessions':sessions,
    }
    return render(request,'core/profile.html',context)

def create_class(request):
    if request.method == 'POST':
        form = CreateClass(request.POST)
        code = randomword(6)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.user = request.user
            classroom.c_code = code
            classroom.save()
            messages.success(request,"Class created successfully!!")
            return redirect("classroom",pk=classroom.pk) 
        else:
            messages.error(request,"There is some problem with your form!!")
            return redirect("home") 
        
    
    


def classroom(request,pk):
    classroom = get_object_or_404(Classroom,pk=pk)
    people =User.objects.filter(classpeople__classroom=classroom)
    teacher = User.objects.get(id=classroom.user.pk)
    questions = Questions.objects.filter(classroom=classroom)
    sessions = ClassroomSession.objects.filter(user=request.user,classroom=classroom)
    all_sessions = ClassroomSession.objects.filter(classroom=classroom)
    context = {
        'classroom':classroom,
        'people':people,
        'teacher':teacher,
        'questions':questions,
        'sessions':sessions,
        'all_sessions':all_sessions,
  
    }
    return render(request,'core/classroom.html',context)

def invite_people(request,pk):
    if request.method == 'POST':
        email = request.POST['email']
        classroom = get_object_or_404(Classroom,pk=pk)
        code = classroom.c_code
        message = f'''Hello Suraj sent you a code to join the classroom.
        link : http://127.0.0.1:8000/join_class/{pk}/{code}'''
        send_to = [email,]
        send_mail("Join Classroom",message,'surajmishra7777@gmail.com',send_to,fail_silently=False)
        messages.success(request,"Invitation sent successfully!!")
    else:
        messages.error(request,"Email is not sent properly. Please try again.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def join_class(request,pk,code):
    if request.user.is_authenticated:
        user = request.user
        classroom = get_object_or_404(Classroom,pk=pk)
        if is_already_joined(user,classroom)==True:
            messages.info(request,"You have already joined this class.")
            return redirect("classroom",pk=pk)
        else:
            if classroom.c_code == code:
                obj = ClassPeople.objects.create(user=user,classroom=classroom)
                obj.save()
                messages.success(request,"Class Joined successfully!!")
                return redirect('classroom',pk=pk)
            else:
                messages.error(request,"Please check the join code.")
                return redirect("home")
    
    else:
        messages.info(request,"Please login first.")
        return redirect("login")

def is_already_joined(user,classroom):
    print(user.id)
    print(classroom.id)
    if ClassPeople.objects.filter(classroom=classroom,user=user).count()==1:
        return True
    else:
        return False

def create_question(request,pk):
    if request.method == "POST":
        classroom = get_object_or_404(Classroom,pk=pk)
        question = request.POST['question']
        answer = request.POST['answer']
        if request.POST['mcq']=="Multiple choice":
            q_type = "Multiple choice"
            obj = Questions.objects.create(user=request.user,classroom=classroom,text=question,answer=answer,q_type=q_type)
            obj.save()
            count = int(request.POST['count'])
            for i in range(1,count+1):
                mcq = MultipleChoiceQuestions.objects.create(question=obj)
                option = request.POST[f'{i}']
                print(option)
                mcq.option=option
                mcq.answer = answer
                mcq.save()
 
        else:
            q_type = "Short answer"
            obj = Questions.objects.create(user=request.user,text=question,answer=answer,q_type=q_type)
            obj.save()

    messages.success(request,"Question posted successfully.")
    return redirect('classroom',pk=pk)

def question_details(request,pk):
    ques = get_object_or_404(Questions,pk=pk)
  
    context = {
        'question':ques,
        
    }
    return render(request,'core/question-details.html',context)

def answer_short(request,pk):
    if request.method=="POST":
        question = get_object_or_404(Questions,pk=pk)
        text = request.POST["answer"]
        if question.answer == text:
            is_correct= True
        else:
            is_correct = False
        ans = Answers.objects.create(user=request.user,question=question,text=text,is_correct=is_correct)
        ans.save()
        messages.success(request,"Answer submitted.")
        return redirect("question-details",pk=pk)

def answer_mcq(request,pk):
    if request.method=="POST":
        option = request.POST['group1']
        question = get_object_or_404(Questions,pk=pk)
        if question.answer == option:
            is_correct = True
        else:
            is_correct = False
        ans_mcq = MultipleChoiceAnswer(user=request.user,question=question,option=option,is_correct=is_correct)
        ans_mcq.save()
        messages.success(request,"Answer submitted.")
        return redirect("question-details",pk=pk)

def is_already_answered_mcq(request,pk):
    question = get_object_or_404(Questions,pk=pk)
    if MultipleChoiceAnswer.objects.filter(user=request.user,question=question).count()==1:
        return True
    else:
        return False

def is_already_answered_short(request,pk):
    question = get_object_or_404(Questions,pk=pk)
    if Answers.objects.filter(user=request.user,question=question).count()==1:
        return True
    else:
        return False

def create_session(request,pk):
    if request.method == "POST":
        q_list = request.POST.getlist('checkboxlist')
        classroom = get_object_or_404(Classroom,pk=pk)
        session = ClassroomSession.objects.create(user=request.user,classroom=classroom,q_list=json.dumps(q_list) )
        session.save()
        return redirect("session",pk=session.pk)

    else:
        classroom = get_object_or_404(Classroom,pk=pk)
        questions = classroom.questions.all
        context={
            'classroom':classroom,
            'questions':questions,
        }
        return render(request,'core/create-session.html',context)

def class_session(request,pk):
    if request.user.is_authenticated:
        class_session = get_object_or_404(ClassroomSession,pk=pk)
        marks = students_marks(pk)
        students = session_joined(request,pk)
        jsonDec = json.decoder.JSONDecoder()
        q_list = jsonDec.decode(class_session.q_list)
        print(q_list)
        question_short = []
        question_mcq=[]
        answers = SessionAnswers.objects.filter(class_session=class_session)
        s_answers = student_ans(request,pk)
        for id in q_list:
            obj = get_object_or_404(Questions,pk=int(id))
            if obj.q_type == "Short answer":
                question_short.append(obj)
            else:
                question_mcq.append(obj)
        stats_c = session_answer_correct(pk)
        stats_ic = session_answer_incorrect(pk)
        ans_data = get_answer(pk)
        user_ans = SessionAnswers.objects.filter(user=request.user,class_session=class_session)
        toppers = top_students(pk)
        lasts = last_students(pk)
        hard_ques = hard_questions(pk)
        joined_user_count = get_total_joined_user(pk)
        correct_answers = get_correct_answer_count(pk)
        ca_len = len(correct_answers)
        context = {
            'q_short':question_short,
            'q_mcq':question_mcq,
            'class_session':class_session,
            'total_question_count':len(q_list),
            'students':students,
            'answers':answers,
            's_answers':s_answers,
            'stats_c':stats_c,
            'stats_ic':stats_ic,
            'marks':marks,
            'q_list':q_list,
            'ans_data':ans_data,
            'user_ans':user_ans,
            'toppers':toppers,
            'lasts':lasts,
            'hard_ques':hard_ques,
            'joined_user_count':joined_user_count,
            'correct_answers':correct_answers,
        }
        return render(request,'core/session.html',context)
    else:
        messages.info(request,"You need to login first.")
        return redirect("login")

def session_joined(request,pk):
    session = get_object_or_404(ClassroomSession,pk=pk)
    students = JoinedUserSession.objects.filter(class_session=session)
    if request.user.pk == session.user.pk:
        return students
    else:
        if JoinedUserSession.objects.filter(user=request.user,class_session=session).count()==0:
            js = JoinedUserSession.objects.create(user=request.user,class_session=session)
            js.save()
            students = JoinedUserSession.objects.filter(class_session=session)
            return students
        else:
            return students
    
def session_answers(request,pk,qk):
    if request.method == 'POST':
        session = get_object_or_404(ClassroomSession,pk=pk)
        question = get_object_or_404(Questions,pk=qk)
        if question.q_type == "Short answer":
            answer=request.POST['answer']
        else:
            answer = request.POST['group1']
        if answer == question.answer:
            is_correct = True
            marks = 50
        else:
            marks = 0
            is_correct = False
        sa = SessionAnswers.objects.create(user = request.user, class_session = session, question=question,answer=answer,marks=marks,is_correct=is_correct)
        sa.save()
        messages.success(request,"Answer submitted.")
        return redirect("session",pk=pk)
    


def is_already_answered(request,sk,qk):
    session = get_object_or_404(ClassroomSession,pk=sk)
    question = get_object_or_404(Questions,pk=qk)
    if SessionAnswers.objects.filter(user=request.user,class_session=session,question=question).count()>=1:
        return True
    else:
        return False

def error_404(request, exception):

    return render(request,'error/404.html',{})

def error_500(request):
    return render(request,'error/500.html',{})

def session_answer_correct(pk):
    session = get_object_or_404(ClassroomSession,pk=pk)
    correct = SessionAnswers.objects.select_related('question').filter(class_session=session,is_correct=True)
    data_c = []
    for ques in correct:
        data_c.append(ques.question.text)
    data_cd = Counter(data_c)
    data_c = {}
    for k,v in data_cd.items():
        data_c[k] = f"{v}"
    print(data_c)
    return data_c


def session_answer_incorrect(pk):
    session = get_object_or_404(ClassroomSession,pk=pk)
    incorrect = SessionAnswers.objects.select_related('question').filter(class_session=session,is_correct=False)
    
    data_ic = []
    for ques in incorrect:
        data_ic.append(ques.question.text)
    data_icd = Counter(data_ic)
    data_ic = {}
    for k,v in data_icd.items():
        data_ic[k] = f"{v}"
    print(data_ic)
    return data_ic

def student_ans(request,pk):
    session = get_object_or_404(ClassroomSession,pk=pk)
    stu = SessionAnswers.objects.filter(user=request.user,class_session=session)
    data={}
    for obj in stu:
        data[obj.question.text]=obj.answer

    print(data)
    return data

def students_marks(pk):
    session = get_object_or_404(ClassroomSession,pk=pk)
    students = SessionAnswers.objects.filter(class_session=session)
    students_join = JoinedUserSession.objects.filter(class_session=session)

    marksd = {} 
    for u in students: 
        marks = 0 
        if u.user in marksd: 
            marksd[u.user]+=u.marks 
        else: 
            marksd[u.user]=u.marks 
    for stu in students_join:
        if stu.user not in marksd:
            marksd[stu.user] = 0

    
    print(marksd)

    return marksd

def get_answer(pk):
    session = get_object_or_404(ClassroomSession,pk=pk)
    jsonDec = json.decoder.JSONDecoder()
    q_list = jsonDec.decode(session.q_list)
    data = {}
    students_ans = SessionAnswers.objects.filter(class_session=session).order_by('question')
    for stu in students_ans: 
        if stu.user.username not in data:
            value = {}
            value[stu.question.pk] = stu.is_correct
            data[stu.user.username]=value
        
        else:
            value = data[stu.user.username]
            value[stu.question.pk] = stu.is_correct
            data[stu.user.username]=value

    for key, value in data.items():
        for q in q_list:
            if int(q) not in value:
                value[int(q)] = None
            
            
    for k,v in data.items():
        v =  dict(sorted(v.items()))
        data[k]= v
    students = JoinedUserSession.objects.filter(class_session=session)
    for stu in students:
        if stu.user.username not in data:
            ls = {}
            for q in q_list:
                ls[int(q)]=None 
            ls['total']= 0
            data[stu.user.username]=ls

    total_correct_ans = User.objects.filter(s_ans__is_correct=True,s_ans__class_session=session).annotate(count=Count('s_ans__user'))   
    
    for stu in total_correct_ans:
        if stu.username in data:
            data[stu.username]['total']=stu.count
    for k,v in data.items():
        try:
            if v['total']:
                pass
        except:
            v['total'] = 0


                
    print(data)
    return data


    

def top_students(pk):
    session = get_object_or_404(ClassroomSession,pk=pk)
    if User.objects.filter(s_ans__class_session=session).annotate(sum=Sum('s_ans__marks')).order_by('-sum').count()>3:
        toppers= User.objects.filter(s_ans__class_session=session).annotate(sum=Sum('s_ans__marks')).order_by('-sum')[:3]  
        return toppers  
    else:
        return 
def last_students(pk):
    session = get_object_or_404(ClassroomSession,pk=pk)
    if User.objects.filter(s_ans__class_session=session).annotate(sum=Sum('s_ans__marks')).order_by('sum').count()>5:
        lasts= User.objects.filter(s_ans__class_session=session).annotate(sum=Sum('s_ans__marks')).order_by('sum')[:3]  
        return lasts
    else:
        return 

def hard_questions(pk):
    session = get_object_or_404(ClassroomSession,pk=pk)
    # if Questions.objects.filter(s_ans__is_correct = False,s_ans__class_session = session).annotate(count=Count('s_ans__question')).order_by('-count').count()>3:
    hard_ques = Questions.objects.filter(s_ans__is_correct = False,s_ans__class_session = session).annotate(count=Count('s_ans__question')).order_by('-count')[:3]
    return hard_ques

def get_total_joined_user(pk):
    session = get_object_or_404(ClassroomSession,pk=pk)
    joined_user_count = JoinedUserSession.objects.filter(class_session=session).count()
    print(joined_user_count)
    return joined_user_count

def get_correct_answer_count(pk):
    session = get_object_or_404(ClassroomSession,pk=pk)
    jsonDec = json.decoder.JSONDecoder()
    q_list = jsonDec.decode(session.q_list)
    correct_answers = Questions.objects.filter(s_ans__is_correct = True,s_ans__class_session = session).annotate(count=Count('s_ans__question')).order_by('s_ans__question')
    data = {}
    for ans in correct_answers:
        data[ans.pk] = ans.count
    for q in q_list:
        if int(q) not in data:
            data[int(q)]=0

    data = dict(sorted(data.items()))
    print(data)
    return data
