import os
import shutil
import sys


def dlog(message):
    print(message, flush=True)


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
        dlog(f"开始同步{self.origin}至{self.dest}")
        if not os.path.exists(self.origin):
            dlog(f"源文件路径不存在：{self.origin}")
            return

        is_origin_folder = os.path.isdir(self.origin)

        is_dest_folder = None
        if os.path.exists(self.dest):
            is_dest_folder = os.path.isdir(self.dest)

        if is_dest_folder is not None and is_origin_folder != is_dest_folder:
            dlog(f"目的路径跟源路径不是一个类型，无法同步")
            return

        # 判断是文件还是文件夹
        if is_origin_folder:
            if not os.path.exists(self.dest):
                os.mkdir(self.dest)
            # 是文件夹，就遍历文件夹中的文件和文件夹
            files = os.listdir(self.origin)
            for file in files:
                src_file = os.path.join(self.origin, file)
                dest_file = os.path.join(self.dest, file)
                SyncAction(src_file, dest_file).sync()
        else:
            # 是文件，就复制文件
            origin_size = os.path.getsize(self.origin)
            if os.path.exists(self.dest) and origin_size == os.path.getsize(self.dest):
                dlog(f"{self.origin}与{self.dest}大小一至，跳过拷贝")
                return
            shutil.copy2(self.origin, self.dest)
            dlog(f"已拷贝{self.origin}至{self.dest}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("参数不对，应该要3个参数")
    origin = sys.argv[1]
    dest = sys.argv[2]
    SyncAction(origin, dest).sync()
