# file -- pkg.application.py --

import pkg.common

def create_application(account_id: int, plan_id: int, name: str, description: str, access_token: str, base_url: str, userKey = '', key_id = '', keyValue = '', redirectUrl = '') -> int:
    values = { 'access_token': access_token,
               'plan_id': plan_id,
               'name': name,
               'description': description }
    if userKey != '':
        values['user_key'] = userKey
    if key_id != '':
        values['application_id'] = key_id
    if keyValue != '':
        values['application_key'] = keyValue
    if redirectUrl != '':
        values['redirect_url'] = redirectUrl
    response = pkg.common.post_json(base_url+'/accounts/'+str(account_id)+'/applications.json', values)
    return response['application']['id']

def accept_application(account_id: int, application_id: int, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token }
    response = pkg.common.put_json(base_url+'/accounts/'+str(account_id)+'/applications/'+str(application_id)+'/accept.json', values)
    return response['application']['id']

def update_app_key(account_id: int, application_id: int, key_value: str, access_token: str, base_url: str):
    values = { 'access_token': access_token }
    response = pkg.common.get_json(base_url+'/accounts/'+str(account_id)+'/applications/'+str(application_id)+'/keys.json', values)
    keyFound = False
    if len(response['keys']) > 0:
        for key in response['keys']:
            if key['key']['value'] == key_value:
                keyFound = True # nothing needs to be done
        if keyFound == False:
            values['key'] = response['keys'][0]['key']['value']
            response = pkg.common.delete(base_url+'/accounts/'+str(account_id)+'/applications/'+str(application_id)+'/keys.json', values)
    else:
        values['key'] = key_value
        response = pkg.common.post_json(base_url+'/accounts/'+str(account_id)+'/applications/'+str(application_id)+'/keys.json', values)

def update_application(account_id: int, application_id: int, name: str, description: str, access_token: str, base_url: str, userKey = '', key_id = '', keyValue = '', redirectUrl=''):
    values = { 'access_token': access_token,
               'name': name,
               'description': description }
    if redirectUrl != '':
        values['redirect_url'] = redirectUrl
    response = pkg.common.put_json(base_url+'/accounts/'+str(account_id)+'/applications/'+str(application_id)+'.json', values)
    if(keyValue != ''):
        update_app_key(account_id, application_id, keyValue, access_token, base_url)
        print('Updated app key for application with id: '+str(application_id))
    return response['application']['id']

def create_developer_account_appliction_for_testing(application_plan_id: int, service_name: str, app_id: str, app_key: str, require_approval: bool, access_token: str, base_url: str):
    developer_account_id = pkg.account.find_account_id('Developer', access_token, base_url)
    params = { 'access_token': access_token }
    response = pkg.common.get_json(base_url+'/accounts/'+developer_account_id+'/applications.json', params)
    if len(response['applications']) == 0:
        print('No applications found')
    else:
        print(str(len(response['applications']))+' application(s) found.')
        applicationFound = False
        for application in response['applications']:
            if application['application']['name'] == 'Developer '+service_name+' App':
                applicationFound = True
                application_id = update_application(developer_account_id, application['application']['id'], 'Developer '+service_name+' App', 'Developer account application for '+service_name, access_token, base_url, key_id=app_id, keyValue=app_key)
                print('Updated application with id: '+str(application_id))
        if applicationFound == False:
            application_id = create_application(developer_account_id, application_plan_id, 'Developer '+service_name+' App', 'Developer account application for '+service_name, access_token, base_url, key_id=app_id, keyValue=app_key)
            print('Created application with id: '+str(application_id))
            if require_approval:
                application_id = accept_application(developer_account_id, application_id, access_token, base_url)
                print('Approved application with id: '+str(application_id))
