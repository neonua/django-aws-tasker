import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from django-lambda-tasker/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    print(filename)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("django-lambda-tasker", "__init__.py")


if sys.argv[-1] == 'publish':
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

setup(
    name='django-lambda-tasker',
    version=version,
    license="MIT",
    description='',
    long_description=open('README.md').read(),
    author='neonua',
    author_email='neonua666@gmail.com',
    url='',
    packages=[
        'django-lambda-tasker'
    ],
    install_requires=['Django>=3.2'],
    include_package_data=True,
    keywords='django-lambda-tasker',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe=False,
    tests_require=['Django>=3.2'],
)

