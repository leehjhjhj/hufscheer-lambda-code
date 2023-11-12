from data_set import DATA

def check_badword(target):
    for i in range(len(target)):
        for j in range(i + 1, len(target) + 1):
            if target[i:j] in DATA:
                return True
    return False
