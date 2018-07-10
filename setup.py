from setuptools import find_packages, setup

install_requires = [
    'luigi>=2.7',
    'telepot==12.7',
]


setup(
    name='luigi-telegram',
    version='0.1',
    description='Luigi Tasks notifications to Telegram messenger',
    author='Adylzhan Khashtamov',
    url='https://github.com/adilkhash/luigi-telegram',
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
