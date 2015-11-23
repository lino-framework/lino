from setuptools import setup
exec(compile(
    open('lino/setup_info.py', "rb").read(), 'lino/setup_info.py', 'exec'))

# above line is equivalent to the line below, except that it works
# also in Python 3

# execfile('lino/setup_info.py')

if __name__ == '__main__':
    setup(**SETUP_INFO)

