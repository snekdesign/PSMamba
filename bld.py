import os
import re
import subprocess

_BUILD = 'build'
_DUPLICATED = frozenset([
    b'??0bad_alloc@std@@QEAA@AEBV01@@Z',
    b'??0bad_array_new_length@std@@QEAA@AEBV01@@Z',
    b'??0exception@std@@QEAA@AEBV01@@Z',
    b'??1bad_array_new_length@std@@UEAA@XZ',
    b'?what@exception@std@@UEBAPEBDXZ',
])
_LIBRARY_BIN = os.environ['LIBRARY_BIN']


def main():
    with subprocess.Popen(
        ['dumpbin', '/EXPORTS', os.path.join(_LIBRARY_BIN, 'libmamba.dll')],
        stdout=subprocess.PIPE,
    ) as dumpbin:
        it = dumpbin.stdout
        next(filter(re.compile(br'ordinal\s+hint\s+RVA\s+name').search, it))
        next(it)
        with open('libmamba.def', 'wb') as f:
            f.write(b'LIBRARY libmamba.dll\nEXPORTS\n')
            for line in it:
                if line.isspace():
                    break
                name = line.split(maxsplit=4)[3]
                if name not in _DUPLICATED:
                    f.write(b'    %b\n' % name)
        dumpbin.communicate()
    if dumpbin.returncode:
        raise subprocess.CalledProcessError(dumpbin.returncode, dumpbin.args)
    subprocess.run('lib /DEF:libmamba.def /MACHINE:X64', check=True)
    os.mkdir(_BUILD)
    subprocess.run(
        [
            'cmake',
            '-DCMAKE_INSTALL_PREFIX="%(LIBRARY_PREFIX)s"' % os.environ,
            '-GVisual Studio 17 2022',
            '..',
        ],
        cwd=_BUILD,
        check=True,
    )
    subprocess.run('cmake --build . --config Release', cwd=_BUILD, check=True)
    subprocess.run('cmake --install .', cwd=_BUILD, check=True)
    os.link('PSMamba.psm1', os.path.join(_LIBRARY_BIN, 'PSMamba.psm1'))


if __name__ == '__main__':
    main()
