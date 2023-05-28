import os
import csv
import shutil
from Global import growthStage, datasetVolumnRatio

clearOldDataset = False
generateTempDataset = False
generateDataset = True

# 清除所有数据集
if clearOldDataset:
    for set in ["test", "train", "validate"]:
        if set not in os.listdir("./data"):
            continue
        print(f"清理{set}数据集")
        setPath = f"./data/{set}/"
        for entry in os.listdir(setPath):
            os.remove(setPath+entry)
    print("清理完成")


# 把rawData中所有数据复制到temp/dataPreprocess中
# 同时把标签记录在temp/dataPreprocess/target.csv中
if generateTempDataset:
    print("生成临时数据集")

    csvFile = open(f"./temp/dataPreprocess/target.csv", "w", newline="")
    csvWriter = csv.writer(csvFile)

    imgCount = 0
    for stageName in growthStage.keys():
        dirPath = f"./rawData/{stageName}"

        for fileName in os.listdir(dirPath):
            filePath = f"{dirPath}/{fileName}"
            dstPath = f"./temp/dataPreprocess/{imgCount}.png"
            shutil.copyfile(filePath, dstPath)
            csvWriter.writerow([f"{imgCount}.png", growthStage[stageName]])
            print(imgCount, end="\r")
            imgCount += 1

    csvFile.close()

    print("临时数据集生成完成")


# 把临时数据集中的图片按比例复制到data/train中
# 并根据图片的类别在各自的target.csv中记录
# 保证每个类别的数据量相等
if generateDataset:
    print("分配数据到训练集、验证集和测试集")

    # 统计每个类别的数据量
    csvFile = open("./temp/DataPreprocess/target.csv")
    csvReader = csv.reader(csvFile)
    targetContent = []
    for line in csvReader:
        targetContent.append(line)
    csvFile.close()

    amountStat = [0, 0, 0, 0, 0]
    for entry in targetContent:
        amountStat[int(entry[1])] += 1
    print(amountStat)

    # 计算训练集、验证集和测试集需要的每个类别的数据量
    M = len(targetContent)  # 数据集总量
    N = min(amountStat)     # 每个类别需要的数据量
    N_train = N * datasetVolumnRatio["train"]
    N_validate = N * datasetVolumnRatio["validate"]
    N_test = N * datasetVolumnRatio["test"]
    assert N_train + N_validate + N_test == N

    # 向训练集、验证集和测试集分配数据
    trainTargetFile = open("./data/train/target.csv", "w", newline="")
    trainWriter = csv.writer(trainTargetFile)
    validateTargetFile = open("./data/validate/target.csv", "w", newline="")
    validateWriter = csv.writer(validateTargetFile)
    testTargetFile = open("./data/test/target.csv", "w", newline="")
    testWriter = csv.writer(testTargetFile)
    currentClass = "0"    # 目前在分配的类别
    count_train = 0
    count_validate = 0
    count_test = 0
    idx_train = 0
    idx_validate = 0
    idx_test = 0
    for i in range(M):
        imgPath = f"./temp/dataPreprocess/{i}.png"
        info = f"currentClass={currentClass}, "
        if count_train != N_train:  # 分配训练集
            shutil.copyfile(imgPath, f"./data/train/{idx_train}.png")
            idx_train += 1
            count_train += 1
            info += f"idx_train={idx_train}, count_train={count_train}"
            trainWriter.writerow([f"{idx_train}.png", currentClass])
        if count_train == N_train and count_validate != N_validate:   # 分配验证集
            shutil.copyfile(imgPath, f"./data/validate/{idx_validate}.png")
            idx_validate += 1
            count_validate += 1
            info += f"idx_validate={idx_validate}, count_validate={count_validate}"
            validateWriter.writerow([f"{idx_validate}.png", currentClass])
        if count_train == N_train and count_validate == N_validate and count_test != N_test:    # 分配测试集
            shutil.copyfile(imgPath, f"./data/test/{idx_test}.png")
            idx_test += 1
            count_test += 1
            info += f"idx_test={idx_test}, count_test={count_test}"
            testWriter.writerow([f"{idx_test}.png", currentClass])
        if count_train == N_train and count_validate == N_validate and count_test == N_test:    # 本类别分配完毕，快进到下个类别
            if targetContent[i][1] == currentClass:
                continue
            else:
                currentClass = targetContent[i][1]
                count_train = 0
                count_validate = 0
                count_test = 0
                info = "                                                                                         "
        print(info, end="\r")

    print("\n分配完成")
