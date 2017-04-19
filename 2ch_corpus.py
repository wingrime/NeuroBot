import json
import re
import urllib.request

CATALOG = "https://2ch.hk/b/catalog.json"


def get_json(req_url):
    with urllib.request.urlopen(req_url) as url:
        return json.loads(url.read().decode())


def get_thread_url(id):
    return "http://2ch.hk/b/res/" + str(id) + ".json"


def get_threads_ids():
    threads = get_json(CATALOG)['threads']
    for thread in threads:
        yield thread['num']


def remove_html_tags(s):
    p = re.compile(r'<.*?>')
    return p.sub('', s)


def remove_numers(s):
    return re.sub(r"\d+", "", s)


def remove_symbols(s):
    s = re.sub(r">>\d+|&#|>>|&gt;|~|;|\(оп\)|\(op\)|\-\-|\.\.|\.\.\.|—|\:|[a-zA-Z]|\)\)|\?\?|\@|\&|\(\)|\=|\_", "", s)
    return re.sub(r"\(\)|\.\.|\.\.\.", "", s)


def cleanse_text(str):
    str = remove_html_tags(str)
    str = remove_numers(str)
    str = remove_symbols(str)
    return str.lower().strip()


def get_all_posts():
    for thread_id in get_threads_ids():
        try:
            posts = get_json(get_thread_url(thread_id))['threads'][0]['posts']
            for post in posts:
                comment = cleanse_text(post['comment']);
                if (len(comment) > 5):
                    yield comment  # , int(post['num']), int(post['parent'])
        except:
            pass


posts = get_all_posts()
f = open('result.txt', 'w')
for post in posts:
    try:
        f.write(post)
        f.write("\n")
        f.flush()
    except:
        pass
