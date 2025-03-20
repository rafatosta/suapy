from setuptools import setup
import suapy

setup_requires = ['setuptools']
try:
    setup(
        name=suapy.__appname__.lower(),
        version=suapy.__version__,
        author=suapy.__author__,
        author_email=suapy.__email__,
        description=suapy.__comment__,
        url=suapy.__website__,
        license='GPLv3+',
        packages=['suapy',
                  'suapy.services'
                  ],
        include_package_data=True,
        package_data={},
        setup_requires=setup_requires,
        entry_points={'gui_scripts': ['suapy = suapy.__main__:main']},
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
