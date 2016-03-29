#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuki Furuta <furushchev@jsk.imi.i.u-tokyo.ac.jp>

import os
import pprint
import urlparse
import json
import requests

BINTRAY_BASE_URL=os.getenv('BINTRAY_BASE_URL', 'https://api.bintray.com')
BINTRAY_REPOSITORY=os.getenv('BINTRAY_REPOSITORY', 'ros-ios/cocoapods')
BINTRAY_USER=os.getenv('BINTRAY_USER', 'furushchev')
BINTRAY_API_KEY=os.getenv('BINTRAY_API_KEY', '8279544003b24122d63c35985e6a482f9f30cf2b')

class BintrayHandler(object):
    def __init__(self, repo):
        if repo in self.list_repositories():
            print 'found', repo
            self.subject = repo.split('/')[0]
            self.repo = repo.split('/')[1]
        else:
            raise BaseException("%s not found" % repo)

    def request(self, url, method='GET', **params):
        full_url = os.path.join(BINTRAY_BASE_URL, url)
        res = requests.request(method, full_url,
                               auth=(BINTRAY_USER, BINTRAY_API_KEY),
                               verify=True,
                               **params)
        res.raise_for_status()
        return res.json()

    def list_repositories(self):
        url = os.path.join('repos', BINTRAY_USER)
        return [r['owner'] + '/' + r['name'] for r in self.request(url)]

    def list_packages(self):
        url = os.path.join('repos', self.subject, self.repo, 'packages')
        return [r['name'] for r in self.request(url)]

    def create_package(self, params):
        if 'vcs_url' not in params or 'licenses' not in params:
            raise BaseException('licenses and vcs_url are mandatory')
        url = os.path.join('packages', self.subject, self.repo)
        data = json.dumps(params)
        return self.request(url, 'POST', data=json.dumps(params))

    def delete_package(self, pkg_name):
        res = self.request(os.path.join('packages', self.subject, self.repo, pkg_name), 'DELETE')
        if 'message' in res and res['message'] == 'success':
            return True
        else:
            return False

    def find_package(self, pkg_name):
        url = os.path.join('search', 'packages')
        res = self.request(url,
                           params={'name': pkg_name,
                                   'subject': self.subject,
                                   'repo': self.repo})
        if pkg_name in [r['name'] for r in res]:
            return True
        else:
            return False

    def upload_file(self, bin_path, dest_path, pkg_name, version, publish=True, override=True):
        url = os.path.join('content', self.subject, self.repo, pkg_name, version, dest_path)
        res = None
        with open(bin_path, 'rb') as f:
            res = self.request(url, 'PUT',
                               params={'publish': '1' if publish else '0',
                                       'override': '1' if override else '0'},
                               files={os.path.basename(bin_path): f})
        if 'message' in res and res['message'] == 'success':
            return True
        else:
            return False


if __name__ == '__main__':
    b = BintrayHandler(BINTRAY_REPOSITORY)
    b.list_repositories()
    print b.delete_package('test')
    print b.create_package({'name': 'test',
                            'desc': 'test desc',
                            'licenses': ['MIT'],
                            'vcs_url': 'https://github.com/furushchev/test'})
    print b.list_packages()
    print b.find_package('test')
    print b.upload_binary("/tmp/test.zip", 'test.zip', "test", "0.0.0")
