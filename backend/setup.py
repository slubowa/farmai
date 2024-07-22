from setuptools import setup, find_packages

setup(
    name='farm_ai_backend',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask_cors',
        'flask_session',
        'pandas',
        'scikit-learn',
        'joblib',
        'requests',
        'numpy',
        'python-dotenv',
        'openai',
    ],
)