from setuptools import setup

setup(name='MonthDelta',
      version='1.0b',
      description='date computations with months',
      long_description=open('README.rst').read(),
      author='Jess Austin',
      author_email='jess.austin@gmail.com',
      url='http://pypi.python.org/pypi/MonthDelta',
      license='MIT',
      py_modules=['monthdelta'],
      provides=['monthdelta'],
      test_suite='tests.test_monthdelta',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3'])
