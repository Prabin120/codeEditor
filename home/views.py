from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from random import randint
import subprocess
import os
from django.core.mail import send_mail
from .models import feedbackForm
from django.conf import settings
import re

# Create your views here.
def index(request):
    return render(request,'home/index.html')

def run_program(file_path,file_name, program_type, input_data=None):
    if program_type in ("c","cpp"):
        if program_type =="c":
            process = subprocess.Popen(['gcc', file_path + file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
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
        process = subprocess.Popen(['python3', file_path+file_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

    data ={
        'output':'',
        'error':"You are trying to import restricted libraries"
    }

    if language == "py":
        restrict_lib = 'asyncio, ctypes, fcntl, http, http.client, http.server, io, json, mmap, os, queue, sched, select, signal, socket, subprocess, sys, threading, time, traceback, tty, urllib, urllib.request, urllib.response, urllib.robotparser, xmlrpc.client, xmlrpc.server'
        restrict_lib_regex = re.compile(r'\b(' + '|'.join(restrict_lib.split(', ')) + r')\b')
        if restrict_lib_regex.search(code):
            return JsonResponse(data)

    elif language in ("c","cpp"):
        restrict_lib = "system, popen, fopen, freopen, freopen_s, tmpfile, tmpfile_s, tmpnam, tmpnam_s, gets, sprintf, snprintf, vsprintf, vfprintf, fscanf, sscanf, open, creat, remove, unlink, execl, execle, execlp, execv, execvp, fcntl, ioctl, pipe, mkfifo, opendir, readdir, closedir, getaddrinfo, gethostbyname, socket, bind, listen, accept, connect, send, recv, shutdown, select, ioctlsocket, WSAStartup, WSACleanup"
        restrict_lib_regex = re.compile(r'\b(' + '|'.join(restrict_lib.split(', ')) + r')\b')
        if restrict_lib_regex.search(code):
            return JsonResponse(data)

    elif language == "java":
        restrict_lib = "java.io.File|java.io.FileInputStream|java.io.FileOutputStream|java.io.RandomAccessFile|java.io.BufferedInputStream|java.io.BufferedOutputStream|java.io.BufferedReader|java.io.BufferedWriter|java.io.ByteArrayInputStream|java.io.ByteArrayOutputStream|java.io.CharArrayReader|java.io.CharArrayWriter|java.io.CharConversionException|java.io.DataInputStream|java.io.DataOutputStream|java.io.EOFException|java.io.Externalizable|java.io.FileDescriptor|java.io.FilePermission|java.io.FileNotFoundException|java.io.FileReader|java.io.FileWriter|java.io.FilterInputStream|java.io.FilterOutputStream|java.io.FilterReader|java.io.FilterWriter|java.io.Flushable|java.io.IOException|java.io.InputStream|java.io.InputStreamReader|java.io.InterruptedIOException|java.io.InvalidClassException|java.io.InvalidObjectException|java.io.LineNumberInputStream|java.io.LineNumberReader|java.io.NotActiveException|java.io.NotSerializableException|java.io.ObjectInput|java.io.ObjectInputStream|java.io.ObjectOutput|java.io.ObjectOutputStream|java.io.ObjectStreamClass|java.io.ObjectStreamConstants|java.io.ObjectStreamException|java.io.ObjectStreamField|java.io.OptionalDataException|java.io.OutputStream|java.io.OutputStreamWriter|java.io.PipedInputStream|java.io.PipedOutputStream|java.io.PipedReader|java.io.PipedWriter|java.io.PrintStream|java.io.PrintWriter|java.io.PushbackInputStream|java.io.PushbackReader|java.io.RandomAccessFile|java.io.Reader|java.io.SequenceInputStream|java.io.Serializable|java.io.StreamCorruptedException|java.io.StreamTokenizer|java.io.StringBufferInputStream|java.io.StringReader|java.io.StringWriter|java.io.SyncFailedException|java.io.UTFDataFormatException|java.io.UnsupportedEncodingException|java.io.WriteAbortedException|java.io.Writer|java.lang.annotation.Annotation|java.lang.annotation.AnnotationFormatError|java.lang.annotation.AnnotationTypeMismatchException|java.lang.annotation.Documented|java.lang.annotation.ElementType|java.lang.annotation.IncompleteAnnotationException|java.lang.annotation.Inherited|java.lang.annotation.Retention|java.lang.annotation.RetentionPolicy|java.lang.annotation.Target|java.lang.Appendable|java.lang.ArithmeticException|java.lang.ArrayIndexOutOfBoundsException|java.lang.ArrayStoreException|java.lang.AssertionError|java.lang.Boolean|java.lang.Byte|java.lang.CharSequence|java.lang.Character|java.lang.Class|java.lang.ClassCastException|java.lang.ClassCircularityError|java.lang.ClassFormatError|java.lang.ClassLoader|java.lang.ClassNotFoundException|java.lang.CloneNotSupportedException|java.lang.Cloneable|java.lang.Comparable|java.lang.Compiler|java.lang.Deprecated|java.lang.Double|java.lang.Enum|java.lang.Error|java.lang.Exception|java.lang.ExceptionInInitializerError|java.lang.Float|java.lang.IllegalAccessError|java.lang.IllegalAccessException|java.lang.IllegalArgumentException|java.lang.IllegalMonitorStateException|java.lang.IllegalStateException|java.lang.IllegalThreadStateException|java.lang.IncompatibleClassChangeError|java.lang.IndexOutOfBoundsException|java.lang.InheritableThreadLocal|java.lang.InstantiationError|java.lang.InstantiationException|java.lang.Integer|java.lang.InternalError|java.lang.InterruptedException|java.lang.Iterable|java.lang.LinkageError|java.lang.Long|java.lang.Math|java.lang.NegativeArraySizeException|java.lang.NoClassDefFoundError|java.lang.NoSuchFieldError|java.lang.NoSuchFieldException|java.lang.NoSuchMethodError|java.lang.NoSuchMethodException|java.lang.NullPointerException|java.lang.Number|java.lang.NumberFormatException|java.lang.Object|java.lang.OutOfMemoryError | java.net.DatagramPacket|java.net.DatagramSocket|java.net.HttpURLConnection|java.net.IDN|java.net.Inet4Address|java.net.Inet6Address|java.net.InetAddress|java.net.InetSocketAddress|java.net.JarURLConnection|java.net.MalformedURLException|java.net.MulticastSocket|java.net.NetworkInterface|java.net.NoRouteToHostException|java.net.PasswordAuthentication|java.net.PortUnreachableException|java.net.ProtocolException|java.net.Proxy|java.net.ProxySelector|java.net.ResponseCache|java.net.ServerSocket|java.net.Socket|java.net.SocketException|java.net.SocketImpl|java.net.SocketImplFactory|java.net.SocketOption|java.net.SocketOptions|java.net.SocketTimeoutException|java.net.StandardProtocolFamily|java.net.StandardSocketOptions|java.net.URI|java.net.URISyntaxException|java.net.URL|java.net.URLClassLoader|java.net.URLConnection|java.net.URLDecoder|java.net.URLEncoder|java.net.URLStreamHandler|java.net.URLStreamHandlerFactory|java.net.UnknownHostException|java.net.UnknownServiceException|java.net.URISyntaxException|java.net.http.HttpClient|java.net.http.HttpRequest|java.net.http.HttpResponse|java.net.http.HttpResponse$BodyHandler|java.net.http.HttpResponse$BodyHandlers|java.net.http.HttpTimeoutException|java.net.spi|java.net.SocketPermission|java.security.AccessControlContext|java.security.AccessController|java.security.AccessControlException|java.security.AlgorithmParameters|java.security.AllPermission|java.security.AuthProvider|java.security.BasicPermission|java.security.Certificate|java.security.CodeSigner|java.security.CodeSource|java.security.DigestException|java.security.DigestInputStream|java.security.DigestOutputStream|java.security.DomainLoadStoreParameter|java.security.DomainCombiner|java.security.GeneralSecurityException|java.security.Guard|java.security.GuardedObject|java.security.Identity|java.security.IdentityScope|java.security.InvalidAlgorithmParameterException|java.security.InvalidKeyException|java.security.InvalidParameterException|java.security.Key|java.security.KeyException|java.security.KeyFactory|java.security.KeyManagementException|java.security.KeyPair|java.security.KeyPairGenerator|java.security.KeyRep|java.security.KeyStore|java.security.KeyStoreException|java.security.KeyStoreSpi|java.security.MessageDigest|java.security.NoSuchAlgorithmException|java.security.NoSuchProviderException|java.security.Permission|java.security.PermissionCollection|java.security.Permissions|java.security.Policy|java.security.PolicySpi|java.security.Policy.Parameters|java.security.Principal|java.security.PrivateKey|java.security.ProtectionDomain|java.security.Provider|java.security.ProviderException|java.security.PublicKey|java.security.SecureClassLoader|java.security.SecureRandom|java.security.Security|java.security.SecurityPermission|java.security.Signature|java.security.SignatureException|java.security.SignedObject|java.security.Signer|java.security.Timestamp|java.security.cert.CRL|java.security.cert.CRLException|java.security.cert.CRLSelector|java.security.cert.CertPath|java.security.cert.CertPathBuilder|java.security.cert.CertPathBuilderException|java.security.cert.CertPathBuilderResult|java.security.cert.CertPathBuilderSpi|java.security.cert.CertPathChecker|java.security.cert.CertPathParameters|java.security.cert.CertPathValidator|java.security.cert.CertPathValidatorException|java.security.cert.CertPathValidatorResult|java.security.cert.CertPathValidatorSpi|java.security.cert.CertSelector|java.security.cert.CertStore|java.security.cert.CertStoreException|java.security.cert.CertStoreParameters|java.security.cert.CertStoreSpi|java.security.cert.Certificate|java.security.cert.CertificateEncodingException|java.security.cert.CertificateException|java.security.cert.CertificateExpiredException"
        restrict_lib_regex = re.compile(r'\b(' + '|'.join(restrict_lib.split('|')) + r')\b')
        if restrict_lib_regex.search(code):
            return JsonResponse(data)
        
    elif language == "js":
        restrict_lib = "jquery, angular, react, vue, ember, backbone, lodash, underscore, d3, three, babylon, p5, paper, fabric, howler, tone, webgl, webaudio, pixi, phaser, createjs, gsap, jquery-ui, jquery-mobile, jquery-validate, jquery-form, jquery-cookie, bootstrap, foundation, materialize, semantic-ui, ionic, cordova, phonegap, electron, XMLHttpRequest, fetch, WebSocket, Worker, postMessage, importScripts, localStorage, sessionStorage, indexedDB, openDatabase, FileReader, FileWriter, createObjectURL, revokeObjectURL, URL, document.execCommand, eval, Function, require, process, child_process, fs, path"
        restrict_lib_regex = re.compile(r'\b(' + '|'.join(restrict_lib.split(', ')) + r')\b')
        if restrict_lib_regex.search(code):
            return JsonResponse(data)

    else:
        data['error'] = "You are trying to compile a unsupported language"
        return JsonResponse(data)

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


