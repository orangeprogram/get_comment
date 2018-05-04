# 登录

import urllib
import time
import pymongo
from selenium import webdriver
import os
#使用PhantomJS

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs",prefs)
# chrome_options.add_argument("--headless")

brower = webdriver.Chrome("C:\\Users\\orange\\Downloads\\chromedriver_win32\\chromedriver.exe",chrome_options=chrome_options)
wait = webdriver.support.ui.WebDriverWait(brower,10)
# 数据库
client = pymongo.MongoClient('localhost',27017)
next_our = client['douban']

# 获取验证码
def get_yzm(src):
    print("正在保存验证码图片")
    captchapicfile = "captcha.png"
    urllib.request.urlretrieve(src, filename=captchapicfile)
    os.startfile('captcha.png')
    print("请打开图片文件，查看验证码，输入单词......")
    captcha_value = input()
    return captcha_value

def login(url,username,password):
    print(url)
    brower.get(url)
    # brower.find_element_by_css_selector('[class="nav-login"]').click()
    name = brower.find_element_by_id('email')
    print(name)
    name.clear()
    name.send_keys(username)
    pwd = brower.find_element_by_id('password')
    pwd.clear()
    pwd.send_keys(password)
    pic_src = brower.find_element_by_id('captcha_image').get_attribute('src')
    print(pic_src)
    #调用获取验证码的方法
    cap_value = get_yzm(pic_src)
    yan_zheng_ma = brower.find_element_by_id('captcha_field')
    yan_zheng_ma.clear()
    yan_zheng_ma.send_keys(cap_value)
    brower.find_element_by_css_selector('[class="btn-submit"]').click()
    print('登陆成功')






# 搜索电影
def seach(movie_name):
    inp_query = brower.find_element_by_id('inp-query')
    inp_query.clear()
    inp_query.send_keys(movie_name)
    submit = brower.find_element_by_css_selector('[type="submit"]')
    submit.click()
    time.sleep(1)
    brower.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[1]/a').click()
    print("进入详情页")

# 进入短评列表
def into_comment():
    # if brower.find_element_by_xpath('//*[@id="comments-section"]/div[1]/h2/span/a'):
    brower.find_element_by_xpath('//*[@id="comments-section"]/div[1]/h2/span/a').click()
    # brower.find_element_by_xpath('//*[@id="paginator"]/a').click()
    
    print("进入短评列表")

# 获取短评
def get_comment():
    wait.until(lambda brower : brower.find_element_by_css_selector('[class="next"]'))
    time.sleep(1)
    for i in range(1,21):
        comment = brower.find_element_by_xpath('//*[@id="comments"]/div[{}]/div[2]/p'.format(str(i))).text
        comment_name = brower.find_element_by_xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/a'.format(str(i))).text
        votes = brower.find_element_by_xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[1]/span'.format(str(i))).text
        rating = brower.find_element_by_xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/span[2]'.format(str(i))).get_attribute('class')[7:8]
        print(rating)
        #构建字典
        data = {
            'comment': comment,
            'comment_name': comment_name,
            'votes': int(votes),
            'rating':rating
        }
        comments.insert_one(data)
        # print('*'*100)
        # print(data)
        print('成功存入数据库')

#翻页
def next_page():
    next = brower.find_element_by_css_selector('[class="next"]')
    print(dir(next))
    try:
        next.click()
    except:
        print("全部完成了")



comments = next_our['comments']

URL = 'https://www.douban.com/accounts/login'
URL = 'https://www.douban.com/accounts/login?redir=https%3A%2F%2Fmovie.douban.com%2F'

username = '17765286816'
password = 'wgb201005335'
movie = '后来的我们‎'
if __name__=="__main__":
    login(URL,username,password)
    seach(movie)
    into_comment()
    for page in range(24):
        get_comment()
        next_page()