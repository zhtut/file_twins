import json
import os
import schedule
import time
import sync
from path import *


def sync_data(origin, dest):
    # 执行同步数据任务
    dlog(f"-------》开始同步任务：{origin}至{dest}")
    sync.SyncAction(origin, dest).sync()
    dlog("--------》同步完成")


def main():
    config_path = "/config.json"
    if not os.path.exists(config_path):
        config_path = "./config.json"
        if not os.path.exists(config_path):
            raise Exception("config.json不存在，请先配置config.json")
    dlog(f"config路径：{config_path}")
    with open(config_path) as f:
        content = json.loads(f.read())
        dlog(f"config的内容：{content}")
        # 获取任务列表
        tasks = content['tasks']
    if not tasks:
        raise Exception("config.json没有配置tasks")

    # 遍历任务列表并安排定时任务
    for task in tasks:
        origin = task['origin']
        dest = task['dest']
        start_time = task['start']

        # 启动的时候也执行一次
        sync_data(origin, dest)

        # 使用 schedule 库安排定时任务
        schedule.every().day.at(start_time).do(sync_data, origin, dest)

    # 启动定时器并保持运行
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    dlog("开始预订Task")
    main()
