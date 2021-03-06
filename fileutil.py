import sys, os, errno, shutil
import wx
from async import async_call, coroutine
from dialogs import dialogs
from fileutil_common import *

def atomic_write_file(path, data, mode="wb"):
    temp = os.path.join(os.path.dirname(path), ".saving." + os.path.basename(path))
    try:
        with open(temp, mode) as out:
            try:
                shutil.copystat(path, temp)
            except OSError:
                pass
            out.write(data)
    except Exception:
        try:
            os.remove(temp)
        except Exception:
            pass
        raise
    else:
        try:
            rename(temp, path)
        except Exception:
            try:
                os.remove(temp)
            except Exception:
                pass
            raise

def read_file(path, mode="rb"):
    with open(path, mode) as f:
        return f.read()

rename = os.rename

def remove(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)

def mkdir(path):
    try:
        os.mkdir(path)
        return True
    except OSError, e:
        if e.errno == errno.EEXIST:
            return False
        raise

def mkpath(path):
    dirpath = path
    parts = []
    while True:
        try:
            os.mkdir(dirpath)
            break
        except OSError, e:
            if e.errno == errno.EEXIST:
                break
            parts.append(os.path.basename(dirpath))
            dirpath = os.path.dirname(dirpath)
    for part in reversed(parts):
        dirpath = os.path.join(dirpath, part)
        os.mkdir(dirpath)

def is_hidden_file(path):
    return os.path.basename(path).startswith(".")

def is_mount_point(path):
    stat = os.stat(path)
    parent_stat = os.stat(os.path.join(path, ".."))
    return stat.st_dev != parent_stat.st_dev or stat.st_ino == parent_stat.st_ino

def mount_point(path):
    while not is_mount_point(path):
        path = os.path.join(path, "..")
    return path

@coroutine
def shell_remove(path):
    if ask_delete_file(path):
        try:
            yield async_call(remove, path)
        except Exception, e:
            dialogs.error(get_top_window(), "Error deleting file:\n\n%s" % e)

@coroutine
def shell_move(srcpath, dstpath):
    if destination_is_same(srcpath, dstpath):
        return
    if ask_move_file(srcpath, dstpath):
        try:
            yield async_call(shutil.move, srcpath, dstpath)
        except Exception, e:
            dialogs.error("Error moving file:\n\n%s" % e)

@coroutine
def shell_copy(srcpath, dstpath):
    if destination_is_same(srcpath, dstpath):
        return
    if ask_copy_file(srcpath, dstpath):
        try:
            yield async_call(shutil.copy2, srcpath, dstpath)
        except Exception, e:
            dialogs.error(get_top_window(), "Error copying file:\n\n%s" % e)

def shell_move_or_copy(srcpath, dstpath):
    srcdev = os.stat(srcpath).st_dev
    dstdev = os.stat(dstpath).st_dev
    if srcdev == dstdev:
        return shell_move(srcpath, dstpath)
    else:
        return shell_copy(srcpath, dstpath)

if sys.platform == "win32":
    from fileutil_win32 import *
else:
    from fileutil_posix import *
