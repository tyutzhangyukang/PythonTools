# -*- coding: utf-8 -*-
import sys
sys.path.append('.\\core')

#from __future__ import print_function
# 这个语句是 Python2 的概念，Python3 相对于 Python2 是 future，在 Python2 的环境下超前使用 Python3 的 print 函数

#from core.colors  import bad, good, info, run, green, red, white, end
from core.colors  import bad, good, info, run, green, red, white, end

# 打印 banner
print('''      ____  __          __
     / %s__%s \/ /_  ____  / /_____  ____
    / %s/_/%s / __ \/ %s__%s \/ __/ %s__%s \/ __ \\
   / ____/ / / / %s/_/%s / /_/ %s/_/%s / / / /
  /_/   /_/ /_/\____/\__/\____/_/ /_/ %sv1.2.1%s\n''' %
      (red, white, red, white, red, white, red, white, red, white, red, white,
       red, white, end))