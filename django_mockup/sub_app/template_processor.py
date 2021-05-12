import chevron
import inflect

# Trial
trial_mhash = {
    'agreement_date_day': '20',
    'agreement_date_month': 'April',
    'agreement_date_year': '2011',
    'owner_salutation': 'Mrs.',
    'owner_name': 'Asha Ramesh',
    'owner_age': '45',
    'owner_address': '1st Floor, 82A, Vysya Bank Colony, ShantiniketanLayout, Arakere Post, Bannerghatta Road, Bangalore - 560076',
    'owner_relation_to': 'w/o',
    'owner_relative_salutation': 'Mr.',
    'owner_relative_name': 'Ramesh K. N.',
    'tenant_salutation': 'Ms.',
    'tenant_name': 'Sadasivuni Deepti',
    'tenant_age': '34',
    'tenant_address': '53-38-20, KRM Colony, Maddilapalem, Vishakapatnam, AP530013',
    'tenant_relation_to': 'D/o',
    'tenant_relative_salutation': 'Mr.',
    'tenant_relative_name': 'K Sadasivuni',
    'house_address': '2nd Floor on Site # 82A, Vysya Bank Colony, ShantiniketanLyt, Arakere Post, Bannerghatta Road, Bangalore - 560076',
    'period_value': '11',
    'period_unit': 'months',
    'start_date_day': '20',
    'start_date_month': 'April',
    'start_date_year': '2011',
    'end_date_day': '20',
    'end_date_month': 'March',
    'end_date_year': '2011',
    'monetary_unit': 'Rs.',
    'monthly_rent_value': '7000',
    'monthly_rent_words': 'Seven thousand',
    'monthly_rent_deadline': '5',
    'deposit_amount_nos': '90000',
    'deposit_amount_words': 'Ninety thousand',
    'max_months_no_rent': '2',
    'max_unit_no_rent': 'consecutive months',
    'advance_notice_end': '3'
}

def receive_values(mhash):
    # A map where key values are same as the variable names in form and values are the values of input given by user
    # Look at forms.py file to see what the variables names are(i.e the key names)
    with open('sub_app/template_mustach.txt', 'r') as f:
        template = f.read()

    refine_hash(mhash)
    return chevron.render(template=template, data=mhash)

def produce_with_unstructured_data(current_agreement_state,freeform):
    # Here current_agreement_state is a string of the current rental agreement state after modification
    # freeform would be the freeform data, each new clause would be start with a * and hence that can be used as the separator for processing
    pass
    # function must return the state of the rental agreement after the merging of the freeform data clauses in the current agreement state
    # must be returned as a string itself

def refine_hash(mhash):
    #todo need to handle dates and days properly, the value returned would be an object of datetime.date
    p = inflect.engine()

    period_value = int(mhash['period_value'])
    if period_value == 1:
        mhash['period_unit'] = mhash['period_unit'][:-1]

    max_months_no_rent = int(mhash['max_months_no_rent'])
    if max_months_no_rent == 1:
        mhash['max_months_no_rent'] = 'month'

    monthly_rent_value = int(mhash['monthly_rent_value'])
    mhash['monthly_rent_words'] = p.number_to_words(monthly_rent_value).capitalize()

    deposit_amount_nos = int(mhash['deposit_amount_nos'])
    mhash['deposit_amount_words'] = p.number_to_words(deposit_amount_nos).capitalize()

    # ordinal for all days ....
    convert_to_ordinal(mhash, 'agreement_date_day', p)
    convert_to_ordinal(mhash, 'start_date_day', p)
    convert_to_ordinal(mhash, 'end_date_day', p)
    convert_to_ordinal(mhash, 'monthly_rent_deadline', p)


def convert_to_ordinal(mhash, key, p):
    value = p.ordinal(int(mhash[key]))
    mhash[key] = value

