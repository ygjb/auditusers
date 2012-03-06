import os, sys
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def main():
 setup(
     name = "auditusers",
     version = "0.1",
     author = "Yvan Boily",
     author_email = "yboily at mozilladotcom",
     description='A tool for auditing github users',
     url = "https://github.com/ygjb/auditusers",
     packages=['auditusers'],
     long_description=read('README.md'),
     entry_points = make_entry_points(),
     classifiers=['Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python'],
     install_requires= ['requests>=0.6.2']
 )


def cmdline_entrypoints(versioninfo, platform, basename):
    target = 'auditusers.audit:main'
    if platform.startswith('java'):
        points = {'auditusers': target}
    else:
        if basename.startswith("pypy"):
            points = {'auditusers-%s' % basename: target}
        else: # cpython
            points = {'auditusers-%s.%s' % versioninfo[:2] : target,}
        points['auditusers'] = target
    return points

def make_entry_points():
    basename = os.path.basename(sys.executable)
    points = cmdline_entrypoints(sys.version_info, sys.platform, basename)
    keys = list(points.keys())
    keys.sort()
    l = ["%s = %s" % (x, points[x]) for x in keys]
    return {'console_scripts': l}

if __name__ == '__main__':
    main()
