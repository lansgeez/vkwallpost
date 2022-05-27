from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
global sort, notsort
sort = 'data/sort'
notsort = 'data/notsort'

class Pic():
    def __init__(self):
        f = open(f'{notsort}.txt', 'w')
        f.close()
        f = open(f'{sort}.txt', 'w')
        f.close()
        options=webdriver.ChromeOptions()
        #options.add_argument("--headless")
        options.add_argument("start-maximized")
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def animereact(self):
        
        self.browser.get("https://anime-pictures.net/pictures/view_posts/0?lang=ru")
        global sort, notsort
        k=1
        kf=4
        while k<=kf:
            print('Страница -', k,' из -', kf)
            sleep(3)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            hrefsrcclass=self.browser.find_elements_by_class_name('img_block_big')
            for href in hrefsrcclass:
                for taga in href.find_elements_by_tag_name('a'):
                    hreftaga=taga.get_attribute('href')
                    if 'posts' not in hreftaga:
                        print(hreftaga)
                        f = open(f'{notsort}.txt', 'a')
                        f.write(str(hreftaga)+'\n')
                        f.close()    
            k+= 1
            self.browser.find_element_by_link_text(">").click()
       
    def sort(self):
        a=[]
        global writef

        f=open(f'{notsort}.txt')
        for i in f:
            a.append(i)
        f.close()

        for i in a:
            
            print("--------------")
            print(i)
            self.browser.get(i)
            src = i
            likes = self.browser.find_element_by_id('score_n').text

            if int(likes)>19:
                img = self.browser.find_element_by_id('big_preview_cont').find_element_by_tag_name('a').get_attribute('href')
                f = open(f'{sort}.txt', 'a')
                f.write(img+'\n')
                f.write(src)
                f.close()
                print("Добавлено в очередь.")
                print("--------------")
            else:
                print('Пропуск.')
                print("--------------")
            
    def close_browser(self):

        self.browser.close()
        self.browser.quit()
sc = Pic()
sc.animereact()
sc.sort()
sc.close_browser()