from django import forms


class QuestionsForm(forms.Form):

    agreement_date = forms.DateField(label='Agreement signing date', help_text="year/month/day")

    # salutations: Mr,Mrs,Miss
    owner_salutation = forms.CharField(label="Salutation of Owner",
                                       widget=forms.Select(choices=[('Mrs.', 'Mrs.'), ('Mr.', 'Mr.'), ('Ms.', 'Ms.')]))
    owner_name = forms.CharField(label='Name of the Owner', max_length=100)
    owner_age = forms.IntegerField(label='Age of the Owner', help_text='In years',min_value=18,max_value=110)
    owner_address = forms.CharField(label='Address of the Owner', max_length=1000,
                                    widget=forms.Textarea(attrs={"rows": 10, "cols": 30}))

    # relation of relative, Sonof, Daughterof
    owner_relation = forms.CharField(label="Relation of Owner",
                                     widget=forms.Select(choices=[('Son of', 'Son of'), ('Daughter of', 'Daughter of'), ('Wife of', 'Wife of')]))
    owner_relative_salutation = forms.CharField(label="Salutation of Owner",
                                                widget=forms.Select(choices=[('Mrs.', 'Mrs.'), ('Mr.', 'Mr.'), ('Ms.', 'Ms.')]))
    owner_relative_name = forms.CharField(label='Name of Owner\'s relative', max_length=100)
    
    tenant_salutation = forms.CharField(label="Salutation of Tenant",
                                        widget=forms.Select(choices=[('Mrs.', 'Mrs.'), ('Mr.', 'Mr.'), ('Ms.', 'Ms.')]))
    tenant_name = forms.CharField(label='Name of the Tenant', max_length=100)
    tenant_age = forms.IntegerField(label='Age of the Tenant', help_text='In years',min_value=18,max_value=110)
    tenant_address = forms.CharField(label='Address of the Tenant', max_length=1000,
                                     widget=forms.Textarea(attrs={"rows": 10, "cols": 30}))

    tenant_relation = forms.CharField(label="Relation of Tenant",
                                      widget=forms.Select( choices=[('Son of', 'Son of'), ('Daughter of', 'Daughter of'), ('Wife of', 'Wife of')]))

    tenant_relative_salutation = forms.CharField(label="Salutation of Owner",
                                                 widget=forms.Select(choices=[('Mrs.', 'Mrs.'), ('Mr.', 'Mr.'), ('Ms.', 'Ms.')]))
    tenant_relative_name = forms.CharField(label='Name of Tenant\'s relative', max_length=100)

    house_address = forms.CharField(label='Address of the rented property', max_length=1000,
                                    widget=forms.Textarea(attrs={"rows": 10, "cols": 30}))

    period_value = forms.IntegerField(label='Period of stay', help_text='In number of months',min_value=1)

    start_date = forms.DateField(label='Lease start date', help_text="year/month/day")
    # end_date can be calculated from above details
    # end_date = forms.DateField(label='Lease end date', help_text="year/month/day")

    monthly_rent_value = forms.IntegerField(label='Monthly rent value', help_text='In Rs',min_value=0)
    monthly_rent_deadline = forms.IntegerField(label='Deadline day for payment of monthly rent', help_text='Fixed day of every month',min_value=0)
    deposit_amount_nos = forms.IntegerField(label='Deposit amount', help_text='In Rs',min_value=0)

    max_months_no_rent = forms.IntegerField(label='Number of months for which the tenant cannot defer payment of monthly rent',
                                            help_text='In months',min_value=0)

    advance_notice_end = forms.IntegerField(label='Minimum number of months for notice period after which agreement can be terminated early if desired by either party',
                                            help_text='In months',min_value=0)

    furnishing = forms.ChoiceField(label="Furnishing", widget=forms.RadioSelect,
                                   choices=[('Fully furnished', 'Fully furnished'), ('Semi furnished', 'Semi furnished'), ('Unfurnished', 'Unfurnished')])
    furnishing_present = forms.CharField(label="List Furnishing present in house and/or also description of house",
                                         max_length=200, widget=forms.Textarea(attrs={"rows": 10, "cols": 30}))


class TempAgreementConfirmation(forms.Form):
    temp_state = forms.CharField(label="Edit this temporary state if needed",
                                 widget=forms.Textarea(attrs={"rows": 50, "cols": 60}))
    freeform = forms.CharField(label="Enter points to add (starting with *) in freeform manner",
                               widget=forms.Textarea(attrs={"rows": 20, "cols": 50}))

class FinalEdits(forms.Form):
    final_edit = forms.CharField(label="Make final edits if needed",
                                 widget=forms.Textarea(attrs={"rows": 50, "cols": 60}))