# Alternative pdf converter library: https://github.com/JazzCore/python-pdfkit

from fpdf import FPDF

text_path="./RentalAgreementsData/RentalAgreementTextFiles/rental.txt"

# save FPDF() class into
# a variable pdf
pdf = FPDF()

# Add a page
pdf.add_page()

# set style and size of font
# that you want in the pdf
pdf.set_font( "Arial", size=15 )

# open the text file in read mode
f = open( text_path, "r" )

# insert the texts in pdf
for x in f:
    pdf.cell( 200, 10, txt=x, ln=1, align='C' )

pdf.output( "./RentalAgreementsData/RentalAgreementsPDFs/RentalAgreement.pdf")