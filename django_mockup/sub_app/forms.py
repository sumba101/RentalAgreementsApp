from django import forms


class QuestionsForm(forms.Form):
    mhash = dict()
    agreement_date = forms.DateField(label='Agreement signing date', help_text="day/month/year",
                                     input_formats="%d/%m/%Y", widget=forms.DateInput)

    # mhash['owner_salutation']
    mhash['owner_name'] = forms.CharField(label='Name of the tenant', max_length=100)
    mhash['owner_age'] = forms.IntegerField(label='Age of the owner', help_text='In years')
    mhash['owner_address'] = forms.CharField(label='Address of the owner', max_length=1000)
    # mhash['owner_relation_to']
    # mhash['owner_relative_salutation']
    mhash['owner_relative_name'] = forms.CharField(label='Name of owner\'s relative', max_length=100)

    # mhash['tenant_salutation']
    mhash['tenant_name'] = forms.CharField(label='Name of the tenant', max_length=100)
    mhash['tenant_age'] = forms.IntegerField(label='Age of the tenant', help_text='In years')
    mhash['tenant_address'] = forms.CharField(label='Address of the tenant', max_length=1000)
    # mhash['tenant_relation_to']
    # mhash['tenant_relative_salutation']
    mhash['tenant_relative_name'] = forms.CharField(label='Name of tenant\'s relative', max_length=100)

    mhash['house_address'] = forms.CharField(label='Address of the rented property', max_length=1000)

    mhash['period_value'] = forms.IntegerField(label='Period of stay', help_text='In number of units')
    # mhash['period_unit']
    start_date = forms.DateField(label='Agreement start date', help_text='day/month/year',
                                 input_formats='%d/%m/%Y', widget=forms.DateInput)
    end_date = forms.DateField(label='Agreement end date', help_text='day/month/year',
                               input_formats='%d/%m/%Y', widget=forms.DateInput)

    # mhash['monetary_unit']
    mhash['monthly_rent_value'] = forms.IntegerField(label='Monthly rent value', help_text='In selected monetary units')
    mhash['monthly_rent_deadline'] = forms.IntegerField(label='Deadline day for payment of monthly rent',
                                                        help_text='Fixed day of every month')

    mhash['deposit_amount_nos'] = forms.IntegerField(label='Deposit amount', help_text='In selected monetary units')

    mhash['max_months_no_rent'] = forms.IntegerField(label='Number of months for which the tenant cannot defer '
                                                           'payment of monthly rent',
                                                     help_text='In months')

    mhash['advance_notice_end'] = forms.IntegerField(label='Minimum number of months for notice period after which '
                                                           'agreement can be terminated early if desired by either '
                                                           'party',
                                                     help_text='In months')

    # name_Of_The_lesse = forms.CharField(label="Name of the Lesse", max_length=100)
    # name_Of_The_lessor = forms.CharField(label="Name of the Lessor", max_length=100)
    # lesse_child_of = forms.CharField(label="(Lesse) Son/Daughter of", max_length=100)
    # lessor_child_of = forms.CharField(label="(Lessor) Son/Daughter of", max_length=100)
    # address_of_leased_residence = forms.CharField(label="Address of Leased Residence", max_length=100)
    # tenure_of_lease = forms.IntegerField(label="Tenure of the Lease", help_text="in number of Months")
    # date_of_signing = forms.DateField(label="Date of the Lease Signing", help_text="day/month/year",
    #                                   input_formats="%d/%m/%Y", widget=forms.DateInput)
    #
    # rent_amount = forms.IntegerField(label="Rent Amount", help_text="monthly in Rs")
    # due_day = forms.IntegerField(label="Day of month for rent due", help_text="in no.of days from month start")
    # security_deposit = forms.IntegerField(label="Security Deposit", help_text="in Rs")
    # security_deposit_release_date = forms.DateField(label="Date of security deposit release",
    #                                                 help_text="day/month/year",
    #                                                 input_formats="%d/%m/%Y", widget=forms.DateInput)
    #
    # maintenance_charge = forms.ChoiceField(label="Maintenance charges", widget=forms.RadioSelect,
    #                                        choices=[('1', 'Lesse'), ('2', 'Lessor'), ('3', 'Included in Rent')])
    #
    # electricity_charge = forms.ChoiceField(label="Electricity charges", widget=forms.RadioSelect,
    #                                        choices=[('1', 'Lesse'), ('2', 'Lessor'), ('3', 'Included in Rent')])
    #
    # period_of_vacating_notice = forms.IntegerField(label="Period of Notice before vacating", help_text="in Days")
    #
    # furnishing = forms.ChoiceField(label="Furnishing", widget=forms.RadioSelect,
    #                                choices=[('1', 'Fully furnished'), ('2', 'Semi furnished'), ('3', 'Unfurnished')])
    # furnishing_present = forms.CharField(label="List Furnishing present in house and/or also description of house",
    #                                      max_length=200)
