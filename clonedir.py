import os
import sys
from glob import glob
import argparse
from pathlib import Path
# # clonedir -t -r /home/


# 带颜色输出
def color_str(s, color):
    if color == "RED":
        return "\033[1;31;40m"+str(s)+"\033[0m"
    elif color == "YELLOW":
        return "\033[1;33;40m"+str(s)+"\033[0m"
    else:
        return "\033[1;32;40m"+str(s)+"\033[0m"


# 参数处理
parser = argparse.ArgumentParser(
    description="目录克隆工具。用于克隆出一个和源目录结构完全一样的目录，但其中的文件大小为0。")
parser.add_argument("-r", "--root-dir", dest="d_root",
                    type=str, default="", help="要克隆的根文件夹绝对路径。")
parser.add_argument("-o", "--output-dir", dest="d_output", type=str, default="",
                    help="输出文件夹的绝对路径")
parser.add_argument("-t", "--tar", dest="tar", help="生成tar归档。",
                    action="store_true")
parser.add_argument("-s", "--symlink", dest="symlink", help="克隆符号链接内容。如果发现软链接，克隆软链接指向的目录。",
                    action="store_true")
args = parser.parse_args()

if args.d_root.strip() == "/" or args.d_output.strip() == "/":
    print("[ERROR] 不允许克隆(到) / 目录")
    sys.exit(1)


# 构造路径
d_root = args.d_root.strip().rstrip("/").replace("/"+__file__, "", -1)
d_output = args.d_output.strip().rstrip("/").replace("/"+__file__, "", -1)

if len(d_root) == 0:
    d_root = str(Path.cwd())

if len(d_output) == 0:
    d_output = d_root+"_clone"

print(color_str("[源目录] ", "YELLOW"), d_root)
print(color_str("[输出目录] ", "YELLOW"), d_output)

# 验证根目录是否存在
if not Path(d_root).exists():
    print(color_str("[错误] ", "RED")+"源目录 "+d_root + " 不存在。")
    sys.exit(1)

# 如果输出目录存在则取消
if Path(d_output).exists():
    print(color_str("[错误] ", "RED")+"输出目录 "+d_output + " 已存在，请删除后重试。")
    sys.exit(1)

# 创建目录
dirs = [d for d in glob(d_root+"/**/", recursive=True)]
for d in dirs:
    if Path(d).is_symlink() and not args.symlink:
        print(color_str("[忽略 - 符号链接] ", "YELLOW")+d)
        continue
    if not Path(d).is_dir:
        continue
    newdir = d.replace(d_root, d_output, 1)
    if not Path(newdir).exists():
        Path(newdir).mkdir()
        print(color_str("[创建] ", "GREEN")+newdir)
    else:
        print(color_str("[忽略] ", "YELLOW") + newdir + " 已存在")


# 创建文件
files = [f for f in glob(d_root+"/**/*", recursive=True)]
for f in files:
    newfile = f.replace(d_root, d_output, 1)
    if Path(newfile).parent.is_dir():
        Path(newfile).touch()
        print(color_str("[创建] ", "GREEN")+newfile)
    else:
        print(color_str("[忽略 - 符号链接内容]", "YELLOW") + newfile)


# 创建归档
if args.tar:
    print(color_str("[正在创建归档]", "GREEN"))
    os.system("rm " + d_output + ".tar")
    tar_cmd = "tar -cvf " + d_output + ".tar" + " " + d_output
    os.system(tar_cmd)
    print(color_str("[归档已创建]", "GREEN") + d_output + ".tar")
