# -*- coding: utf-8 -*-
from subprocess import check_output, CalledProcessError
from setuptools import setup, find_packages

try:
    gv = check_output(['gdal-config', '--version'], universal_newlines=True).strip()
except CalledProcessError:
    gv = None

requires = [
    'pyramid==1.10.1',
    'SQLAlchemy==1.2.16',
    'transaction==2.4.0',
    'pyramid_tm==2.2.1',
    'pyramid_debugtoolbar==4.5.1',
    'pyramid_mako==1.0.2',
    'zope.sqlalchemy==1.1',
    'zope.interface==4.6.0',
    'zope.event',
    'bunch==1.0.1',
    'flufl.enum==4.1.1',
    'waitress==1.2.0',
    'pygdal' + (('==%s.*' % gv) if gv else ''),
    'psycopg2-binary==2.7.7',
    'geoalchemy2==0.5.0',
    'shapely==1.6.4.post2',
    'affine==2.2.2',
    'geojson==2.4.1',
    'pillow==5.4.1',
    'lxml==4.3.0',
    'passlib==1.7.1',
    'OWSLib==0.17.1',
    'requests[security]==2.21.0',
    'babel==2.6.0',
    'sentry-sdk==0.9.0',
    'python-magic==0.4.15',
    'backports.tempfile==1.0',
    'pip==19.2.3',  # https://github.com/pypa/pip/issues/7209
    'pyproj==2.2.2',
    'python2-secrets==1.0.5',
    'six',

    # TODO: Move to dev or test dependencies
    'pytest',
    'webtest',
    'flake8',
    'flake8-future-import',
    'modernize',
]

extras_require = {
    'dev': ['pdbpp', 'ipython']
}

entry_points = {
    'paste.app_factory': [
        'main = nextgisweb:main'
    ],

    'babel.extractors': [
        'hbs = nextgisweb.i18n.hbs:extract',
    ],

    'pytest11': [
        'nextgisweb = nextgisweb.pytest',
    ],

    'console_scripts': [
        'nextgisweb = nextgisweb.script:main',
        'nextgisweb-config = nextgisweb.script:config',
        'nextgisweb-i18n = nextgisweb.i18n.script:main',
    ],

    'nextgisweb.packages': ['nextgisweb = nextgisweb:pkginfo', ],

    'nextgisweb.amd_packages': [
        'nextgisweb = nextgisweb:amd_packages',
    ],
}

setup(
    name='nextgisweb',
    version='3.1',
    description='nextgisweb',
    long_description="",
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Framework :: Pytest",
    ],
    author='NextGIS',
    author_email='info@nextgis.com',
    url='http://nextgis.com',
    keywords='web wsgi bfg pylons pyramid',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='nextgisweb',
    install_requires=requires,
    extras_require=extras_require,
    tests_require=['nose', ],
    entry_points=entry_points,
)
