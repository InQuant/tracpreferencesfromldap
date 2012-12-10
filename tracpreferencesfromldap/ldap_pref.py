#  -*- coding: utf-8 -*-
#
#  File Name: file.py
#  Creation Date: 2012 Jul 24
#  Last Modified: 2012 Dez 10

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
from trac.util.html import html
from trac.web import IRequestHandler
from trac.web.chrome import INavigationContributor

class LdapPrefPlugin(Component):
    implements(INavigationContributor, IRequestHandler)

    # INavigationContributor methods
    def get_active_navigation_item(self, req):
        return 'helloworld'
    def get_navigation_items(self, req):
        yield ('mainnav', 'helloworld',
            html.A('Hello world', href= req.href.helloworld()))

    # IRequestHandler methods
    def match_request(self, req):
        return req.path_info == '/helloworld'
    def process_request(self, req):
        content = 'Hello World!'
        req.send_response(200)
        req.send_header('Content-Type', 'text/plain')

