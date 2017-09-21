
# TODO: 蜡烛图形态分析
import sys, os

def analyze(parsed):
    pass

def parse(file):
    for line in file:
        if line.startswith('@'):
            pass
        elif line.startswith('#'):
            c = line[1:].strip()
            print(c)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit()
    filename = sys.argv[1]
    if not os.path.exists(filename):
        exit()
    
    with open(filename) as file:
        parse(file)