from setuptools import setup, find_packages

setup(
    name='dashboard-ies',
    version='1.0.0',
    description='Dashboard de Gestión de Alumnos - IES',
    author='Tu Nombre',
    packages=find_packages(),
    install_requires=[
        'streamlit==1.29.0',
        'pandas==2.1.4',
        'openpyxl==3.1.2',
        'xlsxwriter==3.1.9'
    ],
    python_requires='>=3.8'
)
