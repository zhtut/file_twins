import os
import shutil
import stat
import subprocess
import sys
from path import *


def dlog(message):
    print(message, flush=True)


def sync_two_file(path1, path2):
    try:
        origin_size = os.path.getsize(path1)
        if path_exists(path2):
            if os.path.getsize(path2) == origin_size:
                dlog(f"{path1}与{path2}大小一致，无需同步")
                return
    except Exception:
        pass
    copy_result, copy_msg = subprocess.getstatusoutput(f"cp -R {path1} {path2}")
    if copy_result == 0:
        shutil.copystat(path1, path2)
        dlog(f"已拷贝{path1}至{path2}")
    else:
        dlog(f"拷贝{path1}至{path2}失败：{copy_msg}")


class SyncAction:
    origin: str = None
    dest: str = None

    def __init__(self, origin: str, dest: str):
        self.origin = origin
        self.dest = dest

    def sync(self):
        """
        开始同步两个文件夹
        :return:
        """
        if not path_exists(self.origin):
            dlog(f"源文件路径不存在：{self.origin}")
            return

        is_origin_folder = path_is_dir(self.origin)

        is_dest_folder = None
        if path_exists(self.dest):
            is_dest_folder = os.path.isdir(self.dest)
            if is_dest_folder:
                dlog(f"目标{self.dest}是一个文件夹")
            else:
                dlog(f"目标{self.dest}是一个普通文件")

        if is_dest_folder is not None and is_origin_folder != is_dest_folder:
            dlog(f"目的路径跟源路径不是一个类型，无法同步")
            return

        # 判断是文件还是文件夹
        if is_origin_folder:
            if not path_exists(self.dest):
                try:
                    os.mkdir(self.dest)
                except Exception as e:
                    dlog(f"创建文件夹失败：{e}")
            # 是文件夹，就遍历文件夹中的文件和文件夹
            files = os.listdir(self.origin)
            for file in files:
                src_file = os.path.join(self.origin, file)
                dest_file = os.path.join(self.dest, file)
                SyncAction(src_file, dest_file).sync()
        else:
            # 是文件，就复制文件
            sync_two_file(self.origin, self.dest)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("参数不对，应该要3个参数")
    origin = sys.argv[1]
    dest = sys.argv[2]
    SyncAction(origin, dest).sync()
