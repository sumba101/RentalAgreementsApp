from django import forms


class QuestionsForm( forms.Form ):
    name_Of_The_lesse = forms.CharField( label="Name of the Lesse", max_length=100 )
    name_Of_The_lessor = forms.CharField( label="Name of the Lessor", max_length=100 )
    lesse_child_of = forms.CharField( label="(Lesse) Son/Daughter of", max_length=100 )
    lessor_child_of = forms.CharField( label="(Lessor) Son/Daughter of", max_length=100 )
    address_of_leased_residence = forms.CharField( label="Address of Leased Residence", max_length=100 )
    tenure_of_lease = forms.IntegerField( label="Tenure of the Lease", help_text="in number of Months" )
    date_of_signing = forms.DateField( label="Date of the Lease Signing", help_text="day/month/year",
                                       input_formats="%d/%m/%Y", widget=forms.DateInput )

    rent_amount = forms.IntegerField( label="Rent Amount", help_text="monthly in Rs" )
    due_day= forms.IntegerField(label="Day of month for rent due",help_text="in no.of days from month start")
    security_deposit = forms.IntegerField( label="Security Deposit", help_text="in Rs" )
    security_deposit_release_date = forms.DateField( label="Date of security deposit release", help_text="day/month/year",
                                       input_formats="%d/%m/%Y", widget=forms.DateInput )

    maintenance_charge = forms.ChoiceField( label="Maintenance charges", widget=forms.RadioSelect,
                                    choices=[('1', 'Lesse'), ('2', 'Lessor'), ('3', 'Included in Rent')] )

    electricity_charge = forms.ChoiceField( label="Electricity charges", widget=forms.RadioSelect,
                                    choices=[('1', 'Lesse'), ('2', 'Lessor'), ('3', 'Included in Rent')] )


    period_of_vacating_notice = forms.IntegerField( label="Period of Notice before vacating", help_text="in Days" )

    furnishing = forms.ChoiceField( label="Furnishing", widget=forms.RadioSelect,
                                    choices=[('1', 'Fully furnished'), ('2', 'Semi furnished'), ('3', 'Unfurnished')] )
    furnishing_present = forms.CharField( label="List Furnishing present in house and/or also description of house", max_length=200 )

