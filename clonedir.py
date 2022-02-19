import os
import sys
from glob import glob
import argparse
# clonedir.py -t -r /home/

# 参数处理
parser = argparse.ArgumentParser(
    description="目录克隆工具。用于克隆出一个和源目录结构完全一样的目录，但其中的文件大小为0。")
parser.add_argument("-r", "--root-dir", dest="d_root",
                    type=str, default="", help="要克隆的根文件夹绝对路径")
parser.add_argument("-o", "--output-dir", dest="d_output", type=str, default="",
                    help="输出文件夹的绝对路径")
parser.add_argument("-t", "--tar", dest="tar", help="生成tar归档",
                    action="store_true")
args = parser.parse_args()

if args.d_root == "/" or args.d_output == "/":
    print("[ERROR] 不允许克隆(到) / 目录")
    sys.exit(1)


# 构造路径
d_root = args.d_root.strip().rstrip("/").replace("/"+__file__, "", -1)
d_output = args.d_output.strip().rstrip("/").replace("/"+__file__, "", -1)

if len(d_root) == 0:
    print("[ERROR] 必须使用 -r 选项指定根目录，绝对路径。")
    sys.exit(1)
    d_root = os.path.abspath(__file__).replace("/"+__file__, "", -1)

if len(d_output) == 0:
    d_output = d_root+"_clone"


print("源目录 ", d_root)
print("输出目录 ", d_output)

# 验证根目录是否存在
if not os.path.exists(d_root):
    print("[ERROR] 源目录 "+d_output + " 不存在。")
    sys.exit(1)

# 如果输出目录存在则取消
if os.path.exists(d_output):
    print("[ERROR] 输出目录 "+d_output + " 已存在，请删除后重试。")
    sys.exit(1)

# 创建目录
dirs = [d for d in glob(d_root+"/**/", recursive=True)]
for d in dirs:
    newdir = d.replace(d_root, d_output, 1)
    if not os.path.exists(newdir):
        os.mkdir(newdir)
        print("[CREATE] "+newdir)
    else:
        print("[INFO]" + newdir + " Already Existed.")


# 创建文件
files = [f for f in glob(d_root+"/**/*.*", recursive=True)]
for f in files:
    newfile = f.replace(d_root, d_output, 1)
    if not os.path.exists(newfile):
        f = open(newfile, "w")
        f.close()
        print("[CREATE] "+newfile)

    else:
        print("[INFO]" + newfile + " Already Existed.")


# 创建归档
if args.tar:
    print("[正在创建归档]")
    os.system("rm " + d_output + ".tar")
    tar_cmd = "tar -cvf " + d_output + ".tar" + " " + d_output
    os.system(tar_cmd)
    print("[归档已创建] " + d_output + ".tar")
