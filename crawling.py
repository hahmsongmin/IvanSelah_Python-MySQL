import requests
from bs4 import BeautifulSoup
from mysql import set_mysql

# Explanation
# step1. bring information of g-market about best products.
# step2. Oranize information about categories.
# step3. connect the two tables with the foreign key.
# step4. category name, sub name, ranking, title, provider, orinal price, discount price, discount percent
# TO RUN, FIRST USE THE DATABASE IN MYSQL

def get_items(html, category_name, sub_category_name):
    items_result_list = list()
    best_item = html.select(".best-list")
    items = best_item[1].select("ul li")
    for index, item in enumerate(items):
        data_dict = dict()

        ranking = index + 1
        title = item.find("a", class_="itemname")
        ori_price = item.select_one('div.o-price')
        dis_price = item.select_one('div.s-price strong span')
        discount_percent = item.select_one('div.s-price em')

        if ori_price == None or ori_price.get_text() == "":
            ori_price = dis_price

        if dis_price == None:
            ori_price, dis_price = 0, 0
        else:
            ori_price = ori_price.get_text().replace(",", "").replace("원", "")
            dis_price = dis_price.get_text().replace(",", "").replace("원", "")

        if discount_percent == None or discount_percent.get_text() == '':
            discount_percent = 0
        else:
            discount_percent = discount_percent.get_text().replace("%", "")
        #Ex, http://item.gmarket.co.kr/Item?goodscode=1345149344
        product_list = item.select_one("div.thumb > a")
        item_code = product_list.attrs['href'].split('=')[1].split('&')[0]

        res = requests.get(product_list.attrs['href'])
        soup = BeautifulSoup(res.content, "html.parser")
        provider = soup.select_one("span.text__seller > a")
        if provider == None or provider == "":
            provider = soup.select_one("span.text__brand")

        provider = provider.get_text()

        data_dict['category_name'] = category_name
        data_dict['sub_category_name'] = sub_category_name
        data_dict['ranking'] = ranking
        data_dict['item_code'] = item_code
        data_dict['provider'] = provider
        data_dict['title'] = title.get_text()
        data_dict['ori_price'] = ori_price
        data_dict['dis_price'] = dis_price
        data_dict['discount_percent'] = discount_percent

        # print(category_name, sub_category_name, ranking, item_code, provider, title.get_text(),
        #     ori_price, dis_price, discount_percent)

        set_mysql(data_dict)


def get_category(category_link, category_name):
    # print(category_link, category_name)
    res = requests.get(category_link)
    soup = BeautifulSoup(res.content, 'html.parser')
    get_items(soup, category_name, "ALL")

    sub_categories = soup.select('div.navi.group ul li > a')
    for sub_category in sub_categories:
        res = requests.get(
            'http://corners.gmarket.co.kr/' + sub_category['href'])
        soup = BeautifulSoup(res.content, "html.parser")
        get_items(soup, category_name, sub_category.get_text())


gmarket_url = 'http://corners.gmarket.co.kr/Bestsellers'
res = requests.get(gmarket_url)
soup = BeautifulSoup(res.content, 'html.parser')

categories = soup.select('#categoryTabG > li a')
count = 1
for category in categories:
    items_link = f"http://corners.gmarket.co.kr/{category['href']}"
    get_category(items_link, category.get_text())
