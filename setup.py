from setuptools import setup, find_packages

version = '1.0'

setup(
    name='iuem.usersandgroups',
    version=version,
    description="",
    long_description=open("README.rst").read() + "\n" +
        open("CHANGES.txt").read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Framework :: Zope2",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='',
    author='',
    author_email='',
    url='http://svn.plone.org/svn/collective/',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['iuem'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'node.ext.ldap',
        'python_ldap',
        'plone.api',
        # -*- Extra requirements: -*-
    ],
    extras_require=dict(
        test=['plone.app.testing', 'plone.app.robotframework'],
    ),
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
    setup_requires=["PasteScript"],
    paster_plugins=["ZopeSkel"],
)
