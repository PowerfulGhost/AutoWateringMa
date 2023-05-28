import shutil
import os

N=1000
for dir in os.listdir():
    if dir=="PseudoDataGen.py":
        continue
    print(dir)
    for i in range(1,N):
        shutil.copyfile(f"{dir}/0.png",f"{dir}/{i}.png")
