import uuid
import requests
from bs4 import BeautifulSoup
import json


def parse_a_tags_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    a_tags = soup.find_all("div", class_="content_main_item")

    links = []
    for div in a_tags:
        a_tag = div.find("a")
        if a_tag:
            link = "https://tengrinews.kz/" + a_tag.get("href")
            links.append(link)

    return links


def parse_news_details(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.find("h1", class_="head-single").text.strip()
        image_tag = soup.find("picture", class_="content_main_thumb_img")
        image_src = image_tag.find("source")["srcset"] if image_tag else None
        date = soup.find("div", class_="date-time").text.strip()
        paragraphs = soup.find("div", class_="content_main_text").find_all("p")

        content = "\n".join(paragraph.text.strip() for paragraph in paragraphs)

        news_details = {
            "id": str(uuid.uuid4()),
            "title": title,
            "image_src": "https://tengrinews.kz" + image_src if image_src else None,
            "date": date,
            "content": content,
            "url": url,
        }

        return news_details
    else:
        print(f"Failed to retrieve webpage: {url}")
        return None


def parse_multiple_pages(base_url, num_pages):
    all_links = []
    for page in range(1, num_pages + 1):
        url = f"{base_url}{page}/"
        response = requests.get(url)
        if response.status_code == 200:
            links = parse_a_tags_from_html(response.content)
            all_links.extend(links)
        else:
            print(f"Failed to retrieve webpage: {url}")

    return all_links


def parse_and_save_news(base_url, num_pages, output_file):
    links = parse_multiple_pages(base_url, num_pages)
    news_list = []

    for link in links:
        news_details = parse_news_details(link)
        if news_details:
            news_list.append(news_details)

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(news_list, json_file, ensure_ascii=False, indent=4)

    print(
        f"Successfully parsed and saved {len(news_list)} news articles to {output_file}"
    )


base_url = "https://tengrinews.kz/news/page/"
num_pages = 2
output_file = "news_service/utils/parsed_data.json"

parse_and_save_news(base_url, num_pages, output_file)
