from proxyserver.settings.basic import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '64)3d-7+yo_j6)89lc1%0#zu8s+32=ty062#8kxtjb8@5f+9ks'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


JWT_AUTH['JWT_PUBLIC_KEY'] = open('proxyserver/settings/dev.key.pub').read()
