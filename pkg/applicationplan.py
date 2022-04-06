# file -- pkg.applicationplan.py --

import pkg.common

def create_application_plan(service_id: int, name: str, approval_required: bool, cost_per_month: float, setup_fee: float, trial_period_days: int, end_user_required: bool, state_event: str, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token,
               'name': name,
               'approval_required': approval_required,
               'cost_per_month': cost_per_month,
               'setup_fee': setup_fee,
               'trial_period_days': trial_period_days,
               'end_user_required': end_user_required,
               'system_name': 'plan-'+name.lower(),
               'state_event': state_event }
    response = pkg.common.post_json(base_url+'/services/'+str(service_id)+'/application_plans.json', values)
    return response['application_plan']['id']

def set_default_application_plan(service_id: int, plan_id: int, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token }
    response = pkg.common.put_json(base_url+'/services/'+str(service_id)+'/application_plans/'+str(plan_id)+'/default.json', values)
    return response['application_plan']['id']

def update_application_plan(service_id: int, plan_id: int, name: str, approval_required: bool, cost_per_month: float, setup_fee: float, trial_period_days: int, end_user_required: bool, state_event: str, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token,
               'state_event': 'hide' }
    response = pkg.common.put_json(base_url+'/services/'+str(service_id)+'/application_plans/'+str(plan_id)+'.json', values)
    values = { 'access_token': access_token,
               'name': name,
               'approval_required': approval_required,
               'cost_per_month': cost_per_month,
               'setup_fee': setup_fee,
               'trial_period_days': trial_period_days,
               'end_user_required': end_user_required,
               'system_name': 'plan-'+name.lower(),
               'state_event': state_event }
    response = pkg.common.put_json(base_url+'/services/'+str(service_id)+'/application_plans/'+str(plan_id)+'.json', values)
    return response['application_plan']['id']

def setup_application_plan(service_id: int, service_name: str, require_approval: bool, require_end_user: bool, application_plan_status: str, access_token: str, base_url: str) -> int:
    # List application plans
    params = { 'access_token': access_token }
    response = pkg.common.get_json(base_url+'/services/'+str(service_id)+'/application_plans.json', params)
    if len(response['plans']) == 0:
        print('No application plans found')
        app_plan_id = create_application_plan(service_id, service_name+'-default', require_approval, 0, 0, 0, require_end_user, application_plan_status, access_token, base_url)
        print('Created application plan with id: '+str(app_plan_id))
        app_plan_id = set_default_application_plan(service_id, app_plan_id, access_token, base_url)
        print('Set application plan with id: '+str(app_plan_id)+' to default')
    else:
        print(str(len(response['plans']))+' application plan(s) found')
        for plan in response['plans']:
            if plan['application_plan']['name'] == service_name+'-default':
                app_plan_id = update_application_plan(service_id, plan['application_plan']['id'], service_name+'-default', require_approval, 0, 0, 0, require_end_user, application_plan_status, access_token, base_url)
                print('Updated application plan with id: '+str(app_plan_id))
                app_plan_id = set_default_application_plan(service_id, app_plan_id, access_token, base_url)
                print('Set application plan with id: '+str(app_plan_id)+' to default')

    return app_plan_id
