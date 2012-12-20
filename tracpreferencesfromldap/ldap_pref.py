#  -*- coding: utf-8 -*-
#
#  File Name: file.py
#  Creation Date: 2012 Jul 24
#  Last Modified: 2012 Dez 20

#  Copyright (c) 2003-2012 InQuant GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


__author__ = 'Rainer Hihn <rainer.hihn@inquant.de>'
__docformat__ = 'plaintext'

# vim: set ft=python ts=4 sw=4 expandtab :
from trac.core import *
from trac.web import IRequestHandler
from trac.db import with_transaction
from trac.web.session import Session

import wcldapadmin

class LdapPrefPlugin(Component):
    implements(IRequestHandler)

    def __init__(self):
        pass

    def get_ldap_data(self, authname):
        ldapdata = {
                'server_host_name'  : self.env.config.get('ldappreferences', 'server_hostname'),
                'server_port'       : self.env.config.get('ldappreferences', 'server_port'),
                'manager'           : self.env.config.get('ldappreferences', 'manager'),
                'manager_pwd'       : self.env.config.get('ldappreferences', 'manager_pwd'),
                'ldapadd_cmd'       : 'ldapadd -x -h %(host)s -p %(port)s -D "%(manager)s" -w %(manpwd)s',
                'ldapmodify_cmd'    : 'ldapmodify -x -h %(host)s -p %(port)s -D "%(manager)s" -w %(manpwd)s',
                'ldapsearch_cmd'    : 'ldapsearch -x -h %(host)s -p %(port)s -D "%(manager)s" -w %(manpwd)s',
                'root_dn'           : self.env.config.get('ldappreferences', 'root_dn'),
                'ldapdelete_cmd'    : 'ldapdelete -x -h %(host)s -p %(port)s -D "%(manager)s" -w %(manpwd)s',
                'ldappasswd_cmd'    : 'ldappasswd -x -h %(host)s -p %(port)s -D "%(manager)s" -w %(manpwd)s -s %(newpwd)s %(uid)s'
                }
        try:
            ldap = wcldapadmin.WcLdapCmd(ldapdata)
        except wcldapadmin.WcLdapCmdException, wce:
            self.log.error("Ldap Error: %s" % wce)
            return None

        search_filter= '(uid=%s)' % authname
        result = []
        result = ldap.searchUsers(search_filter=search_filter, keys= ['cn','uid','mail','dn','sn','givenName'])
        if len(result) > 0:
            self.log.debug("Found LDAP Results! Updating Data.")
            return result.pop()
        else:
            self.log.debug("No LDAP Results! Not updating antything")
            return None

    def update_settings(self, req, field, value):
        session = Session(self.env, req)
        session[field] = value
        session.save()

    def is_update_needed(self, req, field):
        """Check if the setting is empty
        """
        self.log.debug("Field: %s" % field)
        session = Session(self.env, req)
        if field in session:
            return False
        else:
            return True

    # IRequestHandler methods
    def match_request(self, req):
        uid = req.authname
        if uid == 'anonymous':
            self.log.debug("Anonymous User - Not getting any Preferences")
            return
        self.log.debug("Logged-in User. Checking if an Update is needed")
        if self.is_update_needed(req, 'name') or self.is_update_needed(req, 'email'):
            self.log.debug("Trying to fetch LDAP-Data")
            data = self.get_ldap_data(uid)
            if data == None:
                return
            if 'cn' in data:
                if data.get('cn'):
                    if data.get('sn') and data.get('givenName'):
                        self.update_settings(req, 'name', "%s %s" % (data.get('sn'), data.get('givenName')))
                    else:
                        self.update_settings(req, 'name', data.get('cn'))
            if 'mail' in data:
                if data.get('mail'):
                    self.update_settings(req, 'email', data.get('mail'))
