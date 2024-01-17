# file_twins
每天定时同步文件夹，适用于ssd定时拷贝到机械硬盘用作备份，ssd读写快，机械硬盘存储量大

# 先决条件
- 安装docker，docker很好的解决了权限和启动时机的问题

# 使用
## 1. 先配置docker-compose.yml 
```
version: '3.9'

services:
  app:
    image: file_twins
    build: .
    container_name: file_twins
    restart: always
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Shanghai
    volumes:
      - ./config.json:/config.json
      - /Volumes/Media/mt-photos:/origin
      - /Volumes/Raid/mt_photos:/dest
```
/Volumes/Media/mt-photos是源文件夹，只修改这个就可以，后面可以不改
/Volumes/Raid/mt_photos是目的文件夹，后面/dest代表docker里面的目录
如果有多组的需求，则在下面继续添加两个目录，然后再配置到tasks中

## 2. 配置config.json
```json
{
  "tasks": [
    {
      "origin": "/origin",
      "dest": "/dest",
      "start": "8:00:00"
    }
  ]
}
```
tasks是一个数组，可以支持多个任务的同步
origin代表源文件夹，需要跟上面的/origin一致
dest代表目的文件夹，需要跟上面的/dest一致
start代表每天几点开始同步，目前只支持每天同步

## 3. 启动
```shell
docker compose up -d --build
```

## 4. 查看
```shell
docker ps
```
