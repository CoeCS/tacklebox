#!/usr/bin/env python

import os
import py_compile
import shutil
import stat
import sys
import zipfile


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Syntax: {0} yourscript.py\n".format(sys.argv[0]))
        sys.exit(1)


    filename = sys.argv[1]
    if not filename.endswith(".py"):
        sys.stderr.write("Error: {0} doesn't end with '.py'\n".format(repr(filename)))
        sys.exit(1)

    exename, _ = os.path.splitext(filename)

    if os.path.exists(exename):
        sys.stderr.write("Error: {0} already exists\n".format(repr(exename)))
        sys.exit(1)

    if os.path.exists("__main__.py"):
        sys.stderr.write("Error: __main__.py already exists in current directory.\n"
        sys.exit(1)

    shutil.copyfile(filename, "__main__.py")

    exfile = open(exename, 'w')
    exfile.write("#!/usr/bin/env python\n")

    zexfile = zipfile.PyZipFile(exfile, 'w')
    zexfile.writepy("__main__.py")
    for path in sys.argv[2:]:
        zexfile.writepy(path)


    os.remove("__main__.py")
    os.remove("__main__.pyc")

    zexfile.close()
    exfile.close()

    st = os.stat(exename)
    os.chmod(exename, st.st_mode | stat.S_IXUSR)



if __name__ == '__main__':
    main()
