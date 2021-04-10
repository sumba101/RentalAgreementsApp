import chevron
import inflect

def receive_values(mhash):
    # A map where key values are same as the variable names in form and values are the values of input given by user
    # Look at forms.py file to see what the variables names are(i.e the key names)
    with open('template_mustach.txt', 'r') as f:
        template = f.read()

    refine_hash(mhash)
    chevron.render(template=template, data=mhash)


def refine_hash(mhash):
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
