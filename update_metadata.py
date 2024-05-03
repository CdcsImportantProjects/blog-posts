import os
import json
import random
import time
GLOBAL_index = []
lines = []
def readFile(file):
    f_obj = open(f"./posts/{file}","r")
    content = f_obj.read()
    f_obj.close()
    return content
def writeFile(file,c):
    f_obj = open(file,"x")
    content = f_obj.write(c)
    f_obj.close()
    return content

def getKeywords(file_c):
    valid_char = "abcdefghijklmnopqrstuvwxyz "
    lower_s = file_c.lower()
    t_str_1 = ""
    for char in lower_s:
        if char in valid_char:
            t_str_1 = t_str_1 + char
        else:
            t_str_1 = t_str_1 + " "
    arr = t_str_1.split(" ")
    n_arr = []
    for item in arr:
        if item != "":
            n_arr.append(item)
    c_dic = {}
    for item in n_arr:
        try:
            c_dic[item] += 1
        except:
            c_dic[item] = 1
    c_dic_sort_rev = {k: v for k, v in sorted(c_dic.items(), key=lambda item: item[1])}
    c_dic_sort = dict(reversed(c_dic_sort_rev.items()))
    top_words = []
    top_word_id = 0
    for word in c_dic_sort:
        if top_word_id == 8:
            break
        if len(word) >= 5:
            top_words.append(word)
            top_word_id += 1
    return top_words
def getTitle(file_c):
    for line in file_c.split("\n"):
        if len(line) > 0:
            lines.append(line)
        if line.startswith("# "):
            return line.strip("# ")
            break
    return None
def getChapters(file_c):
    chapters = []
    for line in file_c.split("\n"):
        if line.startswith("## "):
            chapters.append(line.strip("## "))
    return chapters
def getFilename(full_file_name):
    filename = []
    arr = full_file_name.split(".")
    idx = 0
    for part in arr:
        if idx == len(arr)-1 and len(arr) != 1:
            break
        filename.append(part)
        idx += 1
    return ".".join(filename)
for folder in os.walk("./posts"):
    for file in folder[2]:

        try:
            os.mkdir("./metadata")
        except:
            print("metadata folder exists!")
        try:
            os.mkdir("./metadata/posts")
        except:
            print("posts folder exists!")
        try:
            os.mkdir(f"./metadata/posts/{getFilename(file)}")
        except:
            print("post data folder exists!")
            print(getFilename(file))
        try:
            os.mkdir(f"./metadata/search_index")
        except:
            print("search index exists!")
        if not os.path.exists(f"./metadata/posts/{getFilename(file)}/data.json"):
            writeFile(f"./metadata/posts/{getFilename(file)}/data.json",json.dumps({
            "id":getFilename(file),
            "title":getTitle(readFile(file)),
            "chapters":getChapters(readFile(file)),
            "file_url":f"https://raw.githubusercontent.com/CdcsImportantProjects/blog-posts/main/posts/{file}",
            "posted_at":time.time()
        }))
        GLOBAL_index.append({
            "id":getFilename(file),
            "title":getTitle(readFile(file)),
            "keywords":getKeywords(readFile(file)),
        })
writeFile("./metadata/search_index/index.json",json.dumps(GLOBAL_index))
hp_randomPosts = []
for i in range(5):
    hp_randomPosts.append(random.choice(GLOBAL_index))
homepage = {
    "random_line":random.choice(lines),
    "posts":hp_randomPosts
}
writeFile("./homepage.json",json.dumps(homepage))    
        
