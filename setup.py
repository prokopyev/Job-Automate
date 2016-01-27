from setuptools import setup, find_packages

setup(name='jobautomate',
      version='0.0.1',
      author='Mandeep Bhutani',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
        'indeed',
        'selenium',
      ],
      entry_points='''
        [console_scripts]
        jobautomate=jobautomate:main
        ''',
      )