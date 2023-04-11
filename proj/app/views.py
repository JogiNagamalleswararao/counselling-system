from django.shortcuts import render
import requests

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib.auth import authenticate, login
from django.core import serializers
import json
from django.contrib import messages
from django.contrib.auth.models import User

#--------------------------
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from datetime import datetime, time, timedelta
import pytz
#--------------------------

def splash(request):
    return render(request, 'splash.html')

def base(request):
    return render(request,'base.html')

#--------------------- LOG IN HANDLE -----------------------------
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        username=username.upper()
        password = request.POST['password']
        # print(username,password)
        # Check if user exists
        try:
            user = Login.objects.get(uid=username)
        except:
            messages.error(request, 'Username does not exist')
            return redirect('login')
        # Check if password is correct
        if user.password == password:
            # Login user
            if user.teacher==True:
                request.session['user_id'] = user.uid
                return redirect('teacher_dashboard')
                pass
            elif user.parent==True:
                request.session['user_id'] = user.uid
                return redirect('parent_dashboard')
            else:
                request.session['user_id'] = user.uid
                #return render(request,'student_d.html')
                return redirect('student_details')
        else:
            messages.error(request, 'Incorrect password')
            return redirect('login')
        
    return render(request, 'login.html')



    #     my_queryset = Login.objects.all()
    #     my_dict =  list(my_queryset.values())
    #     #print(my_dict)
    #     for x in range(len(my_queryset)):
    #         if (my_dict[x]['uid']) == username and (my_dict[x]['password']) == password:
    #             if my_dict[x]['student']==True:
    #                 my_queryset1 = Student.objects.all()
    #                 my_dict1 =  list(my_queryset1.values())
    #                 print((my_dict1[x]['uid']))
    #                 return redirect('student_details')
    #                 # messages.error(request, "student success")
                    
    #                 # here render Student deta
    #                 #return render(request, 'student_d.html')
    #                 pass
    #             elif my_dict[x]['teacher']==True:
    #                 # here render teacher deta
    #                 pass
    #             else:
    #                 # here render parent deta
    #                 pass
    #             messages.error(request, "success")
    #             return render(request, 'login.html')
    #             break
    #     messages.error(request, "sorry wrong credentials")
    # # my_json = json.dumps(my_dict)
    # # print(my_json)
    # return render(request, 'login.html')




    # my_queryset = Login.objects.all().values('uid', 'password')
    # my_json = serializers.serialize('json', my_queryset)
    #login=Login.objects.all()
    # login = serializers.serialize('json', login)
    #print(len(login))
    #return render(request, 'login.html')
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return redirect('home')
    # return render(request, 'login.html')

# def student_r(request):
#     return render(request, 'student_r.html')
#     pass
#--------------------- ------------------------ -----------------------------


#--------------------- Parent Registration -----------------------------
def parent_r(request):
    if request.method == 'POST':
        uid="P"
        uid += request.POST['uid']
        uid=uid.upper()
        my_queryset = Parent.objects.all()
        my_dict =  list(my_queryset.values())
        f=0
        for x in range(len(my_queryset)):
            if (my_dict[x]['uid']) == uid:
                f=1
                break
        if f!=1:
            email = request.POST['email']
            password = request.POST['password']
            fname = request.POST['fname']
            lname = request.POST['lname']
            image_file = request.FILES.get('image')
            mobile_num = request.POST['mobile_num']
            # address = request.POST['address']
            mentor_name = request.POST['mentor_name']
            # create a new parent object with the provided information
            parent = Parent(
                uid=uid,
                Email=email,
                password=password,
                Fname = fname,
                Lname = lname,
                mobile_num=mobile_num,
                mentor_name=mentor_name,
                image=image_file
            )
            parent.save()
            try:
                login=Login(
                    uid=uid,
                    password=password,
                    parent='True'
                )
                login.save()
            except:
                messages.error(request, "someting error")
        else:
            messages.error(request, "User alredy exit")

        return render(request, 'reg_success.html')
    #     return redirect('home')

    return render(request, 'parent_r.html')
#---------------------------------------------------------------------


#--------------------- Student Registration -----------------------------
def student_r(request):

    
    if request.method == 'POST':
        uid = request.POST['uid']
        uid=uid.upper()
        my_queryset = Student.objects.all()
        my_dict =  list(my_queryset.values())
        f=0
        for x in range(len(my_queryset)):
            if (my_dict[x]['uid']) == uid:
                f=1
                break
        if f!=1:
            email = request.POST['email']
            password = request.POST['password']
            fname = request.POST['fname']
            lname = request.POST['lname']
            branch = request.POST['branch']
            sec = request.POST['sec']
            mobile_num = request.POST['mobile_num']
            address = request.POST['address']
            mentor_name = request.POST['mentor_name']
            image_file = request.FILES.get('image')
            # create a new student object with the provided information
            student = Student(
                uid=uid,
                email=email,
                password=password,
                fname=fname,
                lname=lname,
                branch=branch,
                sec=sec,
                mobile_num=mobile_num,
                address=address,
                mentor_name=mentor_name,
                image=image_file
            )
            student.save()
            try:
                login=Login(
                    uid=uid,
                    password=password,
                    student='True'
                )
                login.save()
            except:
                pass
                # print("error")
            

            return render(request, 'reg_success.html')
        else:
            messages.error(request, "User alredy exit")


    return render(request, 'student_r.html')
#--------------------- ------------------------------ -----------------------------

#-------------------------- Teacher Registration handle ----------------------------

def teacher_r(request):
    if request.method == 'POST':
        uid = request.POST['uid']
        uid=uid.upper()
        my_queryset = Teacher.objects.all()
        my_dict =  list(my_queryset.values())
        f=0
        for x in range(len(my_queryset)):
            if (my_dict[x]['uid']) == uid:
                f=1
                break
        if f!=1:
            email = request.POST['email']
            password = request.POST['password']
            name = request.POST['name']
            dep = request.POST['dep']
            mobile_num = request.POST['mobile_num']
            image_file = request.FILES.get('image')
            des = request.POST['des']
            
            # create a new teacher object with the provided information
            teacher = Teacher(
                uid=uid,
                Email=email,
                password=password,
                name=name,
                dep=dep,
                mobile_num=mobile_num,
                image=image_file,
                des=des
            )
            instance = Teacher(image=image_file)
            instance.save()
            teacher.save()
            try:
                login=Login(
                    uid=uid,
                    password=password,
                    teacher='True'
                )
                login.save()
            except:
                pass
                # print("error")

            return render(request, 'reg_success.html')
        else:
            messages.error(request, "User alredy exit")

    return render(request, 'teacher_r.html')
#--------------------- ----------------- -----------------------------


#---------------------Log out -----------------------------
def logout(request):
    return render(request, 'base.html')
#--------------------- -------- -----------------------------


#--------------------- Student Dashboard -----------------------------
def student_details(request):
    # Get user id from session
    user_id = request.session.get('user_id')
    
    
    # Check if user is logged in
    if not user_id:
        return redirect('login')
    
    # Get user object
    try:
        user = Student.objects.get(uid=user_id)
        #print(user)
    except :
        messages.error(request, "Student.DoesNotExist")
        return redirect('login')
    
    # Get student details
    student = Student.objects.get(uid=user)
    teacher=""
    try:
        mentor=Mentor.objects.get(student_uid=user)
        teacher=Teacher.objects.get(uid=mentor.teacher_uid)
        
    except:
        pass

    context = {'student': student,
               'teacher':teacher
               }
    #print(teacher.teacher_uid)
    #student = user.uid
    #print(student)
    #adding teacher detais also to get the data from mentor table 
    
    return render(request, 'student_d.html', context)

    messages.error(request, "student success")
    # student = Student.objects.get(user=request.user)
    # return render(request, 'student_details.html', {'student': student})
#--------------------- -------------------- -----------------------------

#--------------------- Teacher Dashboard handle -----------------------------

def teacher_dashboard(request):
    # Get user id from session
    user_id = request.session.get('user_id')
    
    
    # Check if user is logged in
    if not user_id:
        return redirect('login')
    
    # Get user object
    try:
        user = Teacher.objects.get(uid=user_id)
    except Student.DoesNotExist:
        return redirect('login')
    
    # Get student details
    teacher = Teacher.objects.get(uid=user)
    print(teacher.uid)
    #student = user.uid
    
    if request.method == 'POST':
            # Get the student id entered by the teacher
        DT = request.POST.get('approvalDatetime')
        link=request.POST.get('student_link')
        meetlink = Link(uid=user_id)
        if link != None:
            meetlink.link = link
            meetlink.save()
        # print(DT)
        #print(student_uid)
    # if Mentor.objects.filter(student_uid=student_uid)!=True:
    #     messages.error(request, 'Student alredy added in your Dashboard')
        try:
                # Get the student object
            student_uid = request.POST.get('student_uid')
            student_uid=student_uid.upper()
            student = Student.objects.get(uid=student_uid)
            try:
                if (Mentor.objects.get(student_uid=student_uid).student_uid)==student_uid:
                    messages.error(request, 'Student with that ID exist in others or your dashboard')

            except:
                count = Mentor.objects.filter(teacher_uid=teacher).count()
                # print(count)
                if count < 5:
                        # Add the student to the teacher's list of students
                    mentor=Mentor(teacher_uid=teacher.uid,student_uid=student.uid)
                    mentor.save()
                    # print(mentor)    
                    messages.success(request, f'{student.fname} {student.lname} has been added to your list of students.')
                else:
                    messages.error(request, 'You have already added the maximum number of students allowed.')
            
        except Student.DoesNotExist:
            messages.error(request, 'Student with that ID does not exist.')
        
    
    student_ids=[]
    student_uids = Mentor.objects.filter(teacher_uid=user)
    my_dict =  list(student_uids.values())
    for x in range(len(my_dict)):
        # print(my_dict[x]['student_uid'])
        student_ids.append(my_dict[x]['student_uid'])
    
    mentors = Student.objects.filter(uid__in=student_ids)
    parent_requests=ParentRequest.objects.filter(teacher=user)

    # requset_parent=[]
    # requset_teacher = ParentRequest.objects.filter(teacher=user)
    # my_dict =  list(requset_teacher.values())
    # for x in range(len(my_dict)):
        
    #     requset_parent.append(my_dict[x]['parent'][1:])
    # student_r = Student.objects.filter(uid__in=student_ids)
    # requset_parent=[]
    # for x in range(len(my_dict)):
    #     print(my_dict[x]['parent'])
    #     requset_parent.append(my_dict[x]['parent'])
    # parent_r = Parent.objects.filter(uid__in=requset_parent)


    
    #----sinngle recode ----teacher1 = Mentor.objects.get(teacher_uid=user)

    
        
    context = {
            'teacher': teacher,
            'mentors': mentors,
            'parent_requests':parent_requests,    
            # 'student_r':student_r,
            # 'parent_r':parent_r,

    }
        
    return render(request, 'teacher_d.html', context)


    # #adding teacher detais also to get the data from mentor table 
    # context = {'teacher': teacher}
    # return render(request, 'teacher_d.html', context)
    # user_id = request.session.get('user_id')
    # pass
#--------------------------------------------------------------------------------

#---------------- parent Dashboard handle ---------------------------------
def parent_dashboard(request):
    user_id = request.session.get('user_id')
    # print(user_id[1:])
    parent = Parent.objects.get(uid =user_id )
    student = Student.objects.get(uid=user_id[1:])
    mentor = Mentor.objects.get(student_uid=user_id[1:])
    # print(student)
    #/////////////////////////////
    teacher=Teacher.objects.get(uid=mentor.teacher_uid)
    # parent_request=ParentRequest(parent=parent,teacher=teacher.uid,student=student)
    # if request.method == 'POST':
    #     #reason = request.POST['reason']
    #     parent_request.message = request.POST.get('reason')
    #     parent_request.save()   
    # ///////////////////////      
    # tuition_fee = TuitionFee.objects.get(student=student)
    context = {
         'parent': parent,
         'student': student,
         'mentor': teacher,
    #     'tuition_fee': tuition_fee,
    }
    return render(request, 'parent_d.html',context)
#--------------------------------------------------------------------------------

#----------- Teacher approvel the parent request ------------------------------
def approve_request(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        parent_email = request.POST.get('parent_email')
        message = request.POST.get('message')
        teacher = request.POST.get('teacher') 
        parent_phno=request.POST.get('parent_phone')
        print(parent_phno)
        if request.method == 'POST':
            selected_date = request.POST.get('selected_date')
            selected_time = request.POST.get('selected_time')
            parent_email = request.POST.get('parent_email')
            teacher = request.POST.get('teacher')
            parent_ph=request.POST.get('parent_phno')
            
            # link1=Link.objects.get(uid=teacher)
            # teacher_links = Link.objects.filter(uid=teacher)
            # links = Link.objects.all()
            # print(teacher_links)
            # print(teacher_links)
            # link=Link.objects.g
           
        if selected_date != None and selected_time != None and parent_ph!=None:
            my_queryset = Link.objects.filter(uid=teacher)
            my_dict =  list(my_queryset.values())
            
            print(my_dict[0]['link'])
            print(parent_email)
            try:
                teacher=Teacher.objects.get(uid=teacher)
            except:
                pass
            # ------------------------ google calender -----------------------
            # # Replace with your own values
            # event_start = datetime(int(selected_date[0:4]),int(selected_date[5:7]),int(selected_date[8:10]), int(selected_time[0:2]),int(selected_time[3:5]), tzinfo=pytz.UTC)
            # timezone = 'UTC'
            # event_summary = 'New Event'
            # event_location = 'Online'

            # # Get credentials
            # import os
            # import json
            
            # # Get the path to the credentials file
            # dirname = os.path.dirname(__file__)
            # creds_filename = os.path.join(dirname,  'credentials.json')

            # # Load the credentials from the file
            # with open(creds_filename, 'r') as creds_file:
            #     creds_data = json.load(creds_file)

            # # Create the flow
            # flow = InstalledAppFlow.from_client_config(creds_data, ['https://www.googleapis.com/auth/calendar'])

            # creds = flow.run_local_server(port=0)
            # service = build('calendar', 'v3', credentials=creds)
            # # creds = None
            # # if creds is None or not creds.valid:
            # #     flow = InstalledAppFlow.from_client_secrets_file(
            # #         './credentials.json', ['https://www.googleapis.com/auth/calendar'])
            # #     creds = flow.run_local_server(port=0)
            # # service = build('calendar', 'v3', credentials=creds)

            # # Create event with Meet link
            # event = {
            #     'summary': event_summary,
            #     'location': event_location,
            #     'start': {
            #         'dateTime': event_start.isoformat(),
            #         'timeZone': timezone,
            #     },
            #     'end': {
            #         'dateTime': (event_start + timedelta(hours=1)).isoformat(),
            #         'timeZone': timezone,
            #     },
            #     'conferenceData': {
            #         'createRequest': {
            #             'requestId': '1234567890',
            #             'conferenceSolutionKey': {
            #                 'type': 'hangoutsMeet',
            #             },
            #         },
            #     },
            # }

            # try:
            #     event = service.events().insert(calendarId='primary', conferenceDataVersion=1,
            #                                     body=event, sendNotifications=True).execute()
            #     meet_link = event['hangoutLink']
            #     print('Meet Link:', meet_link)
            # except HttpError as error:
            #     print(f'An error occurred: {error}')
            
            #///////////////////////////////////////////
            import smtplib
            from email.mime.text import MIMEText

            # Email account details
            my_email = "sriramhota22@gmail.com"
            my_password = "jfhbsuoojvwpqmfe"

            # Recipient email address
            recipient_email = parent_email

            # Link to include in message body
            # link = "https://www.example.com"

            # Create message object
            
            message = MIMEText(f"\n\nDear Parents/Guardians, \n \n \nI hope this email finds you and your family well.I am writing this email to inform you that I will be conducting an online meeting through Google Meet on {selected_date} at {selected_time} for discussing your child's progress and any other concerns that you may have. Attached to this email, you will find a link to join the meeting.\n\n          MEETLINK: {my_dict[0]['link']}\n\nPlease ensure that you have a stable internet connection and a device with a camera and microphone for a smooth online experience. I look forward to meeting you all virtually and discussing your child's progress.\n\nIf you have any queries or concerns, please do not hesitate to reach out to me. \n\nThank you,\n\nBest regards,\n\n{teacher.name},\n{teacher.des},\nVishnu Institute of Technology ")

            message['From'] = my_email
            message['To'] = recipient_email
            message['Subject'] = "Meeting Request Follow-up"

            # Connect to SMTP server and send message
            smtp_session = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_session.starttls()
            smtp_session.login(my_email, my_password)
            smtp_session.sendmail(my_email, recipient_email, message.as_string())

            smtp_session.quit()


            #------------- 1st sms -----------------------------------------
            
            url= 'https://www.fast2sms.com/dev/bulkV2'
            message="Meeting has been scheduled on your request, please attend it"
            # message="Dear Parents/Guardians,\nwe are conceder your request, please join Google Meet on {selected_date} at {selected_time},\n MEETLINK: {my_dict[0]['link']}"
            number=parent_ph
            payload=f'sender_id=FTWSMS&message={message}&route=v3&language=english&numbers={number}'

            headers={
                 'authorization' : 'WDSuUazkHBi3hYgvqAtPCdRIxO6fsQloj9yZ5L8FXnbe2NJ4VMrWYSxUym5d6GM3oPtE2blsXpqnV4w0',
                 'Content-Type':'application/x-www-form-urlencoded'
             }
            response = requests.request("POST",url=url,data=payload,headers=headers)
            print(response.text)


            #------------- 2nd sms ------------------
            url= 'https://www.fast2sms.com/dev/bulkV2'
            message=f"Meet Link:{my_dict[0]['link']}, Date:{selected_date}, Time:{selected_time},"
            # message="Dear Parents/Guardians,\nwe are conceder your request, please join Google Meet on {selected_date} at {selected_time},\n MEETLINK: {my_dict[0]['link']}"
            number=parent_ph
            payload=f'sender_id=FTWSMS&message={message}&route=v3&language=english&numbers={number}'

            headers={
                 'authorization' : 'WDSuUazkHBi3hYgvqAtPCdRIxO6fsQloj9yZ5L8FXnbe2NJ4VMrWYSxUym5d6GM3oPtE2blsXpqnV4w0',
                 'Content-Type':'application/x-www-form-urlencoded'
             }
            response = requests.request("POST",url=url,data=payload,headers=headers)
            print(response.text)
            #///////////////////////////////////////////
            #----------------------------------------------------------------------
            context={
                'parent_email':parent_email
            }
                # -----------------------------------------------------
            return render(request,'success_sent_link.html',context)


        #print(selected_date[0:4],selected_date[5:7],selected_date[8:10],selected_time[0:2],selected_time[3:5])
            # Do something with the selected date, time, and student name
        context = {
            'parent_email': parent_email,
            'teacher':teacher,
            'parent_phno':parent_phno,
        #     'tuition_fee': tuition_fee,
        }
    # print("hi",teacher)
    
    return render(request, 'approve_request.html',context)
#--------------------------------------------------------------------------------

#----------- Teacher remove the parent request ----------------
def success_remove(request):
    if request.method == 'POST':
        remove = request.POST.get('Remove')
        parent_request = ParentRequest.objects.get(student=remove)
        parent_request.delete()
        print(remove)
    return render(request, 'success_remove.html')
#------------------------------------------------------------------

#----------- parent request sent to database handle ----------------
def success_sent(request):
    user_id = request.session.get('user_id')
    parent = Parent.objects.get(uid =user_id )
    student = Student.objects.get(uid=user_id[1:])
    mentor = Mentor.objects.get(student_uid=user_id[1:])
    print(student)
    teacher=Teacher.objects.get(uid=mentor.teacher_uid)
    parent_request=ParentRequest(parent=parent,teacher=teacher.uid,student=student)
    if request.method == 'POST':
        #reason = request.POST['reason']
        parent_request.message = request.POST.get('reason')
        parent_request.save() 
    return render(request, 'success_sent.html')
#-----------------------------------------------------------------------
