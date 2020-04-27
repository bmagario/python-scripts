import os
f = open("C:" + "\\" + "TEMP" + "\\" + "test.txt", "w+")
d = "\\\\" + "DISK1" + "\\" + "USR"
[os.path.join(d, o) for o in os.listdir(d)
    if os.path.isdir(f.write(os.path.join(d, o) + ","))]

d = "\\\\" + "DISK2" + "\\" + "USR"
[os.path.join(d, o) for o in os.listdir(d)
    if os.path.isdir(f.write(os.path.join(d, o) + ","))]

d = "\\\\" + "DISK3" + "\\" + "USR"
[os.path.join(d, o) for o in os.listdir(d)
    if os.path.isdir(f.write(os.path.join(d, o) + ","))]