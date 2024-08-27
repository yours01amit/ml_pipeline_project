from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = "-e ."


def get_requirements(filepath:str) -> List[str]:
    requirements = []

    if HYPHEN_E_DOT in requirements:
        requirements.remove(HYPHEN_E_DOT)

    with open(filepath) as file_obj:
        requirements = file_obj.readlines()
        requirements = [i.replace('\n','') for i in requirements]



setup(
    name="ML project",
    version="0.0.1",
    author="Amit Kumar",
    author_email='emmysingh019@gmail.com',
    packages= find_packages(),
    install_requires = get_requirements('requirements.txt')
)