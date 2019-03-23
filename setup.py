from setuptools import setup, find_packages

desc = ''
with open('README.rst') as f:
    desc = f.read()

setup(
    name='aumbry',
    version='0.10.0',
    description=('Multi-type configuration library for Python'),
    long_description=desc,
    url='https://github.com/pyarmory/aumbry',
    author='John Vrbanac',
    author_email='john.vrbanac@linux.com',
    license='Apache v2',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],

    keywords='configuration yaml etcd json parameter store multiple',
    packages=find_packages(exclude=['contrib', 'docs', 'spec*']),
    install_requires=[
        'six',
        'alchemize>=0.10.0',
        'pike',
        'deepmerge',
    ],
    extras_require={
        'yaml': ['pyyaml>=5.1'],
        'consul': ['requests'],
        'etcd2': ['requests'],
        'param_store': ['boto3'],
        'fernet': ['cryptography>=2.1.2'],
        'cli': [
            'pyyaml>=5.1',
            'requests',
            'boto3',
            'cryptography>=2.1.2'
        ],
    },
    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': [
            'aumbry = aumbry.cli.app:main'
        ],
    },
)
