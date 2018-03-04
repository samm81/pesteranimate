from setuptools import setup

setup(
    name='pesteranimate',
    version='0.1.0',
    description='Display entries for pesterbot on a time dependent manner',
    url='https://github.com/samm81/pesteranimate',
    author='Samuel Maynard',
    author_email='samwmaynard@gmail.com',
    install_requires=[
        'requests',
        'click'
    ],
    py_modules=['pesteranimate'],
    python_requires='>=3.6',
)
