# file -- pkg.backend.py --

from email.mime import base
import pkg.common

def create_backend(backend_name: str, description: str, private_endpoint: str, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token,
               'name': backend_name,
               'system_name': backend_name.lower(),
               'description': description,
               'private_endpoint': private_endpoint }
    result = pkg.common.post_json(base_url+'/backend_apis.json', values)
    return result['backend_api']['id']

def update_backend(backend_name: str, backend_id: int, description: str, private_endpoint: str, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token,
               'name': backend_name,
               'description': description,
               'private_endpoint': private_endpoint }
    result = pkg.common.put_json(base_url+'/backend_apis/'+str(backend_id)+'.json', values)
    return result['backend_api']['id']

def get_backend_metrics_id(backend_id: int, name: str, access_token: str, base_url: str):
    params = { 'access_token': access_token }
    response = pkg.common.get_json(base_url+'/backend_apis/'+str(backend_id)+'/metrics.json', params)
    for metric in response['metrics']:
        if metric['metric']['friendly_name'] == name:
            return str(metric['metric']['id'])
    return -1

def create_backend_mapping_rule_to_metric(backend_id: int, method: str, pattern: str, delta: str, metric_id: int, access_token: str, base_url: str, position = 1, last = 'true') -> int:
    values = { 'access_token': access_token,
               'http_method': method,
               'pattern': pattern,
               'delta': delta,
               'metric_id': metric_id,
               'position': position,
               'last': last }
    result = pkg.common.post_json(base_url+'/backend_apis/'+str(backend_id)+'/mapping_rules.json', values)
    return result['mapping_rule']['id']

def update_backend_mapping_rule_to_metric(backend_id: int, rule_id: int, method: str, pattern: str, delta: int, metric_id: int, access_token: str, base_url: str, position = 1, last = 'true') -> int:
    values = { 'access_token': access_token,
               'http_method': method,
               'pattern': pattern,
               'delta': delta,
               'metric_id': metric_id,
               'position': position,
               'last': last }
    response = pkg.common.put_json(base_url+'/backend_apis/'+str(backend_id)+'/mapping_rules/'+str(rule_id)+'.json', values)
    return response['mapping_rule']['id']

def create_backend_method(backend_id: int, metric_id: int, name: str, unit, access_token: str, base_url: str, description='') -> int:
    values = { 'access_token': access_token,
               'friendly_name': name,
               'system_name': name.lower(),
               'unit': unit,
               'description': description }
    response = pkg.common.post_json(base_url+'/backend_apis/'+str(backend_id)+'/metrics/'+str(metric_id)+'/methods.json', values)
    return response['method']['id']

def update_backend_method(backend_id: int, metric_id: int, method_id: int, name: str, unit, access_token: str, base_url: str, description='') -> int:
    values = { 'access_token': access_token,
               'friendly_name': name,
               'system_name': name.lower(),
               'unit': unit,
               'description': description }
    response = pkg.common.put_json(base_url+'/backend_apis/'+str(backend_id)+'/metrics/'+str(metric_id)+'/methods/'+str(method_id)+'.json', values)
    method_id = str(response['method']['id'])
    #print('Backend method id: '+rule_id)
    return method_id

def check_backend_exists(backend_name: str, access_token: str, base_url: str) -> int:
    params = { 'access_token': access_token }
    backends = pkg.common.get_json(base_url+'/backend_apis.json', params)
    for api in backends['backend_apis']:
        if api['backend_api']['name'] == backend_name:
            return api['backend_api']['id']
    return -1

def set_mapping_rule(backend_id: int, metric_hits_id: int, pattern: str, http_method: str, access_token: str, base_url: str):
    params = { 'access_token': access_token }
    response = pkg.common.get_json(base_url+'/backend_apis/'+str(backend_id)+'/mapping_rules.json', params)
    if len(response['mapping_rules']) == 0:
        print('No mapping rules found')
        # Add <http_method>, <pattern> mapping rule to Hits
        mapping_rule_id = create_backend_mapping_rule_to_metric(backend_id, http_method, pattern, 1, metric_hits_id, access_token, base_url)
        print('Created mapping rule with id: '+str(mapping_rule_id))
    else:
        print(str(len(response['mapping_rules']))+' mapping rule(s) found')
        for rule in response['mapping_rules']:
            if rule['mapping_rule']['pattern'] == pattern and rule['mapping_rule']['http_method'] == http_method:
                # update rule to match config
                mapping_rule_id = update_backend_mapping_rule_to_metric(backend_id, rule['mapping_rule']['id'], http_method, pattern, 1, metric_hits_id, access_token, base_url, rule['mapping_rule']['position'], rule['mapping_rule']['last'])
                print('Updated mapping rule with id: '+str(mapping_rule_id))

def set_backend_method(backend_id: int, metric_hits_id: int, name: str, unit, access_token: str, base_url: str):
    params = { 'access_token': access_token }
    response = pkg.common.get_json(base_url+'/backend_apis/'+str(backend_id)+'/metrics/'+str(metric_hits_id)+'/methods.json', params)
    if len(response['methods']) == 0:
        print('No methods found')
        print('Created backend method with id: '+create_backend_method(backend_id, metric_hits_id, name, unit, access_token, base_url))
    else:
        print(str(len(response['methods']))+' method(s) found')
        for method in response['methods']:
            if method['method']['friendly_name'] == 'test':
                print('Updated backend method with id: '+update_backend_method(backend_id, metric_hits_id, method['method']['id'], name, unit, access_token, base_url))


def setup_backend(backend_name: str, backend_description: str, private_endpoint: str, access_token: str, base_url: str) -> int:
    backend_id = check_backend_exists(backend_name, access_token, base_url)

    if backend_id > -1:
        backend_id = update_backend(backend_name, backend_id, backend_description, private_endpoint, access_token, base_url)
        print('Updated backend with id: '+str(backend_id))
    else:
        backend_id = create_backend(backend_name, backend_description, private_endpoint, access_token, base_url)
        print('Created backend with id: '+str(backend_id))

    metric_hits_id = get_backend_metrics_id(backend_id, 'Hits', access_token, base_url)
    print('Hit metrics id: '+metric_hits_id)

    set_mapping_rule(backend_id, metric_hits_id, '/', 'GET', access_token, base_url)
    set_mapping_rule(backend_id, metric_hits_id, '/', 'POST', access_token, base_url)

    set_backend_method(backend_id, metric_hits_id, 'test', 1, access_token, base_url)

    return backend_id
