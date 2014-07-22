#!/usr/bin/env python2
import sys
import os

import ckanapi
import requests

APIKEY = sys.argv[1]

ckan = ckanapi.RemoteCKAN('http://127.0.0.1:5000', apikey=APIKEY)

# Create the "Data viewer examples" dataset.
package_name = 'data-viewer-examples'
package_title = 'Data viewer examples'
try:
    print 'Creating "{package_title}" package'.format(**locals())
    package = ckan.action.package_create(name=package_name,
                                         title=package_title)
except ckanapi.ValidationError, e:
    if (e.error_dict['__type'] == 'Validation Error' and
       e.error_dict['name'] == ['That URL is already in use.']):
        print '"{package_title}" package already exists'.format(**locals())
        package = ckan.action.package_show(id=package_name)
    else:
        raise

for filename in os.listdir('example_files'):
    path = os.path.join('example_files', filename)
    extension = os.path.splitext(filename)[1][1:].upper()
    resource_name = 'Example {extension} file'.format(extension=extension)
    print 'Creating "{resource_name}" resource'.format(**locals())
    r = requests.post('http://127.0.0.1:5001/api/action/resource_create',
                      data={'package_id': package['id'],
                            'name': resource_name,
                            'format': extension,
                            'url': 'upload',  # Needed to pass validation
                            },
                      headers={'Authorization': APIKEY},
                      files=[('upload', file(path))])

    if r.status_code != 200:
        print 'Error while creating resource: {0}'.format(r.content)
        break
