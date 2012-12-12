#  -*- coding: utf-8 -*-
#
#  File Name: file.py
#  Creation Date: 2012 Jul 24
#  Last Modified: 2012 Dez 12

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
                'root_dn'           : 'o=%s' % self.env.config.get('ldappreferences', 'root_dn'),
                'ldapdelete_cmd'    : 'ldapdelete -x -h %(host)s -p %(port)s -D "%(manager)s" -w %(manpwd)s',
                'ldappasswd_cmd'    : 'ldappasswd -x -h %(host)s -p %(port)s -D "%(manager)s" -w %(manpwd)s -s %(newpwd)s %(uid)s'
                }
        ldap= wcldapadmin.WcLdapCmd(ldapdata)
        dn = "uid=%s," % authname
        dn_elements = self.env.config.get('ldappreferences', 'dn').split(',')
        for x in dn_elements:
            dn += "%s=%s," % (x, self.env.config.get('ldappreferences', x))
        dn = dn.strip(',')
        return ldap.getUser(dn)

    def update_settings(self, authname, field, value):
        @with_transaction(self.env)
        def _insertTestCase(db):
            c = db.cursor()
            sql = "INSERT INTO \"session_attribute\" VALUES('%s',1,'%s','%s');" % (authname, field, value)
            c.execute(sql)

    def is_update_needed(self, authname, field):
        """Check if the setting is empty
        """
        stmt  = "SELECT value FROM session_attribute WHERE sid = '%s' and name = '%s' LIMIT 1;" % (authname, field)
        dbs = []
        @with_transaction(self.env)
        def _getTestCases(db):
            c= db.cursor()

            c.execute(stmt)
            dbs.append(c.fetchone())
        ret = None
        if len(dbs) < 1 or \
                dbs.pop() == None:
            #val = dbs.pop()[0]
            ret = True # update is needed
        else:
            ret = False
        return ret

    # IRequestHandler methods
    def match_request(self, req):
        if req.authname != 'anonymous':
            if self.is_update_needed(req.authname, 'name'):
                data = self.get_ldap_data(req.authname)
                self.update_settings(req.authname, 'name', data.get('cn'))
            if self.is_update_needed(req.authname, 'email'):
                data = self.get_ldap_data(req.authname)
                self.update_settings(req.authname, 'email', data.get('mail'))
