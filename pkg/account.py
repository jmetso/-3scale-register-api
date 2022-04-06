# file -- pkg.account.py --

import pkg.common

def create_account(name: str, username: str, password: str, email: str, service_plan_id: int, application_plan_id: int, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token,
               'org_name': name,
               'username': username,
               'email': email,
               'password': password,
               'servicePlanId': service_plan_id,
               'application_plan_id': application_plan_id }
    response = pkg.common.post_json(base_url+'/signup.json', values)
    return response['account']['id']

def account_approve(account_id: int, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token }
    response = pkg.common.put_json(base_url+'/accounts/'+str(account_id)+'/approve.json', values)
    return response['account']['id']

def update_account(account_id: int, name: str, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token,
               'org_name': name }
    response = pkg.common.put_json(base_url+'/accounts/'+str(account_id)+'.json', values)
    return response['account']['id']

def find_account_id(org_name, access_token: str, base_url: str) -> int:
    params = { 'access_token': access_token }
    response = pkg.common.get_json(base_url+'/accounts.json', params)
    for account in response['accounts']:
        if account['account']['org_name'] == org_name:
            return str(account['account']['id'])
    return '-1'

def setup_account(account_name: str, username: str, password: str, email: str, service_plan_id: int, app_plan_id: int, access_token: str, base_url: str):
    # List accounts
    params = { 'access_token': access_token }
    response = pkg.common.get_json(base_url+'/accounts.json', params)
    if len(response['accounts']) == 0:
        print('No accounts found')
        account_id = create_account(account_name, username, password, email, service_plan_id, app_plan_id, access_token, base_url)
        print('Created account with id: '+str(account_id))
        account_id = account_approve(account_id)
        print('Approved account with id: '+str(account_id))
    else:
        print(str(len(response['accounts']))+' account(s) found.')
        account_id = find_account_id(account_name, access_token, base_url)
        if account_id == '-1':
            account_id = create_account(account_name, username, password, email, service_plan_id, app_plan_id, access_token, base_url)
            print('Created account with id: '+str(account_id))
            #accountId = accountApprove(account_id)
            #print('Approved account with id: '+str(account_id))
        else:
            account_id = update_account(account_id, account_name, access_token, base_url)
            print('Updated account with id: '+str(account_id))

