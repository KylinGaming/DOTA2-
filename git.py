import subprocess

cmd = 'curl localhost:5600 --data-binary "@E:\Aan\水人.dem"'#要解析的录像文件路径
data = subprocess.Popen(cmd,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        shell=True)
for i in data.stdout.readlines():
    with open("水人.txt", 'ab') as fp:#返回的数据的输出位置和输出文件名
        fp.write(i)
