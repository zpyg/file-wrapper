#!/usr/bin/env python3
"""wrap - 转任意二进制文件为图片
wrap file_path out_path
"""
from sys import argv
from pathlib import Path
from math import ceil
from lzma import compress

import numpy as np
from PIL import Image

# 文件结束标识
EOF_FLAG = 256

# 读取文件并压缩
source_file = Path(argv[1]).read_bytes()
source_file = compress(source_file)
# 转为数组
wrapping = np.asarray(list(map(int, source_file)), dtype=np.uint16)
# 添加 EOF
wrapping = np.append(wrapping, values=EOF_FLAG)
# 补全为正方形
wrapping_width = ceil(wrapping.size**0.5)
wrapping.resize((wrapping_width, wrapping_width, 3))
# 添加 alpha 通道
wrapping_alpha = np.full((wrapping_width, wrapping_width, 1), 0)
wrapping = np.c_[wrapping, wrapping_alpha]
# 查找 EOF 位置
eof_y, eof_x, eof_z = np.squeeze(np.where(wrapping[:, :] == EOF_FLAG))
# 在 alpha 通道存储 EOF 位置
wrapping[eof_y, eof_x, 3] = {0: 51, 1: 102, 2: 153}[eof_z]
# 转换类型为 uint8 后保存
Image.fromarray(wrapping.astype(np.uint8)).save(argv[2])
