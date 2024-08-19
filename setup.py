from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.0.1',
    author='iddhant Dnyane',
    author_email='siddhantdyane2003@gmail.com',
    install_requires=["groq","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)