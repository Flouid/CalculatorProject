from setuptools import setup


setup(
        name='CalculatorProject',
        version='1.0',
        py_modules=['client'],
        install_requires=['Click'],
        entry_points='''
        [console_scripts]
        client=client:cli
        '''
)
