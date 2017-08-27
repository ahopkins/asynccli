import setuptools

setuptools.setup(
    name="asynccli",
    version="0.1.0",
    url="https://github.com/ahopkins/asynccli",

    author="Adam Hopkins",
    author_email="admhpkns@gmail.com",

    description="A CLI framework based on asyncio",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
