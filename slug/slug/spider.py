#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'Package_name' __author__ = '欧冠斌'
__mtime__ = '2020/7/11'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import math
import os
import time
import xlwt
import pandas as pd
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

informations = []
chrome_options = webdriver.ChromeOptions()
# 使用headless无界面浏览器模式
# chrome_options.add_argument('--headless')#增加无界面选项
chrome_options.add_argument('--disable-gpu')  # 如果不加这个选项，有时定位会出现问题
chrome_options.add_argument(
    '--user-data-dir=C:\\Users\\ouguan\\AppData\\Local\\Google\\Chrome\\User Data\\Default')  # 设置成用户自己的数据目录
# 设置文件保存地址
prefs = {'profile.default_content_settings.popups': 0,
         'download.default_directory': 'E:\\downloadfile\\espacenet\\document'}
chrome_options.add_experimental_option('prefs', prefs)

# 启动浏览器，获取网页源代码
browser = webdriver.Chrome(chrome_options=chrome_options)
mainUrl = "https://www.epo.org/index.html"
browser.get(mainUrl)


def spider():
    browser.implicitly_wait(30)
    # print(f"browser text = {browser.page_source}")
    # WebDriverWait(browser,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.mnav')))
    WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.ID, 'searchPatentsBtn')))
    browser.find_element_by_id('search').send_keys('us')
    time.sleep(3)
    browser.find_element_by_id('searchPatentsBtn').click()
    # print(browser.find_element_by_id('searchPatentsBtn'))
    # js ='document.getElementById("searchPatentsBtn").click()'  # js点击元素
    # browser.execute_script(js)# 执行js语句
    # time.sleep(10)
    browser.switch_to_window(browser.window_handles[1])
    time.sleep(20)
    publications_list_str = browser.find_element_by_class_name('publications-list--mYtsKGTt')
    WebDriverWait(browser, 30).until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR, '.item__section--3xemirAV')))
    num_str = browser.find_element_by_class_name('publications-list-header__tooltip-wrapper--37_PQZvC').text
    num_str1 = num_str.replace(" ","");
    num = re.findall('\d+',num_str1)[0]

    #link_len_list = []
    while True:
        browser.execute_script('var q=document.getElementsByClassName("publications-list--mYtsKGTt")[0].scrollTo(0,1000000)')
        time.sleep(3)
        #html = browser.page_source
        #html = browser.HTML(html.encode("utf-8", 'ignore'))
        publications_list = publications_list_str.find_elements_by_xpath("//section")
        # print(title, '----------------2------------------')
        # for item in publications_list:
        #     print(item)

        link_len = len(publications_list)
        print(link_len)
        #link_len_list.append(link_len)
        if link_len > 1000:
            break
            # print(link_len_list[-1])
            # print(link_len_list[-2])
            # print('----------------')
            # if link_len_list[-1] == link_len_list[-2]:
            #     print('渲染完成')
            #     break
    publications_list = publications_list_str.find_elements_by_xpath("//section")

    for publication in publications_list:
        item = {}
        publication.click()
        # publications_list[0].click()
        # WebDriverWait(browser,30).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR,'.biblio__data-section--UREfiFr')))
        # 详情页
        WebDriverWait(browser, 60).until(
            EC.visibility_of(browser.find_element(by=By.ID, value='more-options-selector--publication-header')))
        publication_detail = browser.find_element_by_css_selector('[class="details details--cpiiWz68"]')
        # 下载按钮
        download_btn = publication_detail.find_element_by_id('more-options-selector--publication-header')
        # 下载文档
        download_btn.click()
        time.sleep(3)
        download = browser.find_element_by_xpath("//section[text()='Download']")
        isDisable = download.get_attribute("aria-disabled")
        if isDisable == "false":
            browser.find_element_by_xpath("//section[text()='Download']").click()
            browser.find_element_by_xpath("//li[text()='Original document']").click()
        else:
            browser.find_element_by_id("simple-dropdown").click()
        # 项目信息
        item["title"] = browser.find_element_by_css_selector('[class="h4--19TXYMyq"]').text
        bibliography = publication_detail.find_element_by_class_name('biblio__data-section--UREfiFrz')
        item["applicants"] = bibliography.find_element_by_id('biblio-applicants-content').text
        if isElementExist(bibliography,
                          'biblio-inventors-content'):
            item["inventors"] = bibliography.find_element_by_id('biblio-inventors-content').text
        else:
            item["inventors"] = "none"
        item["classifications_ipc"] = bibliography.find_element_by_id('biblio-international-content').text
        item["classifications_cpc"] = bibliography.find_element_by_id('biblio-cooperative-content').text
        item["priorities"] = bibliography.find_element_by_id('biblio-priority-numbers-content-0').text
        item["applicant_num"] = bibliography.find_element_by_id('biblio-application-number-content').text
        item["publication"] = bibliography.find_element_by_id('biblio-publication-number-content').text
        item["publish_as"] = bibliography.find_element_by_id('biblio-also-published-as-content').text
        item["document"] = "none"
        informations.append(item)
    time.sleep(1200)
    browser.quit()


def spider2():
    browser.implicitly_wait(30)
    # print(f"browser text = {browser.page_source}")
    # WebDriverWait(browser,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.mnav')))
    WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.ID, 'searchPatentsBtn')))
    browser.find_element_by_id('search').send_keys('us')
    time.sleep(3)
    browser.find_element_by_id('searchPatentsBtn').click()
    # print(browser.find_element_by_id('searchPatentsBtn'))
    # js ='document.getElementById("searchPatentsBtn").click()'  # js点击元素
    # browser.execute_script(js)# 执行js语句
    # time.sleep(10)
    browser.switch_to_window(browser.window_handles[1])
    time.sleep(20)

    WebDriverWait(browser, 30).until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR, '.item__section--3xemirAV')))
    num_str = browser.find_element_by_class_name('publications-list-header__tooltip-wrapper--37_PQZvC').text
    num_str1 = num_str.replace(" ","");
    num = re.findall('\d+',num_str1)[0]
    step = 500
    cel_num = math.ceil(int(num)/step)
    start_num = 0
    for i in range(1,cel_num):
        start_num = 1 + (i-1)*step
        end_num = start_num+step -1
        if end_num > int(num):
            end_num = int(num)
        browser.find_element_by_id("more-options-selector--publication-list-header").click()
        time.sleep(3)
        download = browser.find_element_by_xpath("//section[text()='Download']")
        isDisable = download.get_attribute("aria-disabled")
        if isDisable == "false":
            browser.find_element_by_xpath("//section[text()='Download']").click()
            browser.find_element_by_xpath("//li[text()='List (xlsx)']").click()
            min_num = browser.find_elements_by_class_name("download-modal__input--24vDx60I")[0]
            max_num = browser.find_elements_by_class_name("download-modal__input--24vDx60I")[1]
            download_btn = browser.find_element_by_xpath("//button[text()='Download']")
            js = 'document.getElementsByClassName("download-modal__input--24vDx60I")[1].setAttribute("max","'+str(end_num)+'");'
            js2 = 'document.getElementsByClassName("download-modal__input--24vDx60I")[1].setAttribute("value","'+str(end_num)+'");'
            browser.execute_script(js)
            browser.execute_script(js2)
            min_num.clear()
            min_num.send_keys(start_num)
            #max_num.clear()
            #max_num.send_keys(end_num)
            time.sleep(2)
            download_btn.click()
        else:
            browser.find_element_by_id("simple-dropdown").click()
        time.sleep(30)


def download_doc():
    publications_list_str = browser.find_element_by_class_name('publications-list--mYtsKGTt')
    publications_list = publications_list_str.find_elements_by_xpath("//section")

    for publication in publications_list:
        item = {}
        publication.click()
        # publications_list[0].click()
        # WebDriverWait(browser,30).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR,'.biblio__data-section--UREfiFr')))
        # 详情页
        WebDriverWait(browser, 60).until(
            EC.visibility_of(browser.find_element(by=By.ID, value='more-options-selector--publication-header')))
        publication_detail = browser.find_element_by_css_selector('[class="details details--cpiiWz68"]')
        # 下载按钮
        download_btn = publication_detail.find_element_by_id('more-options-selector--publication-header')
        # 下载文档
        download_btn.click()
        time.sleep(3)
        download = browser.find_element_by_xpath("//section[text()='Download']")
        isDisable = download.get_attribute("aria-disabled")
        if isDisable == "false":
            browser.find_element_by_xpath("//section[text()='Download']").click()
            browser.find_element_by_xpath("//li[text()='Original document']").click()
        else:
            browser.find_element_by_id("simple-dropdown").click()
        # 项目信息
        item["title"] = browser.find_element_by_css_selector('[class="h4--19TXYMyq"]').text
        bibliography = publication_detail.find_element_by_class_name('biblio__data-section--UREfiFrz')
        item["applicants"] = bibliography.find_element_by_id('biblio-applicants-content').text
        if isElementExist(bibliography,
                          'biblio-inventors-content'):
            item["inventors"] = bibliography.find_element_by_id('biblio-inventors-content').text
        else:
            item["inventors"] = "none"
        item["classifications_ipc"] = bibliography.find_element_by_id('biblio-international-content').text
        item["classifications_cpc"] = bibliography.find_element_by_id('biblio-cooperative-content').text
        item["priorities"] = bibliography.find_element_by_id('biblio-priority-numbers-content-0').text
        item["applicant_num"] = bibliography.find_element_by_id('biblio-application-number-content').text
        item["publication"] = bibliography.find_element_by_id('biblio-publication-number-content').text
        item["publish_as"] = bibliography.find_element_by_id('biblio-also-published-as-content').text
        item["document"] = "none"
        informations.append(item)
    time.sleep(1200)
    browser.quit()


def export_excel(export):
    # 将字典列表转换为DataFrame
    pf = pd.DataFrame(list(export))
    # 指定字段顺序
    order = ['title', 'applicants', 'inventors', 'classifications_ipc', 'classifications_cpc',
             'priorities', 'applicant_num', 'publication', 'publish_as', 'document']
    pf = pf[order]
    # 将列名替换为中文
    # columns_map = {
    #     'road_name': '路线',
    #     'bus_plate': '车牌',
    #     'timeline': '时间',
    #     'road_type': '方向',
    #     'site': '站点'
    # }
    # pf.rename(columns=columns_map, inplace=True)
    # 指定生成的Excel表格名称
    file_path = pd.ExcelWriter('information.xlsx')
    # 替换空单元格
    pf.fillna(' ', inplace=True)
    # 输出
    pf.to_excel(file_path, encoding='utf-8', index=False)
    # 保存表格
    #file_path.save("E:\\downloadfile\\espacenet\\information")
    file_path.save()


def fill_filename(info_list):
    file_list = get_all_file_name('E:\\downloadfile\\espacenet\\document')
    for item in info_list:
        item["document"] = find_target_file_name(item["title"], file_list)


def get_all_file_name(path):
    file_list = []
    for filename in os.listdir(path):
        file_list.append(filename)
    return file_list


def find_target_file_name(target, file_list):
    for filename in file_list:
        result = filename.find(target)
        if result != -1:
            return filename


# 该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
def isElementExist(element, id):
    flag = True
    try:
        element.find_element_by_id(id)
        return flag

    except:
        flag = False
        return flag


if __name__ == '__main__':
    # 获取信息
    spider2()

    #fill_filename(informations)

    #export_excel(informations)
