from setuptools import setup, find_packages

from swissql.manifest import Manifest
 
 

 
setup(name=Manifest.APP_NAME,
      version=Manifest.APP_VERSION,
      url=Manifest.GIT_URL,
      license=Manifest.LICENSE,
      author=Manifest.AUTHORS_GIT,
      author_email=Manifest.EMAIL,
      packages= find_packages(),
      install_requires = Manifest.REQUIREMENTS ,
      description=Manifest.APP_DESCRIPTION,
      
      python_requires=">=3.7.*",
      entry_points={
        'console_scripts': [
            'swissql = swissql.main:main_start',
        ]}
      )