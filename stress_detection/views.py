from django.http import HttpResponse
from django.shortcuts import render ,get_object_or_404
from django.shortcuts import redirect
from  django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import *
import pycurl
from urllib.parse import urlencode
#from ML import emotions_detection
from ML import test1
from ML import voice2
#from ML.emotion_text import emotion_text

from keras import backend as K

def sends_mail(mail,msg):

	crl = pycurl.Curl()
	crl.setopt(crl.URL, 'https://alc-training.in/gateway.php')
	data = {'email': mail,'msg':msg}
	pf = urlencode(data)

	# Sets request method to POST,
	# Content-Type header to application/x-www-form-urlencoded
	# and data to send in request body.
	crl.setopt(crl.POSTFIELDS, pf)
	crl.perform()
	crl.close()

def first(request):
    return render(request,'index.html')



def index(request):
    return render(request,'index.html')
    
    
def reg(request):
    return render(request,'register.html')
    
    



def addreg(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')


        if register.objects.filter(email=email).exists():
            return render(request, 'register.html', {'status': 'Email already exists. Registration failed.'})
        else:
            user = register(name=name, email=email, phone=phone, password=password,status='pending')
            user.save()
            return render(request, 'register.html', {'status': 'Registration successful.'})

    return render(request, 'register.html')     

def aproveuser(request,id):
    user = get_object_or_404(register, id=id)
    user.status='approved'
    user.save()
    sel=register.objects.all()
    return render(request,'admin/user.html',{'res':sel})
 
def rejectuserrr(request,id):
    user = get_object_or_404(register, id=id)
    user.status='rejected'
    user.save()
    sel=register.objects.all()
    return render(request,'admin/user.html',{'res':sel})    

def faq(request): 
    return render(request, 'faq.html')  
        
def logint(request):
    email = request. POST.get('email')
    password=request. POST.get('password')
    if email == 'admin@gmail.com' and password == 'admin':
        request.session['logintdetail'] = email
        request.session['logint'] = 'admin'
        return render(request, 'admin/index.html',{'status': 'LOGIN SUCCESSFULLY'})

    elif register.objects.filter(email=email,password=password,status='approved').exists():
        userdetails=register.objects.get(email=request.POST['email'], password=password)
        if userdetails.password == request.POST['password']:
            request.session['uid'] = userdetails.id
            request.session['sname'] = userdetails.name

            request.session['semail'] = email

            request.session['user'] = 'user'
            password = request.POST.get('password')

            
            return render(request,'index.html',{'status': 'LOGIN SUCCESSFULLY'})  
    
    elif doctor.objects.filter(email=email,password=password).exists():
        userdetails=doctor.objects.get(email=request.POST['email'], password=password)
        if userdetails.password == request.POST['password']:
            request.session['did'] = userdetails.id
            request.session['tname'] = userdetails.name

            request.session['temail'] = email

            request.session['doctor'] = 'doctor'


            return render(request,'index.html',{'status': 'LOGIN SUCCESSFULLY'})            


            
    
    else:
        return render(request, 'login.html', {'status': 'INVALID USERID OR PASSWORD'})   


def login(request):
    return render(request,'login.html')
    
def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect(first) 
    
def forget(request):
    return render(request,'forgetpass.html') 

def forgetpassword(request):
    if request.method == "POST":
        entered_email = request.POST.get('email')

        # Check if the entered email exists in the regtable (User model)
        try:
            user = register.objects.get(email=entered_email)
            password = user.password  # Retrieve the password from the User model

            # Send the password to the user's email using the sends_mail function
            message = f'Your password For login is: {password}'
         
            sends_mail(entered_email, message)

            return render(request, 'login.html', {'msg': 'Your password has been sent to the registered email.'})

        except register.DoesNotExist:
            return render(request, 'login.html', {'msg': 'Entered email does not exist .'})

    return render(request, 'login.html', {'msg': 'Enter your registered email to recover your password.'})     
   
    
def addremedys(request):
    if request.method == 'POST':
        emotion=request.POST.get('emotion')
        disease=request.POST.get('disease')
        user=remedy(emotion=emotion,disease=disease)    
        user.save()
    return render(request,'admin/addremedy.html')    



def rem(request):
    return render(request,'admin/addremedy.html')

def addmusic(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        emotion=request.POST.get('emotion')
        if emotion in ['happy','surprise']:
            stress="low"
        elif emotion in ['sad','fear','neutral']:
            stress="medium"
        else:
            stress="high"
        myfile=request.FILES['music']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name,myfile)
        myfile1=request.FILES['video']
        fs1 = FileSystemStorage()
        filename1 = fs1.save(myfile1.name,myfile1)
        user=remedy(name=name,emotion=emotion,music=filename,video=filename1,stress_level=stress)    
        user.save()
    return render(request,'admin/addmusic.html')


def addvideo(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        emotion=request.POST.get('emotion')
        if emotion in ['happy','surprise']:
            stress="low"
        elif emotion in ['sad','fear','neutral']:
            stress="medium"
        else:
            stress="high"
        myfile=request.FILES['video']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name,myfile)
        user=remedy(name=name,emotion=emotion,music=filename,stress_level=stress)    
        user.save()
    return render(request,'admin/addvideo.html')        
    
def viewstress(request):
    sel=remedy.objects.all()
    return render(request,'admin/viewremdey.html',{'res':sel})
    
def userview(request):
     sel=register.objects.all()
     return render(request,'admin/user.html',{'res':sel})

def viewresults(request):
    sel=upload.objects.all()
    sel2=result_tbl.objects.all()
    return render(request,'viewresults.html',{'res':sel,'res2':sel2})
     
def dash(request):
    return render(request,'admin/index.html')
    
''''def addup(request,id):

    sel=remedy.objects.get(pk=id)
          
    sel.save()
        return redirect(viewstress)
    return render(request,'admin/update.html',{'res':sel})'''

def update(request,id):
        request.session['emotion_id']=id
        return render(request,'admin/update.html')
        
        
def addup(request):
    if request.method == "POST":
            #print("hi")
            disease=request.POST.get('disease')
            sel=remedy.objects.get(id=request.session['emotion_id'])
            sel.disease=disease
            sel.save()
            return redirect(viewstress)
    return render(request,'admin/update.html')  


'''def livevoice(request):
    stud=request.session['sname']
    K.clear_session()
    emotion,stress_level=test1.predict()
    K.clear_session()
    print("the predicted stress level is:",stress_level)
    user=remedy.objects.filter(emotion=emotion)
  
    ins=result_tbl(user=stud,uid= request.session['uid'] ,emotion=emotion,stress=stress_level,mode='Voice')    
    ins.save()
    return render(request,'viewremedies.html',{'res':user,'emtn':emotion,'strs':stress_level})'''   

'''  message=f'Stress is high for the Student : {stud}'
    if(stress_level=="high"):
        sends_mail("archanaanil529@gmail.com", message)'''



def livevoice(request):
    stud=request.session['sname']
    K.clear_session()
    stress_level, text = voice2.livevoice()
    K.clear_session()
    #print("the predicted stress level is:",stress_level)
    #user=remedy.objects.filter(emotion=emotion)
  
    ins=result_tbl(user=stud,uid= request.session['uid'] ,emotion = text, stress=stress_level, mode='Voice')    
    ins.save()
    return render(request,'index.html',{'res':stress_level})


def startwebcam(request):
    stud=request.session['sname']
    K.clear_session()
    emotion,stress_level=emotions_detection.predict()
    K.clear_session()
    #print("the prefdicted emotion is:",emotion)
    print("the predicted stress level is:",stress_level)
    message=f'Stress is high for the Student : {stud}'
    if(stress_level=="high"):
        sends_mail("archanaanil529@gmail.com", message)
    #user1=remedy(stress_level=stress_level)
    #user1.save()
    user=remedy.objects.filter(emotion=emotion)
   
    ins=result_tbl(user=stud,uid= request.session['uid'] ,emotion=emotion,stress=stress_level,mode='Live')    
    ins.save()
    return render(request,'viewremedies.html',{'res':user,'emtn':emotion,'strs':stress_level})   



def viewremedies(request):
    sel=result_tbl.objects.filter(uid=request.session['uid'])
    return render(request,'viewremedies.html',{'resul':sel})

#def text_emotion(request):
    '''if request.method=="POST":
        text_data=request.POST.get('text_data')
        K.clear_session()
        emotion,stress_level=emotion_text.predict(text_data)
        K.clear_session()
        print("the prefdicted emotion is:",emotion)
        print("the predicted stress level is:",stress_level)
        user=remedy.objects.filter(emotion=emotion)
        return render(request,'viewremedies.html',{'res':user})
    return render(request,'text_emotion.html')
    if request.method=="POST":
        text_data=request.POST.get('text_data')
        K.clear_session()
        emotion=emotion_text.predict(text_data)
        K.clear_session()
        print("the prefdicted emotion is:",emotion)
        user=remedy.objects.filter(emotion=emotion)
        return render(request,'viewremedies.html',{'res':user})
    return render(request,'text_emotion.html')'''



def viewuser(request):
    upd=remedy.objects.all()
    return render(request,'viewremedies.html',{'res':upd})
def adddoctor(request):
    return render(request,'admin/adddoctor.html',{'status': 'SUCCESSFULLY ADDED'})   
def viewuserdoctor(request):
    sel=doctor.objects.all()
    return render(request,'viewuserdoctor.html',{'result':sel})
def consult1(request,id):
    sel=doctor.objects.get(id=id)
    return render(request,'consult.html',{'result':sel})    
def addconsult(request):
    if request.method=="POST":
        des=request.POST.get('des')
        date=request.POST.get('date')
        did=request.POST.get('did')
        medicine=request.POST.get('medicine')
        uid=request.session['uid']
        file = request.FILES['file']
        fs = FileSystemStorage()
        file = fs.save(file.name,file)
        

        donor=consult(did=did,uid=uid,date=date,des=des,file=file,medicine=medicine,status='pending')
        donor.save()
        return redirect(viewuserdoctor)    
def userprescribe(request):
    sel=consult.objects.filter(uid=request.session['uid'],status='consult')
    sel1=doctor.objects.all()
    for i in sel:
        for j in sel1:
            if str(i.did)==str(j.id):
                i.did=j.name
    return render(request,'userprescribe.html',{'result':sel})        
def viewuserconsult(request):
    sel=consult.objects.filter(did=request.session['did'],status='pending')
    sel1=register.objects.all()
    for i in sel:
        for j in sel1:
            if str(i.uid)==str(j.id):
                i.uid=j.name
    return render(request,'vieww.html',{'result':sel})    
def dtt(request,id):
    sel=consult.objects.get(id=id)
    return render(request,'dc.html',{'result':sel})
def dconsult(request):
    if request.method == "POST":
        cid = request.POST.get('cid')
        prescription = request.POST.get('prescription')
        a = consult.objects.get(id=cid)
        did = a.did
        uid = a.uid
        des = a.des
        date = a.date
        file = a.file
        medicine = a.medicine

       
       

        idd = a.id

        donor1 = consult(did=did, file=file, uid=uid, des=des, date=date, medicine=medicine, prescription=prescription, status='consult', id=idd)
        donor1.save()
    return redirect(viewuserconsult)  
def addd(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        password=request.POST.get('password')
        age=request.POST.get('age')
        specialization=request.POST.get('specialization')
        experience=request.POST.get('experience')

        donor=doctor(specialization=specialization,experience=experience,name=name,email=email,phone=phone,address=address,password=password,age=age)
        donor.save()
        return render(request,'adddoctor.html',{'status':' Successfully Added'})


from django.shortcuts import render

def data_submit(request):
    if request.method == "POST":
        q1 = int(request.POST.get('a', 0))
        q2 = int(request.POST.get('b', 0))
        q3 = int(request.POST.get('c', 0))
        q4 = int(request.POST.get('d', 0))
        q5 = int(request.POST.get('e', 0))
        q6 = int(request.POST.get('f', 0))
        q7 = int(request.POST.get('g', 0))
        q8 = int(request.POST.get('h', 0))
        q9 = int(request.POST.get('i', 0))
        q10 = int(request.POST.get('j', 0))

        total_score = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9 + q10

        stress_level = ""
        if total_score <= 2:
            stress_level = "Low Depression :  You might be experiencing some everyday Depression, but it's likely manageable"
        elif total_score <= 5:
            stress_level = "Moderate Depression : You might be experiencing moderate Depression "
        else:
            stress_level = "High Depression : You might be experiencing significant Depression that requires additional support."

        return render(request, 'faq.html', {'status': 'Successfully Added', 'stress_level': stress_level})

    return render(request, 'faq.html')



'''def predict(request):
    if request.method == "POST":
        name = request.POST.get('name')
        try:
            os.remove("media/input/test/input.txt")
        except:
            pass
        fs=FileSystemStorage(location="media/input/test")
        fs.save("input.txt",name)
        
        # Get the prediction result
        result = test.predict()
        
        print("Result:",result)
        cus=upload(name=name,result=result,user_id=request.session['uid'])
        cus.save()
        return render(request,'predict.html',{'res':result})
    return render(request,'predict.html')'''


from django.core.files.base import ContentFile

def predict(request):
    if request.method == "POST":
        name = request.POST.get('name')


        """try:
            os.remove("media/input/test/input.txt")
        except:
            pass
        
        # Assuming name contains the content you want to save to the file
        content = name
        
        # Save the content to the file
        fs = FileSystemStorage(location="media/input/test")
        fs.save("input.txt", ContentFile(content))"""
        
        # Get the prediction result
        result = test1.predict(name)
        
        #print("Result:",result)
        
        # Assuming upload is a model and you want to save the result
        cus = upload(name=name, result=result, user_id=request.session['uid'])
        cus.save()
        
        return render(request, 'predict.html', {'res': result})
    
    return render(request, 'predict.html')
