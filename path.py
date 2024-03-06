import os.path
import stat


def dlog(message):
    print(message, flush=True)


def path_exists(path: str) -> bool:
    if os.path.exists(path):
        return True
    try:
        atts = os.lstat(path)
        if atts:
            print("文件存在")
            return True
    except Exception as e:
        pass
    return False


def path_is_dir(path: str) -> bool:
    if not path_exists(path):
        return False
    attrs = os.lstat(path)
    # 判断是符号链接还是目录
    st_mode = attrs.st_mode
    if attrs.st_mode and stat.S_ISDIR(st_mode):
        return True
    return False
