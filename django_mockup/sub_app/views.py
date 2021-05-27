import mimetypes

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View

from .forms import QuestionsForm, TempAgreementConfirmation, FinalEdits
from .pdfConverter import save_pdf_convert
from .template_processor import receive_values, produce_with_unstructured_data


def home(request):
    return render( request, 'sub_app/home.html' )

text_path="sub_app/RentalAgreementsData/RentalAgreementTextFiles/rental.txt"
pdf_path = "sub_app/RentalAgreementsData/RentalAgreementsPDFs/RentalAgreement.pdf"
temp_agreement_state = None

def questions(request):
    global temp_agreement_state
    if request.method == 'POST':
        form = QuestionsForm( request.POST )
        if form.is_valid():
            # A map where key values are same as the variable names in form and values are the values of input given by user

            temp_agreement_state = receive_values(form.cleaned_data)
            return HttpResponseRedirect( '/tempview/' )

        else:
            return render( request, 'sub_app/app.html', {'form': form} )

    form = QuestionsForm()
    return render( request, 'sub_app/app.html',{'form':form} )


def view_agreement1(request):
    global temp_agreement_state
    if request.method == 'POST':
        form = TempAgreementConfirmation(request.POST)
        if form.is_valid():
            # A map where key values are same as the variable names in form and values are the values of input given by user
            temp_agreement_state = produce_with_unstructured_data(form.cleaned_data['temp_state'],form.cleaned_data['freeform'])
            return HttpResponseRedirect( '/downloads/' )
        else:
            return render( request, 'sub_app/temp1.html', {'form': form} )

    form = TempAgreementConfirmation(initial={'temp_state' : temp_agreement_state})
    return render( request, 'sub_app/temp1.html',{'form':form} )

# the following is for download button in scraper API
class CSVFileView( View ):
    def get(self, request, *args, **kwargs):
        file = open(pdf_path,'rb')
        mime_type,_ = mimetypes.guess_type(pdf_path)
        response = HttpResponse(file, content_type=mime_type )
        cd = 'attachment;filename="Rental_Agreement.pdf"'
        response['Content-Disposition'] = cd

        return response


def scraper(request):
    Download_button = 0
    Data_done = 0
    if request.method == 'POST':
        form = FinalEdits( request.POST )
        if form.is_valid():
            # The final edits to the form is done, so just pdf convert it and save it
            final_agreement = form.cleaned_data['final_edit']
            with open(text_path,'w') as f:
                f.write(final_agreement)

            save_pdf_convert()
            Data_done = 1
            Download_button = 1
        return render( request, 'sub_app/scraper.html',
                           {'scraper': form, 'Download': Download_button, 'Data_done':Data_done} )

    form = FinalEdits(initial ={'final_edit':temp_agreement_state})
    return render( request, 'sub_app/scraper.html',
                   {'scraper': form, 'Download': Download_button, 'Data_done':Data_done} )
