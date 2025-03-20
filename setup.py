from setuptools import setup
import suapbot

setup_requires = ['setuptools']
try:
    setup(
        name=suapbot.__appname__.lower(),
        version=suapbot.__version__,
        author=suapbot.__author__,
        author_email=suapbot.__email__,
        description=suapbot.__comment__,
        url=suapbot.__website__,
        license='GPLv3+',
        packages=['suapbot',
                  'suapbot.services'
                  ],
        include_package_data=True,
        package_data={},
        setup_requires=setup_requires,
        entry_points={'gui_scripts': ['suapbot = suapbot.__main__:main']},
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
