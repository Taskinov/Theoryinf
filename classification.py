from math import log
import copy

def aload(filename):
    file = open(filename,encoding="utf8")
    file = file.read()
    file = file.translate({ord(c): None for c in '1234567890#—.,-:!?"\'/«»„“();'})
    lines = file.split('\n')
    data = []
    for i in range(len(lines)):
        data.append(lines[i].split('\t'))
    X = []
    Y = []
    
    for row in data:
        Y.append(row[0])
        X.append(row[1:])
    parsed_X = list()

    for i in range(len(X)):
        raw = X[i][0] + X[i][1]
        parsed = list()
        raw = raw.split(' ')
        for j in range(len(raw)):
            if raw[j] != '':
                l = raw[j].lower()
                parsed.append(l.lower())
        parsed_X.append(parsed)
    return parsed_X, Y

def learning(X, Y):
    y = {'science' : 0, 'style' : 0, 'culture' : 0, 'life' : 0, 'economics' : 0, 'business' : 0, 'travel' : 0, 'forces' : 0, 'media' : 0, 'sport' : 0}
    x = dict()
    init_val = dict()
    count_words = 0
    init_val = copy.copy(y)
    for i in Y:
        y[i] += 1
    for i in range(len(X)):
         for j in range(len(X[i])):
            if X[i][j] != '':
                count_words += 1
                l = X[i][j]
                if l in x.keys():
                    x[l][Y[i]] += 1
                else:
                    x[l] = copy.copy(init_val)
                    x[l][Y[i]] += 1
    return x, y, count_words


def compute_prob(x, y):
    sum = 0
    xx = copy.copy(x)
    yy = dict()
    for k in y:
        sum+=y[k]
    for k in y:
        yy[k]=y[k]/sum
    for k in x:
        sum = 0
        for i in x[k]:
            sum += x[k][i]
        for i in x[k]:
            xx[k][i]=x[k][i]/sum
    return xx, yy

def clean_x(x, words_count):
    before = len(x)
    xx = dict()
    for k in x:
        sum=0
        for v in x[k].values():
            sum+=v
        if not (sum < words_count * 0.0000001) and (sum > words_count * 0.0000002):
            xx[k] = x[k]
    after = len(xx)
    return xx, before, after
def parse_test(filename):
    file = open(filename,encoding="utf8")
    file = file.read()
    file = file.translate({ord(c): None for c in '1234567890#—.,-:!?"\'/«»„“();'})
    lines = file.split('\n')
    data = []
    for i in range(len(lines)):
        data.append(lines[i].split('\t'))
    X = list()
    for row in data:
        raw = row[0] + ' ' + row[1]
        parsed = list()
        for i in raw.split(' '):
            if i != '':
                parsed.append(i.lower())
        X.append(parsed)
    return X

classes = ['science', 'style', 'culture', 'life', 'economics', 'business', 'travel', 'forces', 'media', 'sport']
def classify(x,y,lines):
    res = list()
    debug = list()
    for line in lines:
        min_val = 9000000
        current_class = classes[0]
        for c in classes:
            tt = y[c]
            if tt < 10**(-7):
                tt = 10**(-7)
            temp = -log(tt)
            for w in line:
                try:
                    ttt = x[w][c]
                    if ttt < 10**(-7):
                        ttt = 10**(-7)
                    temp += -log(ttt)
                except KeyError:
                    continue
            if temp < min_val:
                current_class = c
                min_val = temp
        res.append(current_class)
        debug.append(min_val)
    return res, debug       

if __name__ == '__main__':
    with open('test.txt', 'w', encoding='utf8') as f:
        print("Start loading...")
        X, Y = aload('news_train.txt')
        x, y, count_w = learning(X, Y)
        print("Words count:",count_w)
        print("Start cleaning...")
        x, b, a = clean_x(x, count_w)
        print("Before: ",b," After: ", a)
        print("Start computing prob...")
        x, y = compute_prob(x,y)
        print("Start parsing test...")
        lines = parse_test("news_test.txt")
        print("Start classifying...")
        res, debug = classify(x,y,lines)
        print("Start outputing results...")
        for i in range(len(res)):
            f.write(res[i]+'\n')
    print('Success')
