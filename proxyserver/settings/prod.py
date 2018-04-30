from proxyserver.settings.basic import *

JWT_AUTH['JWT_PUBLIC_KEY'] = open('proxyserver/settings/prod.key.pub').read()
