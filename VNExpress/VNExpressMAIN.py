from bs4 import BeautifulSoup
import base64
import json
import time
import os
import requests
data_frame = dict()
"""
data_frame = {
    "url":{
        "context":"",
        "images": [
            {
                "url_img": "",
                "caption": ""
            },
            
        ]
        "section": "",
        "subsection": ""
    }
}
"""
#Ham lay context, anh va cap
def Get_Content_Img_Cap(main_link, page_content, page_img, page_cap):
    link_text = requests.get(main_link).text
    link_soup = BeautifulSoup(link_text, "html.parser")
    #Tieu de cua bai bao
    page_title = link_soup.find(class_='title-detail')
    if (page_title!=None):
        page_content.append(page_title.text.strip())
    #Phan mo dau bai bao
    page_description = link_soup.find('p', class_='description')
    if (page_description != None):
        string = ''.join(page_description.find_all(string=True, recursive=False))
        page_content.append(string)
    #Phan lay noi dung chinh co trong bai bao
    link_para = link_soup.find_all('p', class_='Normal')
    #Lay tat ca hinh anh chinh cua bai bao
    link_img_cap = link_soup.find_all('div', class_='fig-picture')
    if (link_para !=[]):
        for para in link_para:
            content = para.text.strip()
            page_content.append(content)
    #Co phan alt va data-src moi lay, con khong thi bo qua
    if (link_img_cap !=[]):
        for img_cap in link_img_cap:
            img = img_cap.find('img', attrs={'data-src': True, 'alt' : True})
            if (img!=None):
                page_img.append(img['data-src'])
                page_cap.append(img['alt'])
#Cac thong tin doc duoc se duoc dua vao file json o ham sau
def Create_Data_frame(main_link, page_content, page_img, page_cap, sec_name, subsec_name, ten_json_file):
    #data_frame duoc khai bao bien global, se duoc lam moi lien tuc o file json
    url = main_link
    data_frame[url] = {}
    data_frame[url]["context"] = page_content
    data_frame[url]["images"] = []
    cnt = 0
    for img in page_img:
        data_frame[url]["images"].append({"url_img": img,"caption": page_cap[cnt]})
        cnt += 1
    data_frame[url]["section"] = sec_name
    data_frame[url]["subsection"] = subsec_name
    file_path = os.path.join('D:\pythonProject\VNEJson', f'{ten_json_file}p.json')
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_frame, json_file, ensure_ascii=False, indent=4)
# Ham nay se la suon xu li cac context, anh va cap o moi trang
def Create_Data(hyperlink, ten_json_file):
    main_link = hyperlink
    page_content = []
    page_img = []
    page_cap = []
    # =====================================================================
    Get_Content_Img_Cap(main_link, page_content, page_img, page_cap)
    # =====================================================================
    if (page_img != []):
        Create_Data_frame(main_link, page_content, page_img, page_cap, muc.find('a')['title'], linh_vuc.find('a')['title'], ten_json_file)
"""
    - Co cac dong code lon cho moi chu de cua trang VNE
    - Dung lenh find_all cho tat ca cac tags li
    - Moi the li chua ten cac subsec can tim, va cac bai bao se duoc duyet het qua tung the li, bai bao co nhieu trang
    
"""
main_url = "https://vnexpress.net"
main_text = requests.get(main_url).text
main_soup = BeautifulSoup(main_text, "html.parser")

muc_luc = main_soup.find('ul', class_='parent').find_all('li') # Tim tat ca cac muc co tai trang chinh cua vnep
for muc in muc_luc:
    #Loai bo cac muc khong can thiet
    #if ( ( muc['class'][0] == 'home') or ( muc['class'][0] == 'newlest' ) or ( muc['class'][0]=='all-menu') or ( muc['class'][0]=='video') or ( muc['class'][0]=='podcasts') or ( muc['class'][0]=='gocnhin')):
     #   continue
    if (muc['class'][0]!='kinhdoanh'):
        continue
    ten_json_file = muc['class'][0]
    #lay duong link dan toi cac muc do
    link_muc = muc.find('a')['href']
    muc_url = f"https://vnexpress.net{link_muc}"
    #lay content
    print(muc_url)
    muc_text = requests.get(muc_url).text
    muc_soup = BeautifulSoup(muc_text, "html.parser")
    type_muc = muc_soup.find('ul', class_='ul-nav-folder')
    ptype_muc = type_muc.find_all('li')
    print("Cac link cua muc: ")
    #Bat dau xu li cac muc nho cua cac muc lon
    for linh_vuc in ptype_muc:
        link_linh_vuc = linh_vuc.find('a')['href']
        #cac trang duoi day khong chua bai bao thong thuong nen skip
        if ('https' in link_linh_vuc or 'trac-nghiem' in link_linh_vuc or 'hen-ho' in link_linh_vuc
        or 'cam-nang' in link_linh_vuc or 'thi-bang-lai' in link_linh_vuc or 'cooking' in link_linh_vuc
        or 'du-lieu-bong-da' in link_linh_vuc or 'tra-cuu-dai-hoc' in link_linh_vuc or ('dien-dan' in link_linh_vuc and 'oto-xe-may' in link_linh_vuc)
        or 'smart-buy' in link_linh_vuc or 'du-an' in link_linh_vuc or 'tu-van' in link_linh_vuc):
            continue
        linh_vuc_url = f"https://vnexpress.net{link_linh_vuc}"
        print(linh_vuc_url)
        print("********")
        linh_vuc_text = requests.get(linh_vuc_url).text
        linh_vuc_soup = BeautifulSoup(linh_vuc_text, "html.parser")
        multi_pages = linh_vuc_soup.find('div', class_='button-page flexbox')
        #Xu li multiple_pages
        if (multi_pages != None):
            page = 1
            while (page<=20):
                page_lv = f"https://vnexpress.net{link_linh_vuc}-p{page}"
                page_text = requests.get(page_lv).text
                page_soup = BeautifulSoup(page_text, "html.parser")
                #Lay tat ca cac link cua bai co tai trang hien hanh
                page_tintuc = page_soup.find_all(class_='title-news')
                #phong truoc hop cac muc dac biet k doc duoc tin thi skip
                if (page_tintuc!=[]):
                    for ban_tin in page_tintuc:
                        if (ban_tin.find('a') !=None):
                            print(ban_tin.find('a')['href'])
                            if ('video' not in ban_tin.find('a')['href'] and 'startup' not in ban_tin.find('a')['href']):
                                Create_Data(ban_tin.find('a')['href'], ten_json_file)
                page+=1
                #toi page cuoi cung khong the doc duoc nua thi break
                check = page_soup.find('div', class_='button-page flexbox')
                if (check != None):
                    if (check.find('a', class_='btn-page next-page disable') != None or check.find('a', class_='btn-page inactive') != None):
                        break


        else: #do trang do khong thuc hien theo kieu multiple_pages thi lam nhu vay
            tin_tuc = linh_vuc_soup.find_all(class_='title-news')
            if (tin_tuc != []):
                for ban_tin in tin_tuc:
                    if (ban_tin.find('a') !=None):
                        print(ban_tin.find('a')['href'])
                        Create_Data(ban_tin.find('a')['href'], ten_json_file)
    print("==================")









