import validators 
from urllib.parse import urlparse

def validate_url(url):

    valid=validators.url(url)

    print(valid)

    domain = urlparse(url).netloc

    print(domain)


validate_url('https://ww.chegg.com/homework-help/mathematical-statistics-and-data-analysis-1st-edition-chapter-9-problem-1p-solution-9780534082475?trackid=71c3376f577c&strackid=480448d8cac0')

