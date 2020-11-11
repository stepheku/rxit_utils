from setuptools import setup, find_packages
from pathlib import Path

with open(Path(".", 'README.md')) as f:
    README = f.read()
with open(Path(".", 'CHANGES.txt')) as f:
    CHANGES = f.read()

# TODO: Add the custom commands to install the unrtf system dependency
CUSTOM_COMMANDS = [
    ['apt-get', 'update'],
    ['apt-get', '--assume-yes', 'install', 'unrtf'],
]

with open(Path(".", "requirements.txt"), "r") as f:
    requires = f.read().splitlines()

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
    ]

setup(name='rxit_utils',
      version='0.0',
      description='rxit_utils',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = rxit_utils:main
      """,
      )
