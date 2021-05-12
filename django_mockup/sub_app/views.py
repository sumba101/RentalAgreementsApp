import pickle
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View

from .forms import QuestionsForm, TempAgreementConfirmation
from .template_processor import receive_values, produce_with_unstructured_data


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

temp_agreement_state = None

def questions(request):
    global temp_agreement_state
    if request.method == 'POST':
        form = QuestionsForm( request.POST )
        if form.is_valid():
            print(form.cleaned_data)
            # A map where key values are same as the variable names in form and values are the values of input given by user

            temp_agreement_state = receive_values(form.cleaned_data)
            return HttpResponseRedirect( '/tempview/' )

        else:
            return render( request, 'sub_app/app.html', {'form': form} )

    form = QuestionsForm()
    return render( request, 'sub_app/app.html',{'form':form} )


def result(request):

    return render( request, 'sub_app/result.html')



def view_agreement1(request):
    global temp_agreement_state
    if request.method == 'POST':
        form = TempAgreementConfirmation(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # A map where key values are same as the variable names in form and values are the values of input given by user
            temp_agreement_state = produce_with_unstructured_data(form.cleaned_data['temp_state'],form.cleaned_data['freeform'])
            return HttpResponseRedirect( '/downloads/' )

    form = TempAgreementConfirmation(initial={'temp_state' : temp_agreement_state})
    return render( request, 'sub_app/temp1.html',{'form':form} )

# the following is for download button in scraper API
class CSVFileView( View ):
    def get(self, request, *args, **kwargs):
        response = HttpResponse( content_type='text/csv' )
        cd = 'attachment;filename="data.csv"'
        response['Content-Disposition'] = cd

        # writer = csv.writer( response, csv.excel )
        # response.write( u'\ufeff'.encode( 'utf8' ) )
        #
        # with open( data_handler.filepath ) as csv_file:
        #     csv_reader = csv.reader( csv_file, delimiter=',' )
        #     for row in csv_reader:
        #         writer.writerow( row )

        #todo: Set and save the file as a pdf using a function from here

        return response


def scraper(request):
    Download_button = 0

    if (request.method == 'POST' and len( request.FILES ) != 0):
        uploaded_file = request.FILES['document']
        if uploaded_file.name.endswith( '.csv' ):
            data_handler.reset()  # resetting the object
            data_handler.save_file( uploaded_file )
            if data_handler.clean_and_validate_data() == False:
                data_handler.reset()
                Upload_error = 1

            else:
                Data_ready = 1

    elif (request.method == 'POST'):
        form = ScraperForm( request.POST )
        if form.is_valid():
            URL = form.cleaned_data['URL']
            # send url to the scraper and create data.csv
            s = Scraper( URL )
            print( "sent URL" )
            filename = str( uuid.uuid4() ) + ".csv"
            s.make_csv( filename='SSAD_project/media/' + filename )
            print( "finished making file" )
            data_handler.reset()  # resetting the object

            data_handler.save_file( filename, save=False )
            if data_handler.clean_and_validate_data() == False:
                data_handler.reset()

            else:
                print( "Data csv made" )
                Data_ready = 1
                Download_button = 1

    scraper = ScraperForm()
    return render( request, 'sub_app/scraper.html',
                   {'scraper': scraper, 'Download': Download_button} )
