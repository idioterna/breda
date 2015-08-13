# -*- coding: utf-8 -*-
from flask import Flask, request
import urllib2, time, re, json, random
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@app.route('/slack/', methods=['POST'])
def slack():
    chunks = request.form.get('text').encode('utf-8').split()
    if len(chunks) >= 2:
        command = chunks[1]
    else: # no command
        return json.dumps(dict(text='What is it?'))
    user = request.form.get('user_name')
    chan = request.form.get('channel_name')
    g = globals()
    if 'slack_' + command in g:
        return json.dumps(dict(text=g['slack_' + command](user, chan, chunks)))
    else:
        return json.dumps(dict(text="I don't know about %s." % command))


def _pic(url, title=None):
    if '?' in url:
        concat_char = '&'
    else:
        concat_char = '?'
    if title:
        return '<%s%scb=%s.jpg|%s>' % (url, concat_char, time.time(), title)
    else:
        return '<%s%scb=%s.jpg>' % (url, concat_char, time.time())


def slack_makin(u, c, m):
    if m[2] != 'copies':
        return
    name = ' '.join(m[3:])
    endings = [
        'ski',
        'inator',
        'tholmeau',
        'as',
        'kadaka',
        'chop',
        'erino',
        name[-1:]+name[-1:]+name[-1:]+name[-1:],
        'wise',
        'man',
        'atollah',
        'ster',
        'ino',
        'ipulator',
        'meister',
    ]
    rand1 = random.choice(endings)
    rand2 = random.choice(endings)
    return "%s%s! the %s%s!" % (name, rand1, name, rand2)


def slack_piramida(user, chan, message):
    menu = urllib2.urlopen('http://pizzerijapiramida.si/malice/').read()
    ts = time.localtime()
    tss = ', %s.%s.%s' % (ts.tm_mday, ts.tm_mon, ts.tm_year % 100)
    start = menu.find(tss) + len(tss)
    end = menu.find('</div>', start)
    daymenu = re.sub(r'<[^>]+?>', ' ', menu[start:end])
    daymenu = daymenu.replace('\n', '').replace('\r', '').replace('€', '€\n').replace('&nbsp;', '')
    daymenu = re.sub(r' +', ' ', daymenu)
    daymenu = daymenu.replace(' 1.', '\n 1.')
    if len(daymenu) > 20:
        return tss[2:] + '\n' + daymenu
    else:
        return "I really can't tell, head to <http://pizzerijapiramida.si/malice/|the page> to see what's cookin'."


def slack_radar(u, c, m):
    return _pic('http://www.arso.gov.si/vreme/napovedi%20in%20podatki/radar_anim.gif', 'SIRAD')


def slack_where(u, c, m):
    return '<https://github.com/idioterna/breda|At home, of course.>'


def slack_bicikelj(u, c, m):
    return "They were all stolen, so just take a hike."


def slack_wat(u, c, m):
    wat = json.load(urllib2.urlopen('http://watme.herokuapp.com/random')).get('wat')
    if wat:
        return _pic(wat)
    else:
        return _pic('http://www.babel.crackerboxpalace.com/gifs/strangelove-wat.gif')


def slack_random(u, c, m):
    data = json.load(urllib2.urlopen('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC')).get('data',{}).get('image_url')
    if data:
        return _pic(data)
    else:
        return _pic('http://www.babel.crackerboxpalace.com/gifs/strangelove-wat.gif')

