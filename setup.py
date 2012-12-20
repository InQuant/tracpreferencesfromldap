from setuptools import setup, find_packages
import sys, os

version = '1.1'

setup(name='tracpreferencesfromldap',
      version=version,
      description="Load 'Full Name' and 'E-Mail-Address' from LDAP",
      long_description="""This Plugin connects to a LDAP-Server that is configured in the trac.ini. It looks up the Full Name and the E-Mail-Address of a user who is identified by the Trac-Login-Name.
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='trac, ldap',
      author='Rainer Hihn',
      author_email='rainer.hihn@inquant.de',
      url='www.inquant.de',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={'trac.plugins': 'tracpreferencesfromldap = tracpreferencesfromldap.ldap_pref'}
      )
