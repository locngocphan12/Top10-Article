from bs4 import BeautifulSoup
import requests
import os
import json
"""file_path = os.path.join('D:\pythonProject\LAODONGJson','thoi-su.json')
with open(file_path, 'r', encoding='utf-8') as json_file:
    data_frame = json.load(json_file)"""
data_frame = {}
def Get_Content_Img_Cap(link, page_content, page_img, page_cap):
    link_text = requests.get(link).text
    link_soup = BeautifulSoup(link_text, "html.parser")
    title = link_soup.find('div', class_='chappeau')
    if title!= None:
        page_content.append(title.text.strip())
    list_para = link_soup.find('div', class_='art-body')
    if list_para != None:
        paragraphs = list_para.find_all(['p'])
        img_caps = list_para.find_all('figure')
        if paragraphs !=[]:
            for p in paragraphs:
                content = p.text.strip()
                page_content.append(content)
        if (img_caps!=[]):
            for img_cap in img_caps:
                img = img_cap.find('img', attrs = {'src':True})
                cap = img_cap.find('figcaption')
                if (img != None and cap != None):
                    page_img.append(img['src'])
                    page_cap.append(cap.text.strip())
def Create_Data_frame(link, page_content, page_img, page_cap, muc, linh_vuc, ten_json_file):
    url = link
    data_frame[url] = {}
    data_frame[url]["context"] = page_content
    data_frame[url]["images"] = []
    cnt = 0
    for img in page_img:
        data_frame[url]["images"].append({"url_img": img, "caption": page_cap[cnt]})
        cnt += 1
    data_frame[url]["section"] = muc
    data_frame[url]["subsection"] = linh_vuc
    file_path = os.path.join('D:\pythonProject\LAODONGJson', f'{ten_json_file}p.json')
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_frame, json_file, ensure_ascii=False, indent=4)
def Create_Data(link, ten_json_file, muc, linh_vuc):
    page_content = []
    page_img = []
    page_cap = []
    # =====================================================================
    Get_Content_Img_Cap(link, page_content, page_img, page_cap)
    # =====================================================================
    if (page_img != []):
        Create_Data_frame(link, page_content, page_img, page_cap, muc,
                          linh_vuc, ten_json_file)


main_url = 'https://laodong.vn'
main_text = requests.get(main_url).text
main_soup = BeautifulSoup(main_text,'html.parser')
menu = main_soup.find('div',class_='main-menu').find('ul',class_ = 'lst-mn')
muc = menu.find_all('li', class_='item')
list_link = dict()
for noi_dung in muc:
    link_muc = noi_dung.find('a', class_='link')
    if (link_muc!=None):
        link_muc = link_muc['href']
        if ('media' in link_muc):
            continue
        muctext = noi_dung.find('a', class_='link').text
        list_link[muctext] = link_muc
menu = main_soup.find('div',class_='main-menu').find('div',id = 'lst-more-menu')
muc = menu.find_all('div', class_='blk')
for noi_dung in muc:
    link_muc = noi_dung.find('a', class_='child-item')
    if (link_muc != None):
        link_muc = link_muc['href']
        muctext = noi_dung.find('a', class_='child-item').text
        list_link[muctext] = link_muc
#print(list_link)

for i in list_link:
    print(list_link[i])
    ten_file_json = list_link[i][list_link[i].rfind('/')+1:]
    if (ten_file_json!='thoi-su'):
        continue
    muc_text = requests.get(list_link[i]).text
    muc_soup = BeautifulSoup(muc_text, "html.parser")
    childs = muc_soup.find('div', class_='children-cats').find('div', class_='list')
    if childs != None:
        menu_childs = childs.find_all('h3')
    if menu_childs != []:
        for child in menu_childs:
            link_child = child.find('a')['href']
            lvtext = child.find('a').text
            link_child = f'https://laodong.vn{link_child}'
            """if ('' in link_child):
                continue"""
            page = 1
            while(True):
                link_pc = f"{link_child}?page={page}"
                page_text = requests.get(link_pc).text
                page_soup = BeautifulSoup(page_text, 'html.parser')
                pos_news = page_soup.find('div', class_='p-lst-articles')
                if pos_news == None:
                    break
                news = pos_news.find_all('article')
                if (news != None):
                    for atc in news:
                        link_atc = atc.find('div', class_='pr')
                        if link_atc != None:
                            link_atc = atc.find('a')['href']
                            print(link_atc," ",page)
                            Create_Data(link_atc, ten_file_json, muctext, lvtext)
                pagination = pos_news.find('div', class_='pagination-md-1')
                if pagination == None:
                    break
                page += 1