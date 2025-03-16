from setuptools import setup
import gpaae

setup_requires = ['setuptools']
try:
    setup(
        name=gpaae.__appname__.lower(),
        version=gpaae.__version__,
        author=gpaae.__author__,
        author_email=gpaae.__email__,
        description=gpaae.__comment__,
        url=gpaae.__website__,
        license='GPLv3+',
        packages=['gpaae',
                  'gpaae.services'
                  ],
        include_package_data=True,
        package_data={},
        setup_requires=setup_requires,
        entry_points={'gui_scripts': ['gpaae = gpaae.__main__:main']},
        keywords='Simple Zapzap whatsapp client web app',
        classifiers=[
            'Environment :: X11 Applications :: Qt',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Topic :: Office/Business',
            'Programming Language :: Python :: 3 :: Only'
        ]
    )
except Exception as e:
    print(e)
