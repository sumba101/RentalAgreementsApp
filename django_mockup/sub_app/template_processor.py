import chevron
import inflect
from dateutil.relativedelta import relativedelta
from sub_app.semantic_search import *

tokenizer, model = load_models()


def receive_values(mhash):
    # A map where key values are same as the variable names in form and values are the values of input given by user
    # Look at forms.py file to see what the variables names are(i.e the key names)
    mhash['end_date'] = mhash['start_date'] + relativedelta(months=mhash['period_value'])
    print(mhash)
    with open('sub_app/template_mustach.txt', 'r') as f:
        template = f.read()

    refine_hash(mhash)

    return chevron.render(template=template, data=mhash)


def produce_with_unstructured_data(current_agreement_state, freeform, index_name='sub_app/dense_index_nonoptim.bin'):
    global tokenizer, model
    # Here current_agreement_state is a string of the current rental agreement state after modification
    # freeform would be the freeform data, each new clause would be start with a * and hence that can be used as the
    # separator for processing pass
    # function must return the state of the rental agreement after the merging of the freeform data clauses in the
    # current agreement state must be returned as a string itself

    freeform = modify_freeform_input(freeform)
    queries = get_query_list(freeform)

    query_embeddings = get_embeddings(queries, tokenizer, model)
    index = load_index(index_name)
    additive_clauses = search_clauses_for_queries(query_embeddings, index)

    delimiter = 'except for normal wear and tear.'
    agreement_split = current_agreement_state.split(delimiter)
    agreement_split[0] += delimiter
    updated_agreement = add_clauses_to_agreement(agreement_split[0], additive_clauses)
    updated_agreement += agreement_split[1]
    updated_agreement = remove_duplicates(updated_agreement, old_delimiter='\n\n', new_delimiter='\n\n')

    return updated_agreement


def refine_hash(mhash):
    p = inflect.engine()

    mhash['monetary_unit'] = 'Rs.'

    mhash['period_unit'] = 'months'
    period_value = int(mhash['period_value'])
    if period_value == 1:
        mhash['period_unit'] = mhash['period_unit'][:-1]

    mhash['max_no_rent_unit'] = 'months'
    max_months_no_rent = int(mhash['max_months_no_rent'])
    if max_months_no_rent == 1:
        mhash['max_no_rent_unit'] = mhash['max_no_rent_unit'][:-1]

    mhash['advance_notice_unit'] = 'months'
    advance_notice_end = int(mhash['advance_notice_end'])
    if advance_notice_end == 1:
        mhash['advance_notice_unit'] = mhash['advance_notice_unit'][:-1]

    monthly_rent_value = int(mhash['monthly_rent_value'])
    mhash['monthly_rent_words'] = p.number_to_words(monthly_rent_value).capitalize()

    deposit_amount_nos = int(mhash['deposit_amount_nos'])
    mhash['deposit_amount_words'] = p.number_to_words(deposit_amount_nos).capitalize()

    agreement_date = mhash['agreement_date']
    mhash['agreement_date_day'] = agreement_date.day
    mhash['agreement_date_month'] = agreement_date.strftime('%B')
    mhash['agreement_date_year'] = agreement_date.year

    start_date = mhash['start_date']
    mhash['start_date_day'] = start_date.day
    mhash['start_date_month'] = start_date.strftime('%B')
    mhash['start_date_year'] = start_date.year

    end_date = mhash['end_date']
    mhash['end_date_day'] = end_date.day
    mhash['end_date_month'] = end_date.strftime('%B')
    mhash['end_date_year'] = end_date.year

    # ordinal for all days ....
    convert_to_ordinal(mhash, 'agreement_date_day', p)
    convert_to_ordinal(mhash, 'start_date_day', p)
    convert_to_ordinal(mhash, 'end_date_day', p)
    convert_to_ordinal(mhash, 'monthly_rent_deadline', p)


def convert_to_ordinal(mhash, key, p):
    value = p.ordinal(int(mhash[key]))
    mhash[key] = value


def modify_freeform_input(freeform):
    freeform = freeform.lower()
    freeform = freeform.replace('i', 'owner')
    freeform = freeform.replace('my', 'owner\'s')
    freeform = freeform.replace('you', 'tenant')
    freeform = freeform.replace('your', 'tenant\'s')
    freeform = freeform.replace('we', 'owner & tenant')

    return freeform


def add_clauses_to_agreement(agreement, additive_clauses):
    agreement = agreement.strip()
    for clause in additive_clauses:
        agreement += '\n\n' + clause

    return agreement


if __name__ == '__main__':
    import os
    import datetime

    os.chdir('../')

    # Trial
    trial_mhash = {
        'agreement_date': datetime.date(2011, 4, 20),
        'owner_salutation': 'Mrs.',
        'owner_name': 'Asha Ramesh',
        'owner_age': '45',
        'owner_address': '1st Floor, 82A, Vysya Bank Colony, ShantiniketanLayout, Arakere Post, Bannerghatta Road, Bangalore - 560076',
        'owner_relation': 'w/o',
        'owner_relative_salutation': 'Mr.',
        'owner_relative_name': 'Ramesh K. N.',
        'tenant_salutation': 'Ms.',
        'tenant_name': 'Sadasivuni Deepti',
        'tenant_age': '34',
        'tenant_address': '53-38-20, KRM Colony, Maddilapalem, Vishakapatnam, AP530013',
        'tenant_relation': 'D/o',
        'tenant_relative_salutation': 'Mr.',
        'tenant_relative_name': 'K Sadasivuni',
        'house_address': '2nd Floor on Site # 82A, Vysya Bank Colony, ShantiniketanLyt, Arakere Post, Bannerghatta Road, Bangalore - 560076',
        'period_value': '11',
        'start_date': datetime.date(2011, 4, 20),
        'end_date': datetime.date(2012, 3, 20),
        'monthly_rent_value': '7000',
        'monthly_rent_words': 'Seven thousand',
        'monthly_rent_deadline': '5',
        'deposit_amount_nos': '90000',
        'deposit_amount_words': 'Ninety thousand',
        'max_months_no_rent': '2',
        'max_unit_no_rent': 'consecutive months',
        'advance_notice_end': '3',
        'furnishing': 'Unfurnished',
        'furnishing_present': '4 Tubelights, 3 Fans, 1 Sofa, 6 Chairs, 3 Taps, 2 Basins, 1 AC, 1 TV'
    }

    trial_unfinished_agreement = '''
    Rental Agreement

This agreement is made on the 20th day of April, 2011
by and between
Mrs. Asha Ramesh, age 45 years,
1st Floor, 82A, Vysya Bank Colony, ShantiniketanLayout, Arakere Post, Bannerghatta Road, Bangalore - 560076,
w/o Mr. Ramesh K. N.,
herein referred to as the Owner;
and Ms. Sadasivuni Deepti, age 34 years,
53-38-20, KRM Colony, Maddilapalem, Vishakapatnam, AP530013,
D/o Mr. K Sadasivuni,
herein referred to as the Tenant.

The owner has agreed to rent out the house premises at 2nd Floor on Site # 82A, Vysya Bank Colony, ShantiniketanLyt, Arakere Post, Bannerghatta Road, Bangalore - 560076, and the tenant has agreed to occupy the same.

The agreement shall be for a period of 11 months beginning from 20th of April, 2011 and ending on 20th of March, 2012.

The tenant agrees to pay a monthly rent of Rs. 7000 (Seven thousand only) starting from 20th of April, 2011. The amount shall be paid before the 5th of every succeeding calendar month for a period of 11 months.

The tenant has deposited with the owner a sum of Rs. 90000 (Ninety thousand only) as security deposit without interest. The deposit shall not entitle the tenant to withhold any payment of monthly rent. The deposit shall be refundable to the tenant at the end of the agreement subject no outstanding payments and return of possession in tenantable condition.

The tenant shall pay the electricity and water charges on the house for the period of the agreement. The tenant shall also pay for all utilities and services based on the occupancy of the premises.

If the tenant fails to pay the monthly rent for a period of 2 months, the owner is at liberty to terminate the agreement and take back immediate possession of the house.

An advance notice of 3 months is required if either of the tenant or owner wish to terminate this agreement before the completion of the period of 11 months.

Tenant should use the rented premises only for residential purpose.

Tenant shall not sublet or underlet the property.

Tenant shall not make any changes without written consent from the landlord.

At the completion of the agreement, tenant should return possession of the house to the owner in good, tenantable condition except for normal wear and tear.

The tenant accepts that the house is provided in Unfurnished condition, which is provided with the following fittings and fixtures:
4 Tubelights, 3 Fans, 1 Sofa, 6 Chairs, 3 Taps, 2 Basins, 1 AC, 1 TV

    '''

    trial_freeform = '''

    *If you have any outage, it's not my responsibility. I won't pay any money for loss due to it. * I have paid for cable tv as per my service level. There won't be any refund or adjustment if you don't like the content of have different choices. * Don't ask for any compensation while leaving.
    *I will pay the property & other taxes on house.*Dont smoke at my home. *You are not rented for forever, so do not expect to make this your permanent home.
    *We both will take a copy of it.
     *You don't have to pay any advance.
     * Dont smoke at my home.
    *I will increase the rent by 5% every year.
    *No pets here.
    *
    I am not responsible for any injury or damage at my place, in case of any accident.
    * Please don't keep pets here!


    '''

    templated_agreement = receive_values(trial_mhash)
    print('Template filling trial result')
    print(templated_agreement)

    agreement_with_queried_clauses = produce_with_unstructured_data(trial_unfinished_agreement, trial_freeform)
    print('Agreement updated with clauses queried using unstructured trial input')
    print(agreement_with_queried_clauses)
