import os
from setuptools import setup

name = 'animatplot'

with open('README.md') as f:
    long_description = f.read()

here = os.path.abspath(os.path.dirname(__file__))

version_ns = {}
with open(os.path.join(here, name, '_version.py')) as f:
    exec(f.read(), {}, version_ns)

setup(name=name,
      version=version_ns['__version__'],
      description='Making animating in matplotlib easy',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/t-makaro/animatplot/',
      author='Tyler Makaro',
      author_email='',
      license='MIT',
      packages=['animatplot',
                'animatplot.animations',
                'animatplot.blocks'],
      python_requires='>=3.8',
      install_requires=['matplotlib>=2.2'],
      classifiers=[
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Visualization',
      ],
      zip_safe=False)
