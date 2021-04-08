from django import forms

class QuestionsForm( forms.Form ):
    name_Of_The_Lesse = forms.CharField(label="Name of the Lesse",max_length=100)
    name_Of_The_Lessor = forms.CharField(label="Name of the Lessor",max_length=100)
    address_of_leased_residence = forms.CharField(label="Address of Leased Residence",max_length=100)
    tenure_of_lease = forms.IntegerField(label="Tenure of the Lease",help_text="in number of Months")
    date_of_signing = forms.DateField(label="Date of the Lease Signing",help_text="day/month/year",input_formats="%d/%m/%Y",widget=forms.DateInput)

    rent_amount = forms.IntegerField( label="Rent Amount",help_text="monthly in Rs" )
    security_depost = forms.IntegerField( label="Security Deposit",help_text="in Rs" )
    maintenance_charge = forms.IntegerField( label="Maintenance Charges", help_text="monthly in Rs")
    electricity_charge = forms.IntegerField( label="Electricity charges", help_text="monthly in Rs" )
    period_of_vacating_notice = forms.IntegerField( label="Period of Notice before vacating",help_text="in Days" )
    furnishing = forms.ChoiceField( label="Furnishing", widget=forms.RadioSelect,choices=[('1','Fully furnished'),('2','Semi furnished'),('3','Unfurnished')] )

# Name(s) of the lessee
# Name of the lessor
# Son/Daughter of data for Lessor and Lessee
# Address of the residence to be given on lease
# Tenure of lease
# Date of signing
# Rent amount
# Security deposit and when it is released
# Maintenance charges
# Electricity charges
# When would late fee be applicable, what mode of payment, how much will it be accrued
# Period of notice before vacating premises
# Fully furnished/Semi furnished/Unfurnished
