# Styleforum Thread Image Scraper


import requests
import os.path
from bs4 import BeautifulSoup





if __name__ == "__main__":


    base_url = 'https://www.styleforum.net/threads/'
    thread_url = 'john-elliott-official-affiliate-thread.343980/'

    start_page = 1
    max_page = 3811


    save_path = './images/'


    # scrape images from each html page
    for page_num in range(start_page,max_page):

        # set up the forum URL
        full_url = base_url + thread_url + 'page-' + str(page_num)
        print('page num = ', page_num)

        # get the html and soup object 
        html = requests.get(full_url).text
        soup = BeautifulSoup(html, "lxml")
    

        # remove signatures, parse out some smilies
        for div in soup.find_all("div", {'class':'signature'}): 
            div.decompose()

        for div in soup.find_all("img", {'class':'mceSmilie'}): 
            div.decompose()

        # forgot quoted images
        for div in soup.find_all("div", {'class':'bbCodeBlock bbCodeQuote'}): 
            div.decompose()



        # get all the remaining images
        tags = soup.findAll("img", class_="bbCodeImage")

        i = 0 # integer naming scheme
        for msg in tags:

            # get the image url
            img_url = msg.get('data-url')
            #print(i)
            
            # parse out more smilies... these things are stubborn
            if "http://files.styleforum.net/images/smilies/" in img_url:
                #print('skipping')
                continue 

            if "https://www.styleforum.net/~styleforumadmin/styleforumfinal/emojione/" in img_url:
                #print('skipped', i)
                continue 

            # write the image content to a local file. change this as needed for whatever purpose
            try:
                filename = str(page_num) + '_' + str(i) + '.jpg'
                full_path = os.path.join(save_path, filename)
                f = open(full_path,'wb')
                f.write(requests.get(img_url).content)
                f.close()


            # rare cases that I don't feel like debugging right now 
            except:
                print('image unavailable')

            i += 1


