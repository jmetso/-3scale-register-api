# file -- pkg.product.py --

import pkg.common

def create_service(name: str, description: str, deployment_option: str, backend_version: str, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token,
               'name': name,
               'description': description,
               'deployment_option': deployment_option,
               'backend_version': backend_version,
               'system_name': 'product-'+name.lower() }
    response = pkg.common.post_json(base_url+'/services.json', values)
    return response['service']['id']

def update_service(service_id: int, name: str, description: str, support_email: str, deployment_option: str, backend_version: int, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token,
               'name': name,
               'description': description,
               'support_email': support_email,
               'deployment_option': deployment_option,
               'backend_version': backend_version }
    response = pkg.common.put_json(base_url+'/services/'+str(service_id)+'.json', values)
    return response['service']['id']

def create_service_plan(service_id: int, name: str, approval_required: str, state_event: str, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token,
               'name': name,
               'approval_required': approval_required,
               'system_name': name.lower(),
               'state_event': state_event }
    response = pkg.common.json_post(base_url+'/services/'+str(service_id)+'/service_plans.json', values)
    return response['service_plan']['id']

def set_default_service_plan(service_id: int, plan_id: int, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token }
    response = pkg.common.put_json(base_url+'/services/'+str(service_id)+'/service_plans/'+str(plan_id)+'/default.json', values)
    return response['service_plan']['id']


def update_service_plan(service_id: int, plan_id: int, name: str, approval_required: str, state_event: str, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token,
               'state_event': 'hide' }
    response = pkg.common.put_json(base_url+'/services/'+str(service_id)+'/service_plans/'+str(plan_id)+'.json', values)
    values = { 'access_token': access_token,
               'name': name,
               'approval_required': approval_required,
               'system_name': name.lower(),
               'state_event': state_event }
    response = pkg.common.put_json(base_url+'/services/'+str(service_id)+'/service_plans/'+str(plan_id)+'.json', values)
    return response['service_plan']['id']

def get_service_metrics_id(service_id: int, name: str, access_token: str, base_url: str) -> int:
    params = { 'access_token': access_token }
    response = pkg.common.get_json(base_url+'/services/'+str(service_id)+'/metrics.json', params)
    for metric in response['metrics']:
        if metric['metric']['friendly_name'] == name:
            return metric['metric']['id']
    return -1

def create_service_method(service_id: int, metric_id: int, name: str, unit: str, access_token: str, base_url: str, description='') -> int:
    values = { 'access_token': access_token,
               'friendly_name': name,
               'system_name': name.lower(),
               'unit': unit,
               'description': description }
    response = pkg.common.post_json(base_url+'/services/'+str(service_id)+'/metrics/'+str(metric_id)+'/methods.json', values)
    return response['method']['id']

def update_service_method(service_id: int, metric_id: int, method_id: int, name: str, unit: str, access_token: str, base_url: str, description='') -> int:
    values = { 'access_token': access_token,
               'friendly_name': name,
               'system_name': name.lower(),
               'unit': unit,
               'description': description }
    response = pkg.common.put_json(base_url+'/services/'+str(service_id)+'/metrics/'+str(metric_id)+'/methods/'+str(method_id)+'.json', values)
    return response['method']['id']

def create_service_mapping_rule_to_metric(service_id: int, method: str, pattern: str, delta: int, metric_id: int, access_token: str, base_url: str, position = 1, last = 'true') -> int:
    values = { 'access_token': access_token,
               'http_method': method,
               'pattern': pattern,
               'delta': delta,
               'metric_id': metric_id,
               'position': position,
               'last': last }
    response = pkg.common.post_json(base_url+'/services/'+str(service_id)+'/proxy/mapping_rules.json', values)
    return response['mapping_rule']['id']

def update_service_mapping_rule_to_metric(service_id: int, rule_id: int, method: str, pattern: str, delta: int, metric_id: int, access_token: str, base_url: str, position = 1, last = 'true'):
    values = { 'access_token': access_token,
               'http_method': method,
               'pattern': pattern,
               'delta': delta,
               'metric_id': metric_id,
               'position': position,
               'last': last }
    response = pkg.common.put_json(base_url+'/services/'+str(service_id)+'/proxy/mapping_rules/'+str(rule_id)+'.json', values)
    return response['mapping_rule']['id']

def update_proxy_config(service_id: int, access_token: str, base_url: str, production_endpoint='', sandbox_endpoint='', credentials_location='', auth_app_key='', auth_app_id='', auth_user_key='', oidc_issuer_endpoint='', oidc_issuer_type='') -> int:
    values = { 'access_token': access_token }
    if production_endpoint != '':
        values['endpoint'] = production_endpoint
    if sandbox_endpoint != '':
        values['sandbox_endpoint'] = sandbox_endpoint
    if credentials_location != '':
        values['credentials_location'] = credentials_location
    if auth_app_key != '':
        values['auth_app_key'] = auth_app_key
    if auth_app_id != '':
        values['auth_app_id'] = auth_app_id
    if auth_user_key != '':
        values['auth_user_key'] = auth_user_key
    if oidc_issuer_endpoint != '':
        values['oidc_issuer_endpoint'] = oidc_issuer_endpoint
    if oidc_issuer_type != '':
        values['oidc_issuer_type'] = oidc_issuer_type
    response = pkg.common.patch_json(base_url+'/services/'+str(service_id)+'/proxy.json', values)
    return response['proxy']['service_id']

def deploy_proxy_config(service_id: int, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token }
    response = pkg.common.post_json(base_url+'/services/'+str(service_id)+'/proxy/deploy.json', values)
    return response['proxy']['service_id']

def promote_proxy_config(service_id: int, environment: str, version: int, to: int, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token,
               'to': to }
    response = pkg.common.post_json(base_url+'/services/'+str(service_id)+'/proxy/configs/'+environment+'/'+str(version)+'/promote.json', values)
    return response['proxy_config']['version']

def show_latest_proxy_config(service_id: int, environment: str, access_token: str, base_url: str) -> int:
    values = { 'access_token': access_token }
    response = pkg.common.get_json(base_url+'/services/'+str(service_id)+'/proxy/configs/'+environment+'/latest.json', values)
    return response['proxy_config']['version']

def check_product_exists(product_name: str, access_token: str, base_url: str) -> int:
    params = { 'access_token': access_token }
    response = pkg.common.get_json(base_url+'/services.json', params)
    print(str(len(response['services']))+' service(s) found')
    for service in response['services']:
        if service['service']['name'] == product_name:
            return service['service']['id']
    return -1

def setup_product_plan(product_id: int, service_name: str, require_approval: bool, application_plan_status: str, access_token: str, base_url: str) -> int:
    params = { 'access_token': access_token }
    response = pkg.common.get_json(base_url+'/services/'+str(product_id)+'/service_plans.json', params)
    if len(response['plans']) == 0:
        print('No service plans found')
        product_plan_id = create_service_plan(product_id, service_name+'-default', require_approval, application_plan_status)
        print('Created service plan with id: '+str(product_plan_id))
        return product_plan_id
    else:
        print(str(len(response['plans']))+' service plan(s) found')
        servicePlanFound = False
        for plan in response['plans']:
            if plan['service_plan']['name'] == service_name+'-default':
                product_plan_id = update_service_plan(product_id, plan['service_plan']['id'], service_name+'-default', require_approval, application_plan_status, access_token, base_url)
                print('Updated service plan with id: '+str(product_plan_id))
                product_plan_id = set_default_service_plan(product_id, product_plan_id, access_token, base_url)
                print('Set service plan with id: '+str(product_plan_id)+' to default')
                servicePlanFound = True
        if servicePlanFound == False:
            product_plan_id = create_service_plan(product_id, service_name, require_approval, application_plan_status, access_token, base_url)
            print('Created service plan with id: '+str(product_plan_id))
            product_plan_id = set_default_service_plan(product_id, product_plan_id, access_token, base_url)
            print('Set service plan with id: '+str(product_plan_id)+' to default')
            return product_plan_id

def update_product_backend(product_id: int, backend_id: int, backend_path: str, access_token: str, base_url: str):
    params = { 'access_token': access_token }
    response = pkg.common.get_json(base_url+'/services/'+str(product_id)+'/backend_usages.json', params)
    if len(response) == 0:
        # add backend into service
        values = { 'access_token': access_token,
                   'backend_api_id': backend_id,
                   'path': backend_path }
        response = pkg.common.post_json(base_url+'/services/'+str(product_id)+'/backend_usages.json', values)
        print('Added backend with id '+str(backend_id)+' to service with id '+product_id)
    else:
        backendFound = False
        for backend in response:
            if backend['backend_usage']['backend_id'] == backend_id:
                values = { 'access_token': access_token,
                           'backend_api_id': backend_id,
                           'path': backend_path }
                response = pkg.common.put_json(base_url+'/services/'+str(product_id)+'/backend_usages/'+str(backend['backend_usage']['id'])+'.json', values)
                print('Updated service with id '+str(product_id))
                backendFound = True
        if backendFound == False:
            for backend in response:
                if backend['backend_usage']['path'] == backend_path:
                    values = { 'access_token': access_token }
                    response = pkg.common.delete(base_url+'/services/'+str(product_id)+'/backend_usages/'+str(backend['backend_usage']['id'])+'.json', values)
                    print('Deleted blocking backend in service with id '+str(product_id))
            values = { 'access_token': access_token,
                       'backend_api_id': backend_id,
                       'path': backend_path }
            response = pkg.common.post_json(base_url+'/services/'+str(product_id)+'/backend_usages.json', values)
            print('Added backend with id '+str(backend_id)+' to service with id '+str(product_id))

def set_product_methods(metric_hits_id: int, product_id: int, access_token: str, base_url: str):
    # list service methods
    params = { 'access_token': access_token }
    print("Hit metrics id: "+str(metric_hits_id))
    response = pkg.common.get_json(base_url+'/services/'+str(product_id)+'/metrics/'+str(metric_hits_id)+'/methods.json', params)
    if len(response['methods']) == 0:
        print('No service methods found')
        print('Created service method with id: '+create_service_method(product_id, metric_hits_id, 'test', '1'))

    else:
        print(str(len(response['methods']))+' service method(s) found')
        for method in response['methods']:
            if method['method']['friendly_name'] == 'test':
                method_id = update_service_method(product_id, metric_hits_id, method['method']['id'], 'test', '1', access_token, base_url)
                print('Updated service method with id: '+str(method_id))
                
    # map method to metrics
    params = { 'access_token': access_token }
    response = pkg.common.get_json(base_url+'/services/'+str(product_id)+'/proxy/mapping_rules.json', params)
    if len(response['mapping_rules']) == 0:
        print('No service mapping rules found')
        # Add GET /* mapping rule to Hits
        print('Created mapping rule with id: '+str(create_service_mapping_rule_to_metric(product_id, 'GET', '/', 1, metric_hits_id, access_token, base_url)))
        # Add POST /* mapping rule to Hits
        print('Created mapping rule with id: '+str(create_service_mapping_rule_to_metric(product_id, 'POST', '/', 1, metric_hits_id, 2, access_token, base_url)))
    else:
        print(str(len(response['mapping_rules']))+' service mapping rule(s) found')
        getFound = False
        postFound = False
        for rule in response['mapping_rules']:
            if rule['mapping_rule']['pattern'] == '/' and rule['mapping_rule']['http_method'] == 'GET':
                # update rule to match config
                print('Updated mapping rule with id: '+str(update_service_mapping_rule_to_metric(product_id, rule['mapping_rule']['id'], 'GET', '/', 1, metric_hits_id, access_token, base_url, rule['mapping_rule']['position'], rule['mapping_rule']['last'])))
                getFound = True
            if rule['mapping_rule']['pattern'] == '/' and rule['mapping_rule']['http_method'] == 'POST':
                # update rule to match config
                print('Updated mapping rule with id: '+str(update_service_mapping_rule_to_metric(product_id, rule['mapping_rule']['id'], 'POST', '/', 1, metric_hits_id, access_token, base_url, rule['mapping_rule']['position'], rule['mapping_rule']['last'])))
                postFound = True
        if getFound == False:
            print('Created mapping rule with id: '+str(create_service_mapping_rule_to_metric(product_id, 'GET', '/', 1, metric_hits_id, access_token, base_url)))
        if postFound == False:
            print('Created mapping rule with id: '+str(create_service_mapping_rule_to_metric(product_id, 'POST', '/', 1, metric_hits_id, 2, access_token, base_url)))

def setup_product(service_name: str, service_description: str, email: str, service_deployment: str, backend_version: int, require_approval: bool, application_plan_status: str, production_url: str, staging_url: str, credentials_location: int, auth_app_id: str, auth_app_key: str, access_token: str, base_url: str):
    product_id = check_product_exists(service_name, access_token, base_url)
    if product_id > -1:
        product_id = update_service(product_id, service_name, service_description, email, service_deployment, backend_version, access_token, base_url)
        print('Updated service with id: '+str(product_id))
    else:
        product_id = create_service(service_name, service_description, service_deployment, backend_version, access_token, base_url)
        print('Created service with id: '+str(product_id))

    # List service plans
    product_plan_id = setup_product_plan(product_id, service_name, require_approval, application_plan_status, access_token, base_url)

    # Create methods
    metric_hits_id = get_service_metrics_id(product_id, 'Hits', access_token, base_url)
    set_product_methods(metric_hits_id, product_id, access_token, base_url)

    # Setup api gateway
    update_proxy_config(product_id, access_token, base_url, production_endpoint=production_url, sandbox_endpoint=staging_url, credentials_location=credentials_location, auth_app_id=auth_app_id, auth_app_key=auth_app_key)
    print('Updated proxy config for service with id: '+str(product_id))
    deploy_proxy_config(product_id, access_token, base_url)
    print('Deployed proxy config for service with id: '+str(product_id))
    latestProxyConfigVersion = show_latest_proxy_config(product_id, 'sandbox', access_token, base_url)
    promote_proxy_config(product_id, 'sandbox', latestProxyConfigVersion, 'production', access_token, base_url)
    print('Promoted proxy config version '+str(latestProxyConfigVersion)+' to production for service with id: '+str(product_id))
    result = { 'product_id': product_id, 'product_plan_id': product_plan_id }
    return result
