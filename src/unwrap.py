#!/usr/bin/env python3
"""unwrap - 还原 wrap 后的文件
unwrap wrapping_path out_path
"""
from pathlib import Path
from lzma import decompress
from sys import argv

import numpy as np
from PIL import Image

# 文件结束标识
EOF_FLAG = 256

# 读取
wrapping = np.asarray(Image.open(argv[1]), dtype=np.uint16)
# 查找 EOF 位置
eof_y, eof_x = np.squeeze(np.where(wrapping[:, :, 3] != 0))
eof_z = {51: 0, 102: 1, 153: 2}[wrapping[eof_y, eof_x, 3]]
# 添加 EOF
wrapping[eof_y, eof_x, eof_z] = EOF_FLAG
# 去除 alpha 通道
wrapping = wrapping[:, :, :3]
# 还原为字节串
wrapping = wrapping.flatten()
# 读取到 EOF
wrapping = wrapping[:wrapping.argmax()]
# 转换类型为 uint8 后转为字节串解压缩
source_file = bytes(wrapping.astype(np.uint8))
source_file = decompress(source_file)
# 保存文件
Path(argv[2]).write_bytes(source_file)
