tracpreferencesfromldap
=======================


**tracpreferencesfromldap** is a Trac-Plugin which loads the
Trac-Preferences **Full Name** and **E-Mail-Address** from a 
given LDAP-Server

LDAP-Settings can be provided via the **trac.ini**::

    [ldappreferences]
    server_hostname = 192.168.1.1
    server_port = 8899
    manager = cn=manager
    manager_pwd = secret
    root_dn = cn=foo,o=bar

