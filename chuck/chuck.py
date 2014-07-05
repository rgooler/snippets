i#!/usr/bin/python
import requests
import os
import subprocess


def get_img():
    cookies = dict()
    cookies['lang'] = 'en'
    cookies['nick'] = 'asdfasdfasdf'
    cookies['PHPSESSID'] = 'adfasdfasdfa'
    baseurl = 'http://example.com/'
    
    chuck_php = requests.get(baseurl + 'chuck.php', cookies=cookies)
    #print chuck_php.text
    number_png_php = chuck_php.text.split('"')[21]
    #print "Fetching", number_png_php
    number_png = requests.get(baseurl + number_png_php, cookies=cookies)
    with open('number.png', 'wb') as fh:
        fh.write(number_png.content)
    #print 'done'

def cleanup():
    try: os.remove('number.png')
    except: pass
    try: os.remove('result.txt')
    except: pass

def tesseract():
    cmd = ['/usr/bin/tesseract', 'number.png', 'result', '-psm', '7', 'nobatch', 'tesseract-chuck']
    subprocess.call(cmd)
    with open('result.txt') as fh:
        res = fh.read()
    return res

def solve(result):
    l = result.split()
    a = (int)(l[0].strip('('))
    b = (int)(l[1].rstrip(')'))
    c = (int)(l[3])
    
    print "(%s^%s) %% %s" % (a,b,c)
    return (a ** b) % c

def submit_answer(answer):
    cookies = dict()
    cookies['lang'] = 'en'
    cookies['nick'] = 'asdfasdf'
    cookies['PHPSESSID'] = 'asdfasdfasdf'
    baseurl = 'http://example.com/'
    body = "answer=%s" % answer
    
    
    chuck_php = requests.post(baseurl + 'chuck.php', cookies=cookies, data=body)
    print chuck_php.text
    
def submit_answer_proxy(answer, host, port):
    cookies = dict()
    cookies['lang'] = 'en'
    cookies['nick'] = 'asdfasdf'
    cookies['PHPSESSID'] = 'asdfasdfasdf'
    baseurl = 'http://example.com/'
    body = "answer=%s" % answer
    proxies = {
        'http': 'http://%s:%s' % (host, port),
        'https': 'https://%s:%s' % (host, port),
    }
    
    
    chuck_php = requests.post(baseurl + 'chuck.php', cookies=cookies, data=body, proxies=proxies)
    print chuck_php.text

if __name__ == "__main__":
    cleanup()
    get_img()
    result = tesseract()
    answer = solve(result)
    print answer
    submit_answer(answer)
    submit_answer_proxy(answer, '1.2.3.4', '1111')

