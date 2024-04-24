from setuptools import setup, find_packages

setup(
    name='solvis_sc3_modbus',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "logging",
        "pyModbusTCP"
    ],
    python_requires='>=3.7',
    license='Apache License',
    author='rei',
    author_email='rei@reixd.net',
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
    ],
)
