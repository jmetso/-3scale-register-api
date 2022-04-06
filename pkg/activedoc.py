# file -- pkg.activedoc.py --

import pkg.common
from os.path import exists

def create_active_doc(service_id, name, body, access_token: str, base_url: str, description = '', published = '', skip_swagger_validations = '') -> int:
    values = { 'access_token': access_token,
               'name': name,
               'service_id': service_id,
               'body': body }
    if description != '':
        values['description'] = description
    if published != '':
        values['published'] = published
    if skip_swagger_validations != '':
        values['skip_swagger_validations'] = skip_swagger_validations
    response = pkg.common.post_json(base_url+'/active_docs.json', values)
    return response['api_doc']['id']

def update_active_doc(service_id, active_doc_id, name, body, access_token: str, base_url: str, description = '', published = '', skip_swagger_validations = '') -> int:
    values = { 'access_token': access_token,
               'name': name,
               'service_id': service_id,
               'body': body }
    if description != '':
        values['description'] = description
    if published != '':
        values['published'] = published
    if skip_swagger_validations != '':
        values['skip_swagger_validations'] = skip_swagger_validations
    response = pkg.common.put_json(base_url+'/active_docs/'+str(active_doc_id)+'.json', values)
    assert service_id == response['api_doc']['id']
    return response['api_doc']['id']

def setup_active_doc(service_id: str, doc_name: str, doc_description: str, filename: str, access_token: str, base_url: str, publish='', skip_swagger_validations=''):
    # List active docs
    params = { 'access_token': access_token }
    response = pkg.common.get_json(base_url+'/active_docs.json', params)
    # Create active doc if not exists
    activeDocFound = False
    for apiDoc in response['api_docs']:
        if apiDoc['api_doc']['service_id'] == service_id and apiDoc['api_doc']['name'] == doc_name:
            activeDocFound = True
            if(exists(filename)):
                with open(filename, 'r') as apifile:
                    data = apifile.read()
                print('Updated api doc with id: '+update_active_doc(service_id, apiDoc['api_doc']['id'], doc_name, data, access_token, base_url, doc_description, publish, skip_swagger_validations))
            else:
                print('OpenAPI doc file not found, skipping.')

    if activeDocFound == False:
        print('Active doc not found')
        if(exists(filename)):
            with open(filename, 'r') as apifile:
                data = apifile.read()
                print('Created api doc with id: '+create_active_doc(service_id, doc_name, data, access_token, base_url, doc_description, publish, skip_swagger_validations))
        else:
            print('OpenAPI doc file not found, skipping.')
