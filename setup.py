from setuptools import setup, find_packages

with open('requirements.txt') as requirements:
    setup(
        name='chebanca',
        version='0.1',
        packages=find_packages(),
        include_package_data=True,
        install_requires=requirements.read().splitlines(),
        entry_points='''
            [console_scripts]
            chebanca=chebanca.main:cli
        ''',
    )
