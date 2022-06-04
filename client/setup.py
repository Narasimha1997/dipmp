
from setuptools import setup, find_packages

long_description = open('README.md').read()


setup(
        name='dipmp-pkg',
        version='0.1.1',
        author='Narasimha Prasanna HN',
        author_email='narasimhaprasannahn@gmail.com',
        url='https://github.com/Narasimha1997/pyMigrate',
        description='Transform python codebase to a virtual environment',
        long_description=long_description,
        long_description_content_type="text/markdown",
        license='MIT',
        packages=find_packages(),
        entry_points={
            'console_scripts': [
                'dipmp = dipmp_pkg.main:main'
            ]
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        keywords='python web3',
        zip_safe=False,
        install_requires=[
            "toml==0.10.2",
            "requests==2.27.1"
        ]
)
