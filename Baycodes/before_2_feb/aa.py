from amazon.api import AmazonAPI

SALES_RANK = 100
AMAZON_ACCESS_KEY = 'AKIAJ6AHCTMPFVQSP3NA'
AMAZON_SECRET_KEY = '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'
AMAZON_ASSOC_TAG = '678654738313'
asin = 'B00NVDNDUW'

amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG, region="UK")
product = amazon.search(asin = asin)	

product1 = amazon.lookup(ItemId='B00EOE0WKQ')
