# Clonedir
目录克隆工具。用于克隆出一个和源目录结构完全一样的目录，但其中的文件大小为0。

## Usage 用法
```` shell
python clonedir.py [-h] [-r D_ROOT] [-o D_OUTPUT] [-t]  
python clonedir.py -t -r /home
python clonedir.py -t -r /home -o /home_clone
````
or 或者
```` shell
clonedir [-h] [-r D_ROOT] [-o D_OUTPUT] [-t] 
clonedir -t -r /home
clonedir -t -r /home -o /home_clone
````

## Optional Arguments 选项
```` shell
  -h, --help                            查看帮助信息。  
  -r D_ROOT, --root-dir D_ROOT          要克隆的根文件夹绝对路径。  
  -o D_OUTPUT, --output-dir D_OUTPUT    输出文件夹的绝对路径。  
  -t, --tar                             生成tar归档。  
  -s, --symlink                         克隆符号链接内容。如果发现软链接，克隆软链接指向的目录。
````
## Info 提示
1. 仅支持Linux平台。Only Linux supported.

2. 要克隆程序所在目录，并生成归档，并克隆软链接目标：
    ```` shell
    clonedir -t -s
    ````