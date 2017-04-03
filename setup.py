from setuptools import setup

setup(name='animatplot',
      version='0.1.dev1',
      description='Making animating in matplotlib easy',
      url='https://github.com/t-makaro/animatplot/',
      author='Tyler Makaro',
      author_email='',
      license='MIT',
      packages=['animatplot'],
      install_requires=['matplotlib'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
      ],
      zip_safe=False)