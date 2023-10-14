from bs4 import BeautifulSoup
import json
import os
import requests
"""file_path = os.path.join('D:\pythonProject\DANTRIJson','bat-dong-san.json')
with open(file_path, 'r', encoding='utf-8') as json_file:
    data_frame = json.load(json_file)"""
data_frame = {}
def Get_Content_Img_Cap(link, page_content, page_img, page_cap):
    link_text = requests.get(link).text
    link_soup = BeautifulSoup(link_text, "html.parser")
    title = link_soup.find(class_='singular-sapo')
    if title!= None:
        page_content.append(title.text.strip())
    list_para = link_soup.find(class_='singular-content')
    if list_para != None:
        paragraphs = list_para.find_all(['p','h4'])
        img_caps = list_para.find_all('figure')
        if paragraphs !=None:
            for p in paragraphs:
                content = p.text.strip()
                page_content.append(content)
        if (img_caps!=None):
            for img_cap in img_caps:
                img = img_cap.find('img', attrs = {'data-src':True})
                cap = img_cap.find('figcaption')
                if (img != None and cap != None):
                    page_img.append(img['data-src'])
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
    file_path = os.path.join('D:\pythonProject\DANTRIJson', f'{ten_json_file}p.json')
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

main_url = 'https://dantri.com.vn'
main_text = requests.get(main_url).text
main_soup = BeautifulSoup(main_text,'html.parser')
menu = main_soup.find('div',class_='nav-full bg-wrap').find('ol',class_ = 'nf-menu')
muc = menu.find_all('li')
for noi_dung in muc:
    link_muc = noi_dung.find('a')['href']
    if (link_muc.count('/') == 1):
        #print(link_muc)
        #link_muc[link_muc.find('/')+1:link_muc.find('.htm')]
        muc_url = f'https://dantri.com.vn{link_muc}'
        muctext = noi_dung.find('a').text
    else:
        continue
    if (link_muc[link_muc.find('/')+1:link_muc.find('.htm')] != 'o-to-xe-may'):
        continue
    ten_file_json = link_muc[link_muc.find('/')+1:link_muc.find('.htm')]
    print(muc_url)
    muc_text = requests.get(muc_url).text
    muc_soup = BeautifulSoup(muc_text, "html.parser")
    childs = muc_soup.find('ol', class_='menu-second child')
    menu_childs = childs.find_all('li')
    for child in menu_childs:
        link_child = child.find('a')['href']
        if link_child.count('/') > 2:
            continue
        print(link_child)
        child_url = f'https://dantri.com.vn{link_child}'
        lvtext = child.find('a').text
        if 'ung-thu' in child_url or 'song-khoe' in child_url or 'dich-vu-y-te-quoc-te' in child_url or 'suc-khoe-chu-dong' in child_url:
            sub_text = requests.get(child_url).text
            sub_soup = BeautifulSoup(sub_text,"html.parser")
            sub_muc = sub_soup.find('ol', class_="menu-second child")
            menu_sub = sub_muc.find_all('li')
            if (menu_sub!=[]):
                for menu in menu_sub:
                    menu_link = menu.find('a')['href']
                    menu_url = f'https://dantri.com.vn{menu_link}'
                    # ------------------------
                    spe_text = requests.get(menu_url).text
                    spe_soup = BeautifulSoup(spe_text, 'html.parser')
                    bang = spe_soup.find('article', class_='article grid')
                    if (bang != None):
                        news = bang.find_all(class_='article-title')
                        if (news != []):
                            for new in news:
                                atcn = new.find('a')
                                if atcn != None:
                                    atcn = new.find('a')['href']
                                    link = f"https://dantri.com.vn{atcn}"
                                    print(link)
                                    Create_Data(link, ten_file_json, muctext, lvtext)
                    cot = spe_soup.find('article', class_='article column')
                    if (cot != None):
                        news = cot.find_all(class_='article-title')
                        if (news != []):
                            for new in news:
                                atcn = new.find('a')
                                if atcn != None:
                                    atcn = new.find('a')['href']
                                    link = f"https://dantri.com.vn{atcn}"
                                    print(link)
                                    Create_Data(link, ten_file_json, muctext, lvtext)
                    # ------------------------
                    page = 1
                    while (page <= 30):
                        print(page)
                        link_pc = f"{child_url[:child_url.find('.htm')]}/trang-{page}.htm"
                        page_text = requests.get(link_pc).text
                        page_soup = BeautifulSoup(page_text, 'html.parser')
                        pos_news = page_soup.find('div', class_='article list')
                        if (pos_news == None):
                            continue
                        news = pos_news.find_all(class_='article-title')
                        if (news != []):
                            for atc in news:
                                link_atc = atc.find('a')
                                if link_atc != None:
                                    link_atc = atc.find('a')['href']
                                    link = f"https://dantri.com.vn{link_atc}"
                                    Create_Data(link, ten_file_json, muctext, lvtext)
                        page += 1
                        if (page_soup.find('a', class_='page-item next') == None):
                            break
            continue
        #------------------------
        spe_text = requests.get(child_url).text
        spe_soup = BeautifulSoup(spe_text,'html.parser')
        bang = spe_soup.find('article', class_='article grid')
        if (bang != None):
            news = bang.find_all(class_='article-title')
            if (news != []):
                for new in news:
                    atcn = new.find('a')
                    if atcn != None:
                        atcn = new.find('a')['href']
                        link = f"https://dantri.com.vn{atcn}"
                        print(link)
                        Create_Data(link, ten_file_json, muctext, lvtext)
        cot = spe_soup.find('article',class_='article column')
        if (cot != None):
            news = cot.find_all(class_='article-title')
            if (news != []):
                for new in news:
                    atcn = new.find('a')
                    if atcn != None:
                        atcn = new.find('a')['href']
                        link = f"https://dantri.com.vn{atcn}"
                        print(link)
                        Create_Data(link, ten_file_json, muctext, lvtext)
        #------------------------
        page = 1
        while(page<=30):
            print(page)
            link_pc = f"{child_url[:child_url.find('.htm')]}/trang-{page}.htm"
            page_text = requests.get(link_pc).text
            page_soup = BeautifulSoup(page_text,'html.parser')
            pos_news = page_soup.find('div', class_='article list')
            if (pos_news == None):
                continue
            news = pos_news.find_all(class_='article-title')
            if (news != []):
                for atc in news:
                    link_atc = atc.find('a')
                    if link_atc != None:
                        link_atc = atc.find('a')['href']
                        link = f"https://dantri.com.vn{link_atc}"
                        Create_Data(link, ten_file_json, muctext, lvtext)
            page += 1
            if (page_soup.find('a', class_='page-item next') == None):
                break
