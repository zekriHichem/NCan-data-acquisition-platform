from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import user_passes_test


from AideCan.forms import *
from AideCan.models import *
from AideCan.tokens import account_activation_token


#first page view
def first_page(request):

    if request.method == 'POST':

        form1 = AuthenticationForm(data=request.POST)
        if form1.is_valid():
            user = form1.get_user()
            login(request, user)
            return redirect('profile', user.id)


        # signup function

        form = signupForm(request.POST or None)
        form2 = DoctorFrom(request.POST or None)
        if form.is_valid() and form2.is_valid():
            user2 = form.save()
            doctor = form2.save()
            # user2.is_staff = True
            user2.is_active = False

            user2.save()
            Doctor.objects.filter(pk=doctor.pk).update(user=user2)

            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': user2,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user2.pk)),
                'token': account_activation_token.make_token(user2),
            })
            mail_subject = 'Activate your  account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'confirmation_email.html')


    else:
        form1 = AuthenticationForm(request.POST or None)
        form = signupForm(request.POST or None)
        form2 = DoctorFrom(request.POST or None)

    return render(request, 'aideCan/index.html', locals())



#Email validation view

def activate(request, uidb64, token,id):
    try:

        user = User.objects.get(pk=id)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None


    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_staff=True
        user.save()
        login(request, user)
        return redirect('profile', user.id)


    else:
        return HttpResponse('Activation link is invalid!')


#profile view
@login_required()
def profile_view(request,id):
    if request.user.id == id:
        id=id
        docs=Doctor.objects.filter(user_id=id)
        doc=Doctor()
        for i in docs:
            doc=i

        if request.method=="POST" :
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            speciality = request.POST['speciality']
            establishment = request.POST['establishment']
            print(request.FILES.get('img'))

            if request.FILES.get('img') is None:
                doc.specialty = speciality
                doc.establishment = establishment
            else:
                print("here")
                doc.specialty = speciality
                doc.establishment = establishment
                doc.photo = request.FILES.get("img")
            User.objects.filter(pk=id).update(first_name=first_name, last_name=last_name, email=email)
            doc.save()

        return render(request, 'aideCan/profile.html',locals())

    else:
        return redirect(Error)






#add mammography wiew
@login_required()
def add_mammography(request,id):
    if request.user.id == id:
        id = id
        docs = Doctor.objects.filter(user_id=id)
        doc = Doctor()

        for i in docs:
            doc = i
        mammographies = []

        list = doc.get_non_labled_mammogrphies()



        for l in list:
            mammographies.append(l)


        if request.method == 'POST':

            file = request.FILES.get('file')

            Mammography.objects.create(mammography=file,user=doc)
            return redirect('add_mammography',id)
        return render(request,'AideCan/add-mammo.html',locals())
    else:
        return redirect(Error(request))



@login_required()
def label_one(request,id,id_mammo):
    if request.user.id == id:
        id = id
        docs = Doctor.objects.filter(user_id=id)
        doc = Doctor()
        for i in docs:
            doc = i

        mammography = Mammography.objects.get(pk=id_mammo)

        diagnostics = Diagnostic.objects.filter(mammography_id=id_mammo)

        if request.method == "POST":
            background_tissue = request.POST['bt']
            abnormality_present = request.POST['ap']
            severity_of_abnormality = request.POST['soa']

            comment = request.POST['comment']
            position = request.POST['position']#TODO::add this to model diagnostic

            if (severity_of_abnormality == "null") :
                Diagnostic.objects.create(user=doc,mammography=mammography,background_tissue=background_tissue,abnormality_present=abnormality_present
                                      ,Cercle=position,comment=comment)
            else:
                Diagnostic.objects.create(user=doc, mammography=mammography, background_tissue=background_tissue,
                                          abnormality_present=abnormality_present,
                                          Severity_of_abnormality=severity_of_abnormality
                                          , Cercle=position, comment=comment)
            return redirect('add_mammography',id)

        return render(request, 'AideCan/label_one.html', locals())
    else:
        return redirect(Error(request))

@login_required()
def show_label(request,id,id_label):
    if request.user.id == id:
        id = id
        docs = Doctor.objects.filter(user_id=id)
        doc = Doctor()
        for i in docs:
            doc = i


        diagnostic = Diagnostic.objects.get(pk=id_label)
        diagnostics = Diagnostic.objects.filter(mammography_id=diagnostic.mammography.id)

        if request.method == "POST":
            background_tissue = request.POST['bt']
            abnormality_present = request.POST['ap']
            severity_of_abnormality = request.POST['soa']

            comment = request.POST['comment']
            position = request.POST['position']  # TODO::add this to model diagnostic

            diagnostic.background_tissue=background_tissue
            diagnostic.abnormality_present=abnormality_present

            if(severity_of_abnormality == "null"):
                diagnostic.Severity_of_abnormality=severity_of_abnormality
            diagnostic.Cercle=position
            diagnostic.comment=comment
            if(request.user.id == doc.user.id):
                diagnostic.save()

            return redirect('show_label',id,id_label)

        return render(request, 'AideCan/show_label.html', locals())
    else:
        return redirect(Error(request))






@login_required()
def sup_mammography(request,id,id_mammo):
    if request.user.id == id:
        id = id
        docs = Doctor.objects.filter(user_id=id)
        doc = Doctor()
        for i in docs:
            doc = i

        mammography = Mammography.objects.get(pk=id_mammo)
        mammographys = Mammography.objects.filter(user=doc)

        if mammography in mammographys :
            mammography.delete()
            return redirect('add_mammography',id)
        else:
            return redirect(Error(request))


    else:
        return redirect(Error(request))


@login_required()
def sup_diagnostic(request,id,id_diag):
    if request.user.id == id:
        id = id
        docs = Doctor.objects.filter(user_id=id)
        doc = Doctor()
        for i in docs:
            doc = i

        diagnostic = Diagnostic.objects.get(pk=id_diag)
        diagnostics = Diagnostic.objects.filter(user=doc)

        if diagnostic in diagnostics :
            diagnostic.delete()
            return redirect('random_labling',id)
        else:
            return redirect(Error(request))


    else:
        return redirect(Error(request))

@login_required()
def show_all_labels(request,id):
    if request.user.id == id:
        id = id
        docs = Doctor.objects.filter(user_id=id)
        doc = Doctor()
        for i in docs:
            doc = i

        diagnostics = Diagnostic.objects.filter(user=doc)

        return render(request,'AideCan/show_all_labels.html',locals())

    else:
        return redirect(Error(request))




@login_required()
def random_labling(request,id):

    if request.user.id == id:
        id = id
        docs = Doctor.objects.filter(user_id=id)
        doc = Doctor()
        for i in docs:
            doc = i

        mammographys = doc.get_teen_mammographys()

        for m in mammographys:
            mammography = m

        diagnostics = Diagnostic.objects.filter(user=doc).order_by("date")

        if request.method == "POST":
            background_tissue = request.POST['bt']
            abnormality_present = request.POST['ap']
            print("this is a result")
            print( request.POST['soa'])
            severity_of_abnormality = request.POST['soa']

            comment = request.POST['comment']
            position = request.POST['position']  # TODO::add this to model diagnostic


            if (severity_of_abnormality == "null"):

                Diagnostic.objects.create(user=doc, mammography=mammography, background_tissue=background_tissue,
                                      abnormality_present=abnormality_present
                                      , Cercle=position, comment=comment)
            else:
                Diagnostic.objects.create(user=doc, mammography=mammography, background_tissue=background_tissue,
                                          abnormality_present=abnormality_present,
                                          Severity_of_abnormality=severity_of_abnormality
                                          , Cercle=position, comment=comment)

        return render(request, 'AideCan/random_labling.html', locals())
        diagnostics = Diagnostic.objects.filter(user=doc)

        return render(request,'AideCan/show_all_labels.html',locals())

    else:
        return redirect(Error(request))


@login_required()
def statistic(request,id):
    if request.user.id == id:


        return render(request, 'AideCan/statistcs.html', locals())

    else:
        return redirect(Error(request))

#error view
def Error(request):
    return HttpResponse('error')


def tel(request):
    return render(request,'data.csv')

@login_required()
@user_passes_test(lambda u: u.is_superuser)
def adminTrain(request):

    modelver = ModelVersion.objects.all().order_by("date");
    return render(request,"AideCan/admin.html",locals())