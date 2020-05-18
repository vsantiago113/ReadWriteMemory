from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='ReadWriteMemory',
      packages=['ReadWriteMemory'],
      version='0.1.5',
      license='MIT',
      description='ReadWriteMemory Class to work with Windows process memory and hacking video games.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Victor M Santiago',
      author_email='vsantiago113sec@gmail.com',
      url='https://github.com/vsantiago113/ReadWriteMemory',
      download_url='',
      keywords=['ReadWriteMemory', 'Hacking', 'Cheat Engine'],
      python_requires='>=3.4.0',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Topic :: Utilities',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      )
