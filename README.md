# 全自动追番方案
## 说明
本项目根据 qBittorrent, Plex 以及 infuse 搭建
![Image](https://cdn.sspai.com/2022/02/09/d94ec60db1c136f6b12ba3dca31e5f5f.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1)
完整教程请移步 [自动追番机器建立教程](https://www.craft.do/s/48MFW9QwaCQMzt)
### 需要依赖
```bash
pip install qbittorrent-api
```
## 使用之前
在 `config.json` 中填入你的 `hostip` `username` `password` `savepath`:
```json
{
  "host_ip": "192.168.31.10:8181",
  "username": "admin",
  "password": "adminadmin",
  "savepath": "/downloads/Bangumi",
  "method": "pn"
}
```
## 自动下载规则建立
```shell
python3 rule_set.py --name <新番名称>
```

# 不符合规则的番剧重命名

## rename_qb
```shell
python3 rename_qb.py --help
```
目前有三种重命名模式
- `normal`: 普通模式，直接重命名，保留番剧字幕组信息。
- `pn`: 纯净模式，保留番剧名称和剧集信息，去掉多余信息。
- `hash`: 哈希模式，用于 Torrent 软件完成之后执行命令。

然后运行 `rename_qb.py` 即可, 如果只想对新番进行重命名，可以在程序中添加添加 `categories="Bangumi"` 语句

根据 `qBittorrent` API 自动重命名下载的种子文件，且不会让种子失效。

- 可以作为 `bash` 脚本运行，可以直接使用仓库中的 `rename.sh`
- 可以构建 `crontab` 定时运行
- 可以使用 Docker 部署，详见文末（推荐）
```shell
0,30 * * * * python3 /path/rename_qb.py
```
- 也可以监测文件夹变化运行。

### rename_qb `hash` 功能
需要 QB 下载完成之后反向输入种子的哈希值，`config` 的`method` 中填写 `hash`, 添加可以编写 Shell 脚本：
```shell
#!/bin/bash
hash = $1

/usr/bin/python3 /path/rename_hash.py --hash $hash
```
QB 中调用该脚本并且引入 **%I** 属性

## Docker 部署
可以使用 Docker 部署重命名应用：
```shell
docker run -d \ 
  --name=Bangumi_rename \ 
  -e HOST=192.168.31.10:8181 \ 
  -e USER=admin \ 
  -e PASSWORD=adminadmin \ 
  -e METHOD=pn \ 
  -e TIME=1800 \ 
  estrellaxd/bangumi_rename_qb:latest
```
`TIME` 为间隔运行时间，单位为秒
# 声明
本项目的自动改名规则根据 [miracleyoo/anime_renamer](https://github.com/miracleyoo/anime_renamer) 项目