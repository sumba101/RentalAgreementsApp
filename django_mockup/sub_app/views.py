import pickle
import time

from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import  QuestionsForm
from .template_processor import receive_values


def home(request):
    return render( request, 'sub_app/home.html' )
#
# def save_obj(obj, name ):
#     with open('sub_app/AnswersData/'+ name + '.pkl', 'wb') as f:
#         pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
#
# def load_obj(name):
#     with open('sub_app/AnswersData/' + name + '.pkl', 'rb') as f:
#         return pickle.load(f)

def questions(request):
    if request.method == 'POST':
        form = QuestionsForm( request.POST )
        if form.is_valid():
            print(form.cleaned_data)
            # A map where key values are same as the variable names in form and values are the values of input given by user
            receive_values(form.cleaned_data)
            return HttpResponseRedirect( '/results/' )

        else:
            print( form.errors )

    form = QuestionsForm()
    return render( request, 'sub_app/app.html',{'form':form} )


def result(request):
    return render( request, 'sub_app/result.html')
