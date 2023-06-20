import requests
import bs4
from fake_headers import Headers
import json

headers = Headers(browser="firefox", os='win')
headers_data = headers.generate()

main_html = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers= headers_data).text
main_soup = bs4.BeautifulSoup(main_html, "lxml")

def get_info_vacancy():
    div_article_list_tag = main_soup.find('div', id = 'a11y-main-content')
    dives = div_article_list_tag.find_all('div', class_ = 'serp-item')

    vacancy_info = []

    for div in dives:

        a_title_vacancy = div.find('a', class_ = 'serp-item__title')
        link = a_title_vacancy['href']

        vacancy_html = requests.get(link, headers=headers.generate()).text
        vacancy_soup = bs4.BeautifulSoup(vacancy_html, "lxml")

        full_info_vacancy = vacancy_soup.find('div', class_ = 'bloko-columns-row')

        title_vacancy = full_info_vacancy.find('h1', class_ = 'bloko-header-section-1').text
        text_vacancy = full_info_vacancy.find('div', class_ = 'vacancy-description').text

        name_company = full_info_vacancy.find('span', class_ = 'vacancy-company-name').text
        city_vacancy = full_info_vacancy.find(attrs={'data-qa': 'vacancy-view-location'})
        if city_vacancy is None:
            city_vacancy = full_info_vacancy.find(attrs={'data-qa': 'vacancy-view-raw-address'}).text
        else:
            city_vacancy = city_vacancy.text
        cost_vacancy = full_info_vacancy.find(attrs={'data-qa': 'vacancy-salary-compensation-type-net', 'class': 'bloko-header-section-2 bloko-header-section-2_lite'})
        if cost_vacancy is not None:
            cost_vacancy = cost_vacancy.text
        if "Django" and "Flask" in text_vacancy:
            vacancy_info.append({
                "title": title_vacancy,
                "link": link,
                "cost": cost_vacancy,
                "name_company": name_company,
                "city": city_vacancy
            })

    return vacancy_info

def created_file(vacancy_info):
    with open('data.txt', 'w', encoding='utf-8') as outfile:
        for data in vacancy_info:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    info_vacancy = get_info_vacancy()
    created_file(info_vacancy)
