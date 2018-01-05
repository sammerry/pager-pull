from setuptools import setup

setup(
    name="pager-pull",
    version='0.1',
    py_modules=['click', 'pypd'],
    install_requires=[
        'Click', 'pypd'
    ],
    entry_points='''
        [console_scripts]
        pager-pull=pagerpull.pagerpull:cli
    ''',
)
