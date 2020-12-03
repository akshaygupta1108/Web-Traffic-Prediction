import requests
import datetime as dt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import string
import os
import random

api_url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/'   #en.wikipedia.org/all-access/all-agents/hello/daily/st/en
storage_path = os.getcwd()+'/cache/'

def get_dates(days=500):
    def date_to_string(date):
        year = str(date.year)
        month = str(date.month)
        day = str(date.day)
        if len(month)<2:
            month = '0'+month
        if len(day)<2:
            day = '0'+day
        return year+month+day
    end = dt.datetime.now()
    start = end - dt.timedelta(days=days)

    start = date_to_string(start)
    end = date_to_string(end)

    return start,end

def get_url(search_word,start,end,language,access):
    request_url = api_url + language + '.wikipedia.org/'+access+'/all-agents/'+search_word+'/daily/'+start + '/' + end
    return request_url

def request_url(url):
    json = requests.get(url)
    json = json.json()
    print('json extracted')
    return json

def extract_views_from_json(json):
    days_per_month = [31,28,31,30,31,30,31,31,30,31,30,31]
    cummulative_days = [sum(days_per_month[:i+1]) for i in range(len(days_per_month))]

    items = json['items']
    dates = []
    views = []
    for item in items:
        time_stamp = item['timestamp']
        year = int(time_stamp[:4])
        month = int(time_stamp[4:6])
        day = int(time_stamp[6:8])
        date = (year*365) + cummulative_days[month-1] + day
        dates.append(date)
        views.append(item['views'])
    
    _,views = zip(*sorted(zip(dates, views)))
    print('views extracted')
    return views

def get_daily_views(search_word,language,access):
    start,end = get_dates()
    url = get_url(search_word,start,end,language,access)
    json = request_url(url)
    views = extract_views_from_json(json)
    return views

def random_string(length=15):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str

def write_to_file(content,fname=''):
    if fname=='':
        fname = random_string() + '.txt'
    path = storage_path + fname
    f = open(path,'w')
    f.write(content)
    f.close()
    return path

    
def plot_graph(*lists,labels=[],colors=[],title='',fname=''):
    plt.clf()
    is_labels = len(labels)>0
    is_colors = len(colors)>0
    if fname=='':
        fname = random_string()+'.png'
    for list in lists:
        label = ''
        if is_labels:
            label = labels[0]
            labels = labels[1:]
        else:
            label = ''
        if is_colors:
            color = colors[0]
            colors = colors[1:]
            plt.plot(list,label=label,color=color)
        else:
            plt.plot(list,label=label)
    plt.title(title)
    plt.xlabel('Days')
    plt.ylabel('Views')
    if is_labels:
        plt.legend()
    plt.savefig(storage_path+fname)
    return storage_path+fname

