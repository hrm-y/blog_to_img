import os
import time

import requests
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from settings import member_num


BASE_URL = "https://www.hinatazaka46.com"


def main(member_name, selected_save_path):
    BLOG_LIST_URL = (
        "https://www.hinatazaka46.com/s/official/diary/member/list?ct="
        + member_num[member_name]
    )
    blog_url, next_exist = get_latest_blog_url(BLOG_LIST_URL)
    i = 0
    while next_exist:
        blog_article_info = get_blog_article_info(blog_url)
        screenshot_path = make_screenshot_path(blog_article_info, selected_save_path)
        # スクショ撮影＆保存（既に保存済みのブログがあれば処理をスルー）
        if not os.path.isfile(screenshot_path):
            screenshot_file = get_screenshot_file(blog_url)
            save_screenshot(screenshot_path, screenshot_file)
        blog_url, next_exist = get_next_blog_url(blog_article_info)
        i += 1
        if i == 3:
            break
    # messagebox.showinfo("完了", "すべてのブログを保存しました")


def get_latest_blog_url(blog_list_url):
    blog_article_info = get_blog_article_info(blog_list_url)
    latest_blog_url = BASE_URL + blog_article_info.find(
        "a", attrs={"class": "c-button-blog-detail"}
    ).get("href")
    # print(latest_blog_url)
    next_exist = True

    return latest_blog_url, next_exist


def get_blog_article_info(blog_url):
    res = requests.get(blog_url)
    blog_article_info = BeautifulSoup(res.text, "html.parser")
    return blog_article_info


def make_screenshot_path(blog_article_info, selected_save_path):
    member_name = blog_article_info.find(
        "div", attrs={"class": "c-blog-article__name"}
    ).text
    member_name = member_name.strip().replace(" ", "")
    date = blog_article_info.find("div", attrs={"class": "c-blog-article__date"}).text
    date = date.strip().split(" ")[0].split(".")
    year = date[0]
    month = date[1]
    day = date[2]
    blog_date = year + month.zfill(2) + day.zfill(2)
    blog_title = blog_article_info.find(
        "div", attrs={"class": "c-blog-article__title"}
    ).text
    blog_title = blog_title.replace(" ", "").replace("\n", "").replace("/", "／")

    screenshot_path = os.path.join(
        selected_save_path, member_name, blog_date + "〈" + blog_title + "〉" + ".png"
    )

    return screenshot_path


def add_margin(pil_img, top, bottom, left, right, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))

    return result


def get_screenshot_file(blog_url):
    chrome_options = Options()
    # chrome_options.add_experimental_option("detach", True)
    # ヘッドレスモード（必須）
    chrome_options.add_argument("--headless")
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(
        service=Service(executable_path=driver_path), options=chrome_options
    )

    driver.maximize_window()
    driver.get(blog_url)
    page_width = 3000
    page_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(page_width, page_height)
    screenshot = driver.find_element(By.CLASS_NAME, "p-blog-article").screenshot_as_png

    return screenshot


def save_screenshot(screenshot_path, screenshot):
    folderpath = os.path.dirname(screenshot_path)
    # 取得したメンバー名のフォルダが未作成であればフォルダを作成
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)

    # filetitle = screenshot_path.strip(member_name + "/").strip(".png")
    filetitle = os.path.basename(screenshot_path).strip(".png")

    with open(screenshot_path, "wb") as f:
        f.write(screenshot)

    # スクショを開いて上下左右に余白を追加
    img = Image.open(screenshot_path)
    img_new = add_margin(img, 40, 0, 30, 30, (255, 255, 255))
    img_new.save(screenshot_path, quality=100)
    print("【保存完了】  " + filetitle)
    time.sleep(1)


def get_next_blog_url(blog_article_info):
    try:
        next_blog_url = BASE_URL + blog_article_info.find(
            "div",
            attrs={
                "class": "c-pager__item c-pager__item--prev c-pager__item--kiji c-pager__item--kiji__blog"
            },
        ).find("a").get("href")

        next_exist = True

    except AttributeError:
        next_exist = False
        next_blog_url = ""
        print("***************全てのブログを保存しました***************")

    return next_blog_url, next_exist


if __name__ == "__main__":
    start_time = time.time()
    main()
    finish_time = time.time()
    elapsed_time = finish_time - start_time
    print(f"所要時間:{str(elapsed_time / 60)[:5]}分")
