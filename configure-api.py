#!/usr/bin/env python3

import pkg.common
import pkg.backend
import pkg.product
import pkg.applicationplan
import pkg.account
import pkg.activedoc
import pkg.application
from os.path import exists
import json

BACKEND_NAME='janne-backend'
BACKEND_DESCRIPTION='Janne\'s backend'
PRIVATE_ENDPOINT='<protocol>://<backend-host-name>:<port>'
TOKEN_NAME='script-token'
ACCESS_TOKEN='<3scale-access-token-with-rw-to-account-management>'
BASE_URL='https://<3scale-tenant-admin-host>/admin/api'
SERVICE_NAME='janne'
SERVICE_DESCRIPTION="Janne's service"
SERVICE_DEPLOYMENT='hosted' # 'hosted' for APIcast hosted, 'self_managed' for APIcast Self-managed, 'service_mesh_istio' for Istio service mesh option
BACKEND_VERSION='2' # Authentication mode: '1' for API key, '2' for App Id / App Key, 'oidc' for OpenID Connect
EMAIL='example@example.com'
REQUIRE_APPROVAL='true' # 'true' or 'false'
REQUIRE_END_USER='false'
APPLICATION_PLAN_STATUS='publish' # 'publish' or 'hide
ACCOUNT_NAME='Janne Enterprises'
USERNAME='janne'
PASSWORD='password'
BACKEND_PATH='/'
APP_ID='appId'
APP_KEY='appKey'
PROD_PUBLIC_BASE_URL='https://<production-api-gw-host-name>:443' # accepted style is <protocol>://<host>:<port>
STAGE_PUBLIC_BASE_URL='https://<staging-api-gw-host-name>:443' # accepted style is <protocol>://<host>:<port>
CREDENTIALS_LOCATION='headers' # headers, query, authorization

# Data could be for example divided into following structures and the processed by the functions
backends = [{ 'name': 'janne-backend',
            'description': "Janne's backend",
            'privateEndpoint': '<private-service-url>' }]

service = { 'name': 'janne',
            'description': "Janne's service",
            'deployment': 'hosted',
            'authenticationMode': '2',
            'appId': 'appId',
            'appKey': 'appKey',
            'productionUrl': '<production-gw-url>',
            'stagingUrl': '<staging-gw-url>',
            'credentialsLocation': 'headers',
            'applicationPlanStatus': 'publish',
            'backend': [{ 'name': 'janne-backend', 'path': '/ '}] }

account = { 'name': 'Janne Enterprises',
            'adminUsername': 'janne',
            'adminPassword': 'password',
}

def read_json_file(filename):
    if(exists(filename)):
        f = open(filename)
        return json.load(f)

def main_v2():
    # read backend configuration
    backends = read_json_file("backends.json")
    print(backends)
    backend_ids = []
    for backend in backends:
        print(backend)
        backend_id = pkg.backend.setup_backend(backend['name'], backend['description'], backend['private_endpoint'], ACCESS_TOKEN, BASE_URL)
        print(backend_id)
        backend_ids.append(backend_id)

    print(backend_ids)
    for backend_id in backend_ids:
        pkg.product.update_product_backend(service['product_id'], backend_id, backend_path, access_token, base_url)

    # TODO

def main():
    backend_id = pkg.backend.setup_backend(BACKEND_NAME, BACKEND_DESCRIPTION, PRIVATE_ENDPOINT, ACCESS_TOKEN, BASE_URL)
    service = pkg.product.setup_product(SERVICE_NAME, SERVICE_DESCRIPTION, EMAIL, SERVICE_DEPLOYMENT, BACKEND_VERSION, REQUIRE_APPROVAL, APPLICATION_PLAN_STATUS, PROD_PUBLIC_BASE_URL, STAGE_PUBLIC_BASE_URL, CREDENTIALS_LOCATION, APP_ID, APP_KEY, ACCESS_TOKEN, BASE_URL)
    pkg.product.update_product_backend(service['product_id'], backend_id, BACKEND_PATH, ACCESS_TOKEN, BASE_URL)
    pkg.activedoc.setup_active_doc(service['product_id'], 'janne-v-0-1-0', 'Janne v0.1', 'openapi.json', ACCESS_TOKEN, BASE_URL, 'true', 'true')
    application_plan_id = pkg.applicationplan.setup_application_plan(service['product_id'], SERVICE_NAME, REQUIRE_APPROVAL, REQUIRE_END_USER, APPLICATION_PLAN_STATUS, ACCESS_TOKEN, BASE_URL)
    pkg.account.setup_account(ACCOUNT_NAME, USERNAME, PASSWORD, EMAIL, service['product_plan_id'], application_plan_id, ACCESS_TOKEN, BASE_URL)
    pkg.application.create_developer_account_appliction_for_testing(application_plan_id, SERVICE_NAME, APP_ID, APP_KEY, REQUIRE_APPROVAL, ACCESS_TOKEN, BASE_URL)

    # output backend status
    params = { 'access_token': ACCESS_TOKEN }
    response = pkg.common.get_json(BASE_URL+'/backend_apis/'+str(backend_id)+'.json', params)
    print('Backend: \n'+response.text+'\n')

    # output service status
    response = pkg.common.get_json(BASE_URL+'/services/'+str(service['product_id'])+'.json', params)
    print('Service: \n'+response.text+'\n')

main()
