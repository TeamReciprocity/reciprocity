"""Setup forDjango Imager app."""
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

REQUIRES = [
    'django',
    'psycopg2',
    'django-registration',
]
TEST = [
    'tox',
    'coverage',
    'pytest-cov',
    'factory-boy',
    'nose',


]


setup(name='Reciprocity',
      version='0.0',
      description='Web application to allow for sharing recipes.',
      author=('Team Reciprocity'),
      author_email='reciprocity.register@gmail.com',
      url='',
      license='MIT',
      keywords='django',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='reciprocity',
      install_requires=REQUIRES,
      extras_require={
          'test': TEST,
      },
      )
