# coding: utf-8

import sys, os.path, re, csv
import pandas as pds
import numpy as np
import json

# Defining url of Aozora-bunko and local work directory.
base_url = "http://www.aozora.gr.jp/"
data_dir = "./"
aozora_dir = data_dir + "csv_data/"
log_dir = aozora_dir + "log/"

# The project uses csv with the name of author and his/her url in Aozora-bunko
# target_author_file = data_dir + "target_author.csv"

# auth_target = []
# with open(target_author_file,"r") as f:
#     reader = csv.reader(f)
#     for row in reader:
#         auth_target.append(row)
# auth_target
#
# print (auth_target)

f = open("train_aozora_data.json", 'r')
j = open("aozora_contents.json", 'r')
k = open("aozora_authors.json", 'r')
l = open("aozora_titles.json", 'r')
m = open("train_q.json")

train_aozora_data = json.load(f)
aozora_contents = json.load(j)
aozora_authors = json.load(k)
aozora_titles = json.load(l)
train_q = json.load(m)

# print(aozora_contents['content_11969'])

content = []

for i in train_aozora_data:

    novel = i['novels']
    tmp_list = [i['author_id']]
    for j in novel:
        tmp_list.append(j['content_id'])

    content.append(tmp_list)


auth_target=[]
for i in range(len(content)):
    auth_target.append(content[i][0])

# for number in range(len(content)):
#     content_idx=number
#     txt_list=[]
#     for j in range(len(content[content_idx])-1):
#         txt_list.append(aozora_contents[content[content_idx][j+1]])
# print(txt_list)


# Make directories for authors and csv, text extraction, and utf converted directories for them.

def make_workdir(aozora_dir=aozora_dir, auth_target=auth_target):
    if not os.path.exists(aozora_dir):
        try:
            os.makedirs(aozora_dir)
            print ("make: " + aozora_dir)
        except OSError as e:
            print (e)

    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
            print ("make: " + log_dir)
        except OSError as e:
            print (e)

    for w in auth_target:
        auth_dir = '{}{}/'.format(aozora_dir, w)
        if not os.path.exists(auth_dir):
            try:
                os.makedirs(auth_dir)
                print ("make: " + auth_dir)
            except OSError as e:
                print (e)
        if not os.path.exists(auth_dir + "csv/"):
            try:
                os.makedirs(auth_dir + "csv/")
                print ("make: " + auth_dir + "csv/")
            except OSError as e:
                print (e)
        if not os.path.exists(auth_dir + "ext/"):
            try:
                os.makedirs(auth_dir + "ext/")
                print ("make: " + auth_dir + "ext/")
            except OSError as e:
                print (e)
        if not os.path.exists(auth_dir + "utf/"):
            try:
                os.makedirs(auth_dir + "utf/")
                print ("make: " + auth_dir + "utf/")
            except OSError as e:
                print (e)



# Downloads all the zip files from author's written pieces.

# def download_zip(auth_target=auth_target):
#     for w in auth_target[1:]:
#         print ("starting %s" % w[0])
#         auth_dir = '{}{}/'.format(aozora_dir, w[0])
#         url = w[1]
#
#         html = urlopen(url)
#
#         if html.getcode() == 200:
#             soup = BeautifulSoup(html, "lxml")
#             piece_list = soup.find("ol")
#             piece_links = piece_list.find_all("a")
#             piece_links_np = np.array([["datetime","title","url","zip"]])
#             for i in piece_links:
#                 title = i.string
#                 link = base_url + i["href"].replace("../", "")
#                 if "cards" in link:
#                     print ("    piece: %s for %s" % (title, link))
#                     piece_html = urlopen(link)
#                     if piece_html.getcode() == 200:
#                         soup = BeautifulSoup(piece_html, "lxml")
#                         zip_part = soup.find_all("a", href=re.compile(".zip"))
#                         if zip_part != []:
#                             zip_file = zip_part[0]["href"]
#                             zip_url = urllib.parse.urljoin(link, zip_file)
#                             print ("        zip_url: %s" % zip_url)
#                             now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
#                             tmp = np.array([[now, title, link, zip_url]])
#                             piece_links_np = np.vstack((piece_links_np, tmp))
#
#                             file_name = os.path.basename(zip_url)
#                             file_full_path = '{}{}'.format(auth_dir, file_name)
#                             urllib.request.urlretrieve(zip_url, filename=file_full_path)
#
#             piece_links_pds = pds.DataFrame(piece_links_np[1:,:], columns=piece_links_np[0,:])
#             piece_links_pds.to_csv(log_dir + w[0] + '_dl_log.csv', quoting=csv.QUOTE_ALL)
#         print ("finished %s" % w[0])




# Extract zip files to txt files. Its character encoding is in SHIfT-JIS.

# def zip_extract(auth_target=auth_target):
#     log_np = np.array([["datetime", "author", "zip"]])
#     for w in auth_target[1:]:
#         auth_dir = '{}{}/'.format(aozora_dir, w[0])
#         ext_dir = '{}{}'.format(auth_dir, "ext/")
#         files = os.listdir(auth_dir)
#         for file in files:
#             if "zip" in file:
#                 file_fullpath = auth_dir + file
#                 with zipfile.ZipFile(file_fullpath, 'r') as zip_file:
#                     zip_file.extractall(path=ext_dir)
#                     now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
#                     tmp = np.array([[now, w[0], zip_file]])
#                     log_np = np.vstack((log_np, tmp))
#                     print ("extracted: " + str(zip_file))
#         zip_ext_pds = pds.DataFrame(log_np[1:,:], columns=log_np[0,:])
#         zip_ext_pds.to_csv(log_dir + w[0] + '_zip_log.csv', quoting=csv.QUOTE_ALL)




# Making txt files with SHIFT-JIS converted to UTF-8.

# def convert_sjis_to_utf8(auth_target=auth_target):
#     log_np = np.array([["datetime", "author", "file"]])
#     for w in auth_target[1:]:
#         auth_dir = '{}{}/'.format(aozora_dir, w[0])
#         ext_dir = '{}{}'.format(auth_dir, "ext/")
#         utf_dir = '{}{}'.format(auth_dir, "utf/")
#         files = os.listdir(ext_dir)
#         for file in files:
#             if "txt" in file:
#                 file_name = ext_dir + file
#                 save_name = utf_dir + file
#                 fout = codecs.open(file_name, 'r', 'shift_jis')
#                 fsave = codecs.open(save_name, 'w+', 'utf-8')
#                 try:
#                     for row in fout:
#                         fsave.write(row)
#                 except Exception as e:
#                     print (file + "gets exception: " + str(type(e)))
#                 finally:
#                     fout.close()
#                     fsave.close()
#                     print ("converted: " + save_name)
#                     now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
#                     tmp = np.array([[now, w[0], file]])
#                     log_np = np.vstack((log_np, tmp))
#         convert_pds = pds.DataFrame(log_np[1:,:], columns=log_np[0,:])
#         convert_pds.to_csv(log_dir + w[0] + '_cvt_log.csv', quoting=csv.QUOTE_ALL)
#
#


# Cleansing UTF-8 texts and convert them to files to CSV.

def data_cleanse(auth_target=auth_target):
    for w in content:
        print ("starting: " + w[0])
        auth_dir = '{}{}/'.format(aozora_dir, w[0])
        ext_dir = '{}{}'.format(auth_dir, "ext/")
        utf_dir = '{}{}'.format(auth_dir, "utf/")
        csv_dir = '{}{}'.format(auth_dir, "csv/")
        files = os.listdir(utf_dir)
        for content_idx in range(len(w)-1):
            # print ("     file: " + file)
            # file_name = utf_dir + file
            np_lines = np.array([["auth","piece","line"]])
            # f = open(file_name, 'r')
            #
            # lines = f.read()
            # f.close

            lines=aozora_contents[w[content_idx+1]]

            lines = lines.replace(u'。', '。\n')
            lines = lines.split('\n')

            ruby = re.compile(u'\《.+?\》')
            chuki = re.compile(u'\［.+?\］')
            zen_sp = re.compile(u'　')
            zen_sp2 = re.compile(u'\u3000')

            for line in lines:
                line_mod = ruby.sub("", line)
                line_mod = chuki.sub("", line_mod)
                line_mod = zen_sp.sub("", line_mod)
                line_mod = zen_sp2.sub("", line_mod)
                np_tmp = np.array([[w[0], content_idx, line_mod]])
                np_lines = np.vstack((np_lines, np_tmp))

            s_line = 1
            e_line = len(lines)
            np_lines_cut = np_lines[s_line:e_line,:]

            lines_pds = pds.DataFrame(np_lines_cut, columns=np_lines[0,:])
            lines_pds.to_csv(csv_dir + w[content_idx+1] + '.csv', quoting=csv.QUOTE_ALL)

        print ("finished: " + w[0])



if __name__ == "__main__":
    make_workdir(aozora_dir, auth_target)
    # download_zip(auth_target)
    # zip_extract(auth_target)
    # convert_sjis_to_utf8(auth_target)
    data_cleanse(auth_target)


print ("finished")

