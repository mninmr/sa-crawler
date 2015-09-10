from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep
import csv

BASE_URL = "http://seekingalpha.com"

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def get_category_links(section_url):
    soup = make_soup(section_url)
    content = soup.find("div", "lists_pages full")
    transcript_links = [BASE_URL + li.a["href"] for li in content.findAll("li")]
    return transcript_links

def get_transcript_info(transcript_url):
    soup = make_soup(transcript_url)
    headline = soup.find("div", "page_header_email_alerts")
    headline_info = parse_headline(headline.h1.span.string)

    return headline_info

def parse_headline(headline):
    if headline.find("Earnings Call Transcript") == -1 \
        or headline.find("Results") == -1:
        return None
    ticker = headline[headline.find("(")+1:headline.find(")")]
    term = headline[headline.find("Results")-10:headline.find("Results")]

    return {"ticker": ticker,
            "term": term}


if __name__ == '__main__':
    data = []
    for ii in range(1, 3):
        link = "http://seekingalpha.com/earnings_center/transcripts/all/" + str(ii)
        transcripts = get_category_links(link)
        for transcript in transcripts:
            info = get_transcript_info(transcript)
            if info != None:
                data.append(info)
            sleep(1)

    with open("transcripts.csv", "wb") as ff:
        writer = csv.writer(ff) 
        writer.writerow(["term", "ticker"])
        for item in data:
            writer.writerow(item.values())

    ff.close()