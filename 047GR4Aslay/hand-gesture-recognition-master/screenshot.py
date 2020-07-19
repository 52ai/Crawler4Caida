import os
import os.path
import mss

cnt = 1
while cnt < 5:
    with mss.mss() as sct:
        filename = sct.shot(mon = -1, output = 'screenshot_{}.png'.format(str(cnt)))
        print(filename)
        cnt += 1