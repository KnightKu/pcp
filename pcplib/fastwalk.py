import os
import readdir
import stat

def fastwalk (sourcedir, onerror=None, topdown=True):
    """Improved version of os.walk: generates a tuple of (sourcedir,[dirs],
    [files]). This version tries to use readdir to avoid expensive stat
    operations on lustre."""
    
    dirlist = []
    filelist = []

    try:
        entries = readdir.readdir(sourcedir)
    except Exception as  err:
        if onerror is not None:
            onerror(err)
        return

    for entry in entries:
        name = entry.d_name
        filetype = entry.d_type
    
        if not name in (".", ".."):
            if filetype == 0:
                fullname = os.path.join(sourcedir, name)
                mode = os.lstat(fullname).st_mode
                if stat.S_ISDIR(mode):
                    filetype = 4
                else:
                    filetype = 8

            if filetype == 4:
                dirlist.append(name)
            else:
                filelist.append(name)

    if topdown:
        yield sourcedir, dirlist, filelist

    for d in dirlist:
        fullname = os.path.join(sourcedir, d)
        for entries in fastwalk(fullname, onerror, topdown):
            yield entries

    if not topdown:
        yield sourcedir, dirlist, filelist