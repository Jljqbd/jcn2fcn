import json # 导入json库用于把列表保存成.json格式
import pypinyin
from tqdm import trange
# import sys

def get_stroke(c):
    # 如果返回 0, 则也是在unicode中不存在kTotalStrokes字段
    strokes = []
    with open('strokes.txt', 'r') as fr:
        for line in fr:
            strokes.append(int(line.strip()))
    unicode_ = ord(c)
    if 13312 <= unicode_ <= 64045:
        return strokes[unicode_-13312]
    elif 131072 <= unicode_ <= 194998:
        return strokes[unicode_-80338]
    else:
        return None
        #print("c should be a CJK char, or not have stroke in unihan data.")
        # can also return 0
# 带声调的(默认)
def yinjie(word):
    # s = ''
    # heteronym=True开启多音字
    #for i in pypinyin.pinyin(word, heteronym=True):
    #    s = s + ''.join(i) + " "
    return pypinyin.pinyin(word, heteronym=True)[0][0]
def create_char():
    characters = [] # 创建一个列表用于保存汉字字符
    for i in range(129, 255):
        s = bytes([i])
        for x in range(64, 255):
            s += bytes([x])
            try:
                c = s.decode("gbk")
            except:
                break
            characters.append(c)
            #print(c, end="\t") # 打印结果
            s = bytes([i])
    return characters
'''
    print(len(characters)) # 打印结果数量
    '''
def write_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
def pinyin_json(word_list):
    #将word_list的文字转化为对应的拼音集
    pinyin_list = []
    list_len = len(word_list)
    for i in trange(0, list_len):
        pinyin_list.append(yinjie(word_list[i]))
    write_file('pinyin.json',pinyin_list)
    print('拼音集合写入完成...')
def stroke_json(word_list):
    #将word_list的文字转化为对应的笔画集
    stroke_list = []
    list_len = len(word_list)
    for i in trange(0, list_len):
        gs = get_stroke(word_list[i])
        if gs != None:
            stroke_list.append(gs)
        else:
            stroke_list.append(0)
    write_file('stroke.json',stroke_list)
    print('笔画集合写入完成...')
def read_json2list(filename):
    f = open(filename, 'r', encoding='UTF-8')
    content = f.read()
    a = json.loads(content)
    f.close()
    return a
def main():
    '''
    str_start = ""
    #获取命令行参数
    for i in range(1, len(sys.argv)):
        str_start += sys.argv[i]
    '''
    # 创建中文字符集
    char_list = create_char()
    #读取pinyin
    pl = read_json2list('pinyin.json')
    #读取笔画
    sl = read_json2list('stroke.json')
    # 输入要转换的原始字符
    str_start = input('请您输入要转换的文字: ')
    str_end = ''
    str_len = len(str_start)
    list_len = len(char_list)
    for i in trange(0, str_len):
        now_char_len = get_stroke(str_start[i]) #最后要修改的文字笔画数，初始时原本文字的笔画数
        edit_str = str_start[i] #最后要修改的文字，初始是原本的文字
        #print('第%c/%c个文字开始转换'%(str(i+1), str(str_len)))
        temp_yj = yinjie(str_start[i])
        for j in trange(0, list_len):
            gs = sl[j] #笔画数
            if temp_yj == pl[j] and gs != None and gs > now_char_len: #相同的音节且找到了比他大的笔画数的字
                now_char_len = gs
                edit_str = char_list[j]
        str_end += edit_str
    print('原本的文字为:%s\n转换后的文字为:%s\n' %(str_start, str_end))  
    input('')        
# step1
'''
char_list = create_char()
pinyin_json(char_list)
stroke_json(char_list)
'''
#
main()


