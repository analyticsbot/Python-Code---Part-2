# import all necessary modules
import mechanize
import json
import urllib2
import os
import sys
import string
import time
import random
import requests
import re
from BeautifulSoup import BeautifulSoup
from multiprocessing import Process, Queue
from text_unidecode import unidecode
from pyPdf import PdfFileReader
import logging
import multiprocessing
import boto
from filechunkio import FileChunkIO
from boto.s3.connection import S3Connection
import subprocess
from datetime import datetime
import warnings
from dateutil import parser
from ebooklib import epub
from threading import Thread
warnings.filterwarnings("ignore")
import argparse

logging.basicConfig(
    filename='nist.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG)

## initialize the argument parser
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-n', help='"number of threads"')
args = arg_parser.parse_args()

AWS_Access_Key = ''
AWS_Secret_Access_Key = ''
S3_BUCKET_NAME = ''

# Connect to S3
c = S3Connection(AWS_Access_Key, AWS_Secret_Access_Key)
b = c.get_bucket(S3_BUCKET_NAME)

# if debug is set as True, updates will be printed on sysout
debug = True

if not os.path.exists('success'):
    os.makedirs('success')

if not os.path.exists('failures'):
    os.makedirs('failures')
    
# declare all the static variables
num_threads = int(args.n.strip())  # number of parallel threads
valid_chars = "-_.() %s%s" % (string.ascii_letters,
                              string.digits)  # valid chars for file names

logging.info('Number of threads ' + str(num_threads))

minDelay = 1  # minimum delay between get requests to www.nist.gov
maxDelay = 2  # maximum delay between get requests to www.nist.gov

logging.info('Minimum delay between each request =  ' + str(minDelay))
logging.info('Maximum delay between each request =  ' + str(maxDelay))

# search_base_urls have the same pattern
# just need to change the research field and page on the first and
search_base_url = 'https://archive.org/details/texts?and%5B%5D=languageSorter%3A%22English%22&sort=&page={page}'

def uploadDataS3(source_path, b):
    # Get file info
    source_size = os.stat(source_path).st_size

    # Create a multipart upload request
    mp = b.initiate_multipart_upload(os.path.basename(source_path))

    # Use a chunk size of 50 MiB (feel free to change this)
    chunk_size = 52428800
    chunk_count = int(math.ceil(source_size / float(chunk_size)))

    # Send the file parts, using FileChunkIO to create a file-like object
    # that points to a certain byte range within the original file. We
    # set bytes to never exceed the original file size.
    for i in range(chunk_count):
        offset = chunk_size * i
        bytes = min(chunk_size, source_size - offset)
        with FileChunkIO(source_path, 'r', offset=offset,
                         bytes=bytes) as fp:
            mp.upload_part_from_file(fp, part_num=i + 1)

    # Finish the upload
    mp.complete_upload()

def readPDF(filename):
    """Function to read the attachment and return the contents"""
    subprocess.call(['pdftotext',filename, filename[:-4] + '.txt'])
    f = open(filename[:-4] + '.txt', 'rb')
    content = f.read()
    return content

def readEPUB(filename):
    """Function to read the attachment and return the contents"""
    book = epub.read_epub(filename)
    content = ''
    for a in book.get_items_of_type(epub.EpubHtml):
	content += a
    return content

def trimArticle(articleText, DIVIDE_ARTICLE):
    article_distributed = articleText.split()
    len_article = len(article_distributed)
    if len_article>DIVIDE_ARTICLE:
        new_article = ''
        for i in range(DIVIDE_ARTICLE):
            new_article = new_article + ' ' + article_distributed[i]
        
        while True:
            i+=1
            new_article = new_article + ' ' + article_distributed[i]
            if new_article.endswith('.'):
                break
    else:
        new_article = articleText
    return new_article.strip()

def download_file(url, name):
    """ function to download the files to local"""
    if '.pdf' not in name:
        local_filename = name + '.pdf'
    else:
        local_filename = name
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename


def split(a, n):
    """Function to split data evenly among threads"""
    k, m = len(a) / n, len(a) % n
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]
            for i in xrange(n))


def getLinks(
        i,
        queue,
        debug,
        minDelay,
        maxDelay,
        num_threads):
    """ Function to pull out all publication links from nist
    data - research ids pulled using a different script
    queue  -  add the publication urls to the list
    """
    

    # pg_idx is the page index for the research search results.
    # break the while loop if there are no more search results
    # add the links to a local list, and the length to another list
    pg_idx = i
    local_queue = []
    len_local_queue = [1111, 222, 333, 4444]
    while True:
        url = search_base_url.replace(
            '{page}', str(pg_idx))
        if debug:
            sys.stdout.write('Visting url :: ' + url + '\n')

        logging.info('Visting url :: ' + url + '\n')
        pg_idx += num_threads
        len_local_queue.append(len(local_queue))

        # if the last 2 elements of the local queue are same it means
        # no new data is being added. Exit the loop
        if len_local_queue[-2] == len_local_queue[-1]:
            break

        # intatiate mechanize browser, read the response and pass it to
        # soup
        br = mechanize.Browser()
        logging.info(
            'Intantiated a browser for thread :: ' +
            str(i) +
            '\n')

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:14.0) Gecko/20100101 Firefox/14.0.1',
            'Referer': 'http://www.nist.com'}

        # wrap the request.
        request = urllib2.Request(url, None, header)

        br.open(request)

        html = br.response().read()
        soup = BeautifulSoup(html)

        divs = soup.findAll('div', attrs = {'class':'item-ia'})
        count = 0
        for div in divs:
            links  = div.findAll('a')
            for link in links:
                try:
                    if link['title']:
                        time.sleep(.1)
                        queue.put('https://archive.org' + link['href'])
                        count +=1
                        logging.info('Added archive to queue :: ' + str(link['href']))

                except Exception,e:
                        pass
        if count == 0:
            break
        print count
        wait_time = random.randint(minDelay, maxDelay)
        if debug:
            sys.stdout.write('Sleeping for :: ' + str(wait_time) + '\n')

        logging.info('Sleeping for :: ' + str(wait_time) + '\n')
        time.sleep(wait_time)


def getElement(name, spans):
    for span in spans:
            ix = spans.index(span)
            try:
                    if span.getText() == name.strip():
                            return spans[ix+1].getText()
                            break
            except:
                    pass

def publicationData(i, queue, debug, minDelay, maxDelay, b):
    while True:
        try:
            url = queue.get() + '&output=json'
        except Exception,e:
            time.sleep(1)
            continue

        if debug:
            sys.stdout.write('Visting publication url :: ' + url + '\n' + '\n')

        logging.info('Visting publication url :: ' + url + '\n' + '\n')
        br = mechanize.Browser()
        
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:14.0) Gecko/20100101 Firefox/14.0.1',
            'Referer': 'http://www.nist.com'}

        # wrap the request.
        request = urllib2.Request(url, None, header)
        br.open(request)
        html = json.loads(br.response().read())
        
        try:
            title = html['metadata']['title'][0]
        except:
            title = ''
        try:
            authors = html['metadata']['creator'][0]
        except:
            authors = ''
        try:
            publicationDate = html['metadata']['publicdate'][0]
            publicationDate = str(parser.parse(publicationDate).replace(second=0).isoformat().replace(':00', '+00:00'))
        except:
            publicationDate = ''
        try:
            collection = html['misc']['collection-title']
        except:
            collection = ''
        try:
            image = html['misc']['image']
        except:
            image = ''

        url1 = url.replace('&output=json','')
        br.open(url1)
        resp = br.response().read()
        soup = BeautifulSoup(resp)
        format_group = soup.findAll(attrs = {'class':'format-group'})
        files = []
        for form in format_group:
            try:
                files.append(form.find('a')['href'])
            except:
                pass
        txt_file_url = ''
        try:
            for file in files:
                if '.txt' in file:
                    txt_file_url = 'https://archive.org' + file
                    break
        except:
            txt_file_url = ''

        try:
            resp = requests.get(txt_file_url)
            soup1 = BeautifulSoup(resp.content)
            text = soup1.find('pre').getText().replace('\n', '')
        except:
            text = ''
        pdf_file_url = ''
        try:
            for file in files:
                if '.pdf' in file:
                    pdf_file_url = 'https://archive.org' +  file
                    break
        except:
            pdf_file_url = ''
        pdf_text = ''
        if text == ''  and pdf_file_url !='':
            try:
                filename = download_file(pdf_file_url, name)
                pdf_text = readPDF(filename)
            except:
                pdf_text = ''
        epub_file_url = ''
        try:
            for file in files:
                if '.epub' in file:
                    epub_file_url = 'https://archive.org'  + file
                    break
        except:
            epub_file_url = ''
        epub_text = ''
        if text == ''  and pdf_file_url =='' and epub_file_url!='':
            try:
                epubfilename = download_file(epub_file_url, name)
                epub_text = readEPUB(epubfilename)
            except:
                epub_text = ''

        digitizing_sponsor = ''
        try:
            publisher = html['metadata']['creator'][0]
        except:
            publisher = ''
        try:
            language = html['metadata']['language'][0]
        except:
            language = ''
        words = ''
        if text !='':
            words = text
        elif text == '' and pdf_text !='':
            words = pdf_text
        elif text == '' and pdf_text == '' and epub_text !='':
            words = epub_text
            
        abstract = trimArticle(words, 50)
        external_id = "archiveorg_" + collection.replace(' ', '-') + '_' + title.replace(' ', '-')
        try:
            date = html['metadata']['year'][0]
        except:
            date = ''

        spans = soup.findAll('span')
        pages = getElement('Pages', spans)
        boxies = soup.findAll(attrs = {'class':'boxy-ttl'})
        for box in boxies:
            try:
                    if box.getText() == 'Uploaded by':
                            digitizing_sponsor = box.findNextSibling().getText()
            except:
                    pass


        # write the fellow summary to file
        file_name = title.replace(' ', '_') + '.json'
        file_name = ''.join(c for c in file_name if c in valid_chars)
        if words == '':
            folder = 'failures'
        else:
            folder = 'success'
        if os.name == 'nt':
            f = open(folder + '//' + external_id, 'wb')
        else:
            f = open(folder + '/' + external_id, 'wb')
        data = {
                "abstract": abstract,
                "external_id": external_id,
                "date": publicationDate,
                "title": title,
                "url": url,
                "words": unidecode(words),
                "meta": {
                        "archiveorg": {
                                        "collection_name": collection,
                                        "authors": authors,
                                        "digitizing_sponsor": digitizing_sponsor,
                                        "publication_date": publicationDate,
                                        "pages": pages,
                                        "publisher": publisher,
                                        "image" : image,
                                        "extra" : str(html)
                                          }
                        }
                }

        f.write(json.dumps(data))
        f.close()
        logging.info('File written ' + file_name)
        if os.name == 'nt':
            uploadDataS3(folder + '//' + file_name, b)
        else:
            uploadDataS3(folder + '/' + file_name, b)
        if debug:
            sys.stdout.write(file_name + ' has been written to S3 bucket' + '\n')
        logging.info(file_name + ' has been written to S3 bucket' + '\n')
        
        if debug:
            sys.stdout.write(file_name + ' written' + '\n')
        wait_time = random.randint(minDelay, maxDelay)
        sys.stdout.write('Sleeping for :: ' + str(wait_time) + '\n')
        logging.info('Sleeping for :: ' + str(wait_time) + '\n')
        sys.stdout.write(
            '******************************************' + '\n')
        sys.stdout.write(
            '******************************************' + '\n')
        time.sleep(wait_time)

if __name__ == "__main__":
    # declare an empty queue which will hold the publication ids
    queue = Queue()
    logging.info('Initialized an empty queue')
    #queue = list()
    threads = []
    for i in range(num_threads):
        threads.append(
            Process(
                target=getLinks,
                args=(
                    i + 1,
                    queue,
                    debug,
                    minDelay,
                    maxDelay,
                    num_threads,

                )))
    j = 1
    for thread1 in threads:
        sys.stdout.write('starting archive link scraper ##' + str(j) + '\n')
        logging.info('starting archive link scraper ##' + str(j) + '\n')
        j += 1
        thread1.start()

    time.sleep(10)

    dataThreads = []
    for i in range(1*num_threads):
        dataThreads.append(
            Process(
                target=publicationData,
                args=(
                    i + 1,
                    queue,
                    debug,
                    minDelay,
                    maxDelay,
                    b,

                )))
    
    j = 1
    for thread in dataThreads:
        sys.stdout.write('starting archive data scraper ##' + str(j) + '\n')
        logging.info('starting archive data scraper ##' + str(j) + '\n')
        j += 1
        thread.start()
    
    try:
        for worker in threads:
            worker.join(10)

    except KeyboardInterrupt:
        print 'Received ctrl-c'
        for worker in threads:
            worker.terminate()
            worker.join(10)
    
    try:
        for worker in dataThreads:
            worker.join(10)
    except KeyboardInterrupt:
        print 'Received ctrl-c'
        for worker in dataThreads:
            worker.terminate()
            worker.join(10)
    
