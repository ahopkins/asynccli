import setuptools

setuptools.setup(
    name="asynccli",
    version="0.1.3",
    url="https://github.com/ahopkins/asynccli",

    author="Adam Hopkins",
    author_email="admhpkns@gmail.com",

    description="A CLI framework based on asyncio",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    setup_requires=['pytest-runner', ],
    tests_require=['pytest', ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
