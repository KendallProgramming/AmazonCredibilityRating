import re
from ast import literal_eval

import requests
from bs4 import BeautifulSoup



url = "https://www.amazon.com/hz/reviews-render/ajax/reviews/get/ref=cm_cr_arp_d_paging_btm_next_2"
urlt = "https://www.amazon.com/CeraVe-Moisturizing-Cream-Daily-Moisturizer/dp/B00TTD9BRC/ref=pd_ci_mcx_mh_mcx_views_0?pd_rd_w=Bo9ev&content-id=amzn1.sym.989f40d8-8518-48dd-a0a7-bf8bb07a7e6d%3Aamzn1.symc.1065d246-0415-4243-928d-c7025bdd9a27&pf_rd_p=989f40d8-8518-48dd-a0a7-bf8bb07a7e6d&pf_rd_r=EJRSP27ZA0DDEK79YT59&pd_rd_wg=KC80U&pd_rd_r=e501782c-2fd5-4c53-89fa-d520d5927be0&pd_rd_i=B00TTD9BRC"


ind1 = urlt.find("/dp")

print(f"first urlt: {urlt[ind1+4:]}\n")
urlt = urlt[ind1+4:]
ind = urlt.find("/")
asin = urlt[:ind]
print(asin)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
}

payload = {
    "sortBy": "",
    "reviewerType": "all_reviews",
    "formatType": "",
    "mediaType": "",
    "filterByStar": "",
    "filterByAge": "",
    "pageNumber": "1",
    "filterByLanguage": "",
    "filterByKeyword": "",
    "shouldAppend": "undefined",
    "deviceType": "desktop",
    "canShowIntHeader": "undefined",
    "reftag": "cm_cr_arp_d_paging_btm_next_2",
    "pageSize": "10",
    "asin": asin,  # <--- change product asin here
    "scope": "reviewsAjax0",
}


for page in range(1, 4):  # <--- change number of pages here
    payload["pageNumber"] = page

    t = requests.post(url, data=payload, headers=headers).text

    soup = BeautifulSoup(
        "\n".join(map(literal_eval, re.findall(r'"<div id=.*?</div>"', t))),
        "html.parser",
    )

    for r in soup.select('[data-hook="review"]'):
        # print(r)
        print(r.select_one(".a-profile-name").text.strip())
        print(r.select_one('[data-hook="review-body"]').text.strip())
        print(r.select_one('[data-hook="review-star-rating"]').text.strip())
        print()