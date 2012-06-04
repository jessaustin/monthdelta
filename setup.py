from setuptools import setup

setup(name='MonthDelta',
      version='1.0a',
      description='date computations with months',
      long_description=open('README.txt').read(),
      author='Jess Austin',
      author_email='jess.austin@gmail.com',
      url='http://pypi.python.org/pypi/MonthDelta',
      license='MIT',
      py_modules=['monthdelta'],
      provides=['monthdelta'],
      test_suite='nose.collector',
      tests_require=['Nose'],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3'])
