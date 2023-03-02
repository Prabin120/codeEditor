from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from random import randint
import subprocess
import os
from django.core.mail import send_mail
from .models import feedbackForm
from django.conf import settings


# Create your views here.
def index(request):
    return render(request,'home/index.html')

def run_program(file_path,file_name, program_type, input_data=None):
    if program_type == 'c':
        process = subprocess.Popen(['gcc', file_path + file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        if process.returncode == 0:
            if input_data:
                input_file = open("input.txt", "w")
                input_file.write(str(input_data))
                input_file.close()
                process = subprocess.Popen(['./a.out'], stdin=open("input.txt"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                process = subprocess.Popen(['./a.out'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = process.stdout.read().decode('utf-8')
            error = process.stderr.read().decode('utf-8')
        else:
            error = process.stderr.read().decode('utf-8')
            output = ""
        return output, error
    elif program_type == 'cpp':
        process = subprocess.Popen(['g++', file_path + file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        if process.returncode == 0:
            if input_data:
                input_file = open("input.txt", "w")
                input_file.write(str(input_data))
                input_file.close()
                process = subprocess.Popen(['./a.out'], stdin=open("input.txt"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                process = subprocess.Popen(['./a.out'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = process.stdout.read().decode('utf-8')
            error = process.stderr.read().decode('utf-8')
        else:
            error = process.stderr.read().decode('utf-8')
            output = ""
        return output, error
    elif program_type == 'java':
        process = subprocess.Popen(['javac', file_path+file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        if process.returncode == 0:
            class_file = file_name.replace('.java', '')
            class_path = 'home/programs/'
            if input_data:
                input_file = open("input.txt", "w")
                input_file.write(str(input_data))
                input_file.close()
                process = subprocess.Popen(['java', '-cp', str(class_path), class_file], stdin=open("input.txt"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                process = subprocess.Popen(['java', '-cp', str(class_path), class_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = process.stdout.read().decode('utf-8')
            error = process.stderr.read().decode('utf-8')
            return output, error
        else:
            error = process.stderr.read().decode('utf-8')
            output = ""
        return output, error
    elif program_type == 'py':
        process = subprocess.Popen(['python', file_path+file_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate(input_data.encode() if input_data else None)
        return output.decode(), error.decode()
    elif program_type == 'js':
        process = subprocess.Popen(['node', file_path + file_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if input_data:
            output, error = process.communicate(input_data.encode())
        else:
            output, error = process.communicate()
        return output.decode(), error.decode()

    else:
        return "Invalid program type"

@csrf_exempt
def code(request):
    language = request.POST['language']
    code = str(request.POST['code'])
    file_name=""
    file_path = "home/programs/"
    if language == "java":
        num = randint(0,1000000000)
        file_name = "MainClass"+str(num)+"."+language
        if "MainClass" in code:
            code = code.replace("MainClass","MainClass"+str(num),1)
        else:
            return JsonResponse({"output":"Error: Please specify main class name as MainClass","error":""})
    else:
        file_name=language+str(randint(0,1000000000))+"."+language

    with open (file_path+file_name,"w") as file:
        file.write(code)
    input_data = request.POST['input']
    output,error = run_program(file_path,file_name, language,input_data)

    if language == 'java':
        os.remove(file_path+file_name)
        os.remove(file_path+file_name.replace('.java','.class'))
    else:
        os.remove(file_path+file_name)
    return JsonResponse({"output":output,"error":error})

def send_feedback_email(name, email, message):
    subject = 'Feedback from {} for codeEditor'.format(name)
    body = 'Name: {}\n\nEmail: {}\n\n{}'.format(name,email, message)
    sender_email = settings.EMAIL_HOST_USER
    recipient_list = ['prabinsharma120@gmail.com']
    send_mail(subject, body, sender_email, recipient_list)
    
def send_response(name, email):
    body = "Thank you {} for your valuable response.\nWe are working continuosly working to give you a better user experience \n\n\n\n\n\n\n\n\tRegards,\nTeam, codeEditor\ncodeeditor12@gmail.com".format(name)
    subject = "Feedback Response"
    sender_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, body, sender_email, recipient_list)

@csrf_exempt
def feedback(request):
    if request.method =='POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        try:
            data=feedbackForm.objects.create(name=name,email=email,message=message)
            data.save()
            send_feedback_email(name=name, email=email, message=message)
            send_response(name=name,email=email)
            return JsonResponse({'sucess':"success"})
        except Exception as e:
            print(e)
            return JsonResponse({'sucess':"failed"})


