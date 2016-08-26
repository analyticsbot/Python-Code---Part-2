from amazon.api import AmazonAPI
from unidecode import unidecode

AMAZON_ACCESS_KEY='AKIAIRGYI76BYPQZXAQQ'
AMAZON_SECRET_KEY ='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'
AMAZON_ASSOC_TAG =273589934636

AMAZON_ACCESS_KEY1='AKIAIYWGSVATZRMKAIRA'
AMAZON_SECRET_KEY1 ='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'
AMAZON_ASSOC_TAG1 =289838321798 

amazon_uk = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG, region="UK")
amazon_uk1 = AmazonAPI(AMAZON_ACCESS_KEY1, AMAZON_SECRET_KEY1, AMAZON_ASSOC_TAG1, region="UK")

asin ='B001FB5FWQ'
product = amazon_uk1.lookup(ItemId=(asin))

price_new = product.price_and_currency
print price_new



