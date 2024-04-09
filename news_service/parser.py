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
            link = "https://tengrinews.kz" + a_tag.get("href")
            links.append(link)

    return links


def parse_media_content(div_tag):
    img_tag = div_tag.find("img")
    if img_tag:
        img_src = img_tag.get("src")
        return img_src
    else:
        video_tag = div_tag.find("video")
        if video_tag:
            source_tag = video_tag.find("source")
            if source_tag:
                video_src = source_tag.get("src")
                return video_src
    return None


def parse_news_details(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.find("h1", class_="head-single").text.strip()
        content_main_div = soup.find("div", class_="content_main")

        media_src = parse_media_content(
            content_main_div.find("div", class_="content_main_thumb")
        )

        date = soup.find("div", class_="date-time").text.strip()
        paragraphs = soup.find("div", class_="content_main_text").find_all("p")

        content = "\n".join(paragraph.text.strip() for paragraph in paragraphs)

        news_details = {
            "id": str(uuid.uuid4()),
            "title": title,
            "media_src": "https://tengrinews.kz" + media_src,
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


def parse_and_save_news_wrapper():
    base_url = "https://tengrinews.kz/news/page/"
    num_pages = 8
    output_file = "news_service/utils/parsed_data.json"
    parse_and_save_news(base_url, num_pages, output_file)
