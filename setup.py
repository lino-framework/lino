from setuptools import setup
fn = 'lino/setup_info.py'
with open(fn, "rb") as fd:
    exec(compile(fd.read(), fn, 'exec'))
# above line is equivalent to the line below, except that it works
# also in Python 3:
# execfile(fn)

if __name__ == '__main__':
    setup(**SETUP_INFO)

