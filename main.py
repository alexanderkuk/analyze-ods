# encoding: utf8

import re
import os
import json
import math
from collections import namedtuple, Counter, defaultdict, OrderedDict
from datetime import datetime, timedelta
from random import seed as random_seed
from random import sample, random

import pandas as pd
import numpy as np

import seaborn as sns
from adjustText import adjust_text
from matplotlib import pyplot as plt
from matplotlib import rc
# For cyrillic labels
rc('font', family='Verdana', weight='normal')

import networkx as nx

from bs4 import BeautifulSoup

# from sklearn.manifold import TSNE
from MulticoreTSNE import MulticoreTSNE as TSNE
from sklearn.cluster import KMeans


from IPython.display import HTML, display


DATA_DIR = 'data'
DUMP_DIR = os.path.join(DATA_DIR, 'dump')
USERS = os.path.join(DUMP_DIR, 'users.json')
CHANNELS = os.path.join(DUMP_DIR, 'channels.json')
VIZ_DIR = 'viz'
VIZ_DATA_DIR = os.path.join(VIZ_DIR, 'data')
CHANNELS_VIZ_DATA = os.path.join(VIZ_DATA_DIR, 'channels.json')
USERS_VIZ_DATA = os.path.join(VIZ_DATA_DIR, 'users.json')
MESSAGES_BY_TIME_VIZ_DATA = os.path.join(VIZ_DATA_DIR, 'messages_by_time.json')
MESSAGES_BY_CHANNELS_VIZ_DATA = os.path.join(VIZ_DATA_DIR, 'messages_by_channels.json')
USERS_BY_TIME_VIZ_DATA = os.path.join(VIZ_DATA_DIR, 'users_by_time.json')

GRAPH = 'graph.gexf'
EMOJI_MENU = os.path.join(DATA_DIR, 'emoji_menu.html')

TEXT = 'text'
OTHER = 'other'
OTHER_COLOR = 'silver'

DAY_NAMES = [
    u'пн',
    u'вт',
    u'ср',
    u'чт',
    u'пт',
    u'сб',
    u'вс',
]

MALE = 'male'
FEMALE = 'female'

FEMALE_NAMES = {
    u'olga', u'irina', u'anna', u'kate', u'julia',
    u'alina', u'daria', u'ekaterina', u'anastasiia', u'natalia',
    u'tatiana', u'yulia', u'evgenia', u'polina', u'alena',
    u'alexandra', u'marina', u'olya', u'ksenia', u'svetlana',
    u'masha', u'maria', u'yana', u'liza', u'karina', u'darya',
    u'margarita', u'anastasiya', u'tatyana', u'ana', u'oksana',
    u'mary', u'vera', u'khrystyna', u'nataliya', u'mariya', u'aida',
    u'elena', u'лера', u'olha', u'sara', u'nataliia',
    u'kseniya', u'ирина', u'катерина', u'ira', u'alisa', u'мария',
    u'марина', u'ai', u'dasza', u'валерия', u'olia', u'diana',
    u'олеся', u'юлия', u'vasyl', u'olena', u'дарья', u'klara',
    u'гульнара', u'vlada', u'анна', u'oleksandra', u'виктория',
    u'helen', u'ксения', u'tanya', u'ольга', u'вероника', u'veronika',
    u'victoria', u'marta', u'алёна', u'yuliia',
}
MALE_NAMES = {
    u'alexander', u'dmitry', u'andrey', u'sergey', u'volodymyr',
    u'anton', u'pavel', u'ivan', u'mikhail', u'alexey', u'alex',
    u'ilya', u'nikita', u'roman', u'vladimir', u'kirill', u'igor',
    u'oleg', u'artem', u'evgeny', u'denis', u'konstantin', u'maxim',
    u'max', u'dmitriy', u'vlad', u'vladislav', u'андрей', u'nikolay',
    u'aleksandr', u'anastasia', u'vadim', u'sergei',
    u'alexandr', u'stanislav', u'egor', u'александр', u'ruslan',
    u'eugene', u'aleksey', u'gleb', u'daniil', u'fedor', u'andrew',
    u'dmitrii', u'дмитрий', u'yury', u'andrei', u'vasily', u'yuriy',
    u'michael', u'boris', u'anatoly', u'valentin', u'евгений',
    u'evgenii', u'leonid', u'artur', u'dima', u'vitaly', u'oleksandr',
    u'vsevolod', u'mike', u'maksim', u'михаил', u'dmytro', u'vasiliy',
    u'никита', u'artyom', u'orlov', u'олег', u'serge', u'yuri',
    u'georgy', u'evgeniy', u'mark', u'taras', u'andrii', u'victor',
    u'vyacheslav', u'maksym', u'danil', u'сергей', u'bohdan',
    u'артём', u'rustam', u'petr', u'владимир', u'илья', u'игорь',
    u'антон', u'marat', u'иван', u'aleksei', u'arthur', u'tigran',
    u'viktor', u'viacheslav', u'константин', u'peter', u'dasha',
    u'кирилл', u'misha', u'bogdan', u'oleh', u'nik', u'grigorii',
    u'svyatoslav', u'arsenii', u'aliaksei', u'kim', u'roma', u'aram',
    u'миша', u'timofei', u'timofey', u'tim', u'yura', u'bulat',
    u'григорий', u'serhiy', u'serhii', u'vitaliy', u'valery',
    u'vasilii', u'nikolaev', u'stepan', u'yaroslav', u'gennady',
    u'vladyslav', u'арсений', u'anthony', u'timur', u'grigory',
    u'yurii', u'павел', u'rinat', u'nick', u'arseny', u'grisha',
    u'arsen', u'yan', u'slava', u'fyodor', u'i', u'valeriy', u'philipp',

    u'oleksii', u'ievgenii', u'arman', u'eugeny', u'serjio', u'вадим',
    u'grigoriy', u'jeorge', u'вячеслав', u'serg', u'ihor', u'алексей',
    u'veaceslav', u'daniel', u'артур', u'даниил', u'dennis', u'semen',
    u'ilia', u'arkady', u'виталий', u'kostia', u'юрий', u'родион',
    u'vas3k',
}
MALE_SUFFIXES = {
    u'ov', u'in', u'ev', u'ов', u'ин', u'ев',
}
FEMALE_SUFFIXES = {
    u'ova', u'ina', u'eva',
}
DEFAULT_CHANNELS = {
    u'_random_flood', u'_meetings', u'deep_learning', u'visualization',
    u'lang_r', u'lang_python', u'theory_and_practice', u'_jobs', u'welcome',
    u'edu_courses', u'interesting_links', u'datasets', u'_general', 
    u'kaggle_crackers', u'mltrainings_live', u'mltrainings_beginners', u'nlp',
    u'career', 'bots'
}


User_ = namedtuple(
    'User',
    ['id', 'name', 'fio', 'image', 'bot']
)

class User(User_):
    def __repr__(self):
        return 'User(name={name!r}, ...)'.format(
            name=self.name
        )

Channel_ = namedtuple(
    'Channel',
    ['id', 'name', 'active', 'creator', 'created', 'members',
     'purpose', 'topic']
)

class Channel(Channel_):
    def __repr__(self):
        return 'Channel(name={name!r}, ...)'.format(
            name=self.name
        )

Reaction = namedtuple(
    'Reaction',
    ['name', 'user']
)
Message = namedtuple(
    'Message',
    ['channel', 'type', 'user', 'posted', 'text', 'reactions']
)
UnknownChannel = namedtuple(
    'UnknownChannel',
    ['id']
)
Command = namedtuple(
    'Command',
    ['name', 'text']
)
Url = namedtuple(
    'Url',
    ['href', 'text']
)

USER = 'user'
CHANNEL = 'channel'
UNKNOWN_CHANNEL = 'unknown_channel'
COMMAND = 'command'
URL = 'url'

Token = namedtuple(
    'Token',
    ['type', 'value']
)

class Text(unicode):
    def __new__(cls, value, tokens):
         object = unicode.__new__(cls, value)
         object.tokens = tokens
         return object


USLACKBOT = User(
    id='USLACKBOT',
    name='slackbot',
    fio='Slack Bot',
    image=None,
    bot=True
)


Edge = namedtuple(
    'Edge',
    ['source', 'target', 'weight']
)
EmojiMenuRecord = namedtuple(
    'EmojiMenuRecord',
    ['name', 'style']
)
UserCard = namedtuple(
    'UserCard',
    ['name', 'image', 'joined',
     'messages', 'welcome_message',
     'channel_messages', 'channel_date_messages', 'top_messages']
)


def log_progress(sequence, every=None, size=None):
    from ipywidgets import IntProgress, HTML, VBox
    from IPython.display import display

    is_iterator = False
    if size is None:
        try:
            size = len(sequence)
        except TypeError:
            is_iterator = True
    if size is not None:
        if every is None:
            if size <= 200:
                every = 1
            else:
                every = size / 200     # every 0.5%
    else:
        assert every is not None, 'sequence is iterator, set every'

    if is_iterator:
        progress = IntProgress(min=0, max=1, value=1)
        progress.bar_style = 'info'
    else:
        progress = IntProgress(min=0, max=size, value=0)
    label = HTML()
    box = VBox(children=[label, progress])
    display(box)

    index = 0
    try:
        for index, record in enumerate(sequence, 1):
            if index == 1 or index % every == 0:
                if is_iterator:
                    label.value = '{index} / ?'.format(index=index)
                else:
                    progress.value = index
                    label.value = u'{index} / {size}'.format(
                        index=index,
                        size=size
                    )
            yield record
    except:
        progress.bar_style = 'danger'
        raise
    else:
        progress.bar_style = 'success'
        progress.value = index
        label.value = str(index or '?')


def read_json_list(path):
    with open(path) as file:
        data = json.load(file)
        for record in data:
            yield record


def load_users():
    #     [(u'profile', 1921),
    #  (u'name', 1921),
    #  (u'deleted', 1921),
    #  (u'is_bot', 1921),
    #  (u'team_id', 1921),
    #  (u'id', 1921),
    #  (u'status', 1918),  # deleted users lack these fields
    #  (u'tz', 1918),      # just 3 users were deleted
    #  (u'tz_label', 1918),
    #  (u'real_name', 1918),
    #  (u'color', 1918),
    #  (u'is_admin', 1918),
    #  (u'is_ultra_restricted', 1918),
    #  (u'is_restricted', 1918),
    #  (u'tz_offset', 1918),
    #  (u'is_primary_owner', 1918),
    #  (u'is_owner', 1918)]
    for record in read_json_list(USERS):
        id = record['id']
        name = record['name']
        bot = record['is_bot']
        fio = record.get('real_name')

        # profile
        #         [(u'fields', 1921),
        #  (u'real_name', 1921),
        #  (u'image_24', 1921),
        #  (u'real_name_normalized', 1921),
        #  (u'image_32', 1921),
        #  (u'image_48', 1921),
        #  (u'avatar_hash', 1921),
        #  (u'image_72', 1921),
        #  (u'image_192', 1921),
        #  (u'image_512', 1891),
        #  (u'first_name', 1735),
        #  (u'last_name', 1716),
        #  (u'title', 809),
        #  (u'skype', 799),
        #  (u'phone', 797),
        #  (u'image_original', 593),
        #  (u'image_1024', 563),
        #  (u'bot_id', 10),
        #  (u'api_app_id', 8),
        #  (u'always_active', 1)]
        image = record['profile']['image_192']

        yield User(id, name, fio, image, bot)


def parse_timestamp(value):
    value = float(value)
    return datetime.fromtimestamp(value)


def load_channels(id_users):
    for record in read_json_list(CHANNELS):
        #         [(u'is_general', 98),
        #  (u'name', 98),
        #  (u'creator', 98),
        #  (u'is_archived', 98),
        #  (u'created', 98),
        #  (u'topic', 98),
        #  (u'purpose', 98),
        #  (u'members', 98),
        #  (u'id', 98),
        #  (u'pins', 36)]
        id = record['id']
        name = record['name']
        active = not record['is_archived']
        creator = id_users[record['creator']]
        created = parse_timestamp(record['created'])
        members = [id_users[_] for _ in record['members']]
        purpose = record['purpose']['value']
        topic = record['topic']['value']
        yield Channel(
            id, name, active, creator, created, members,
            purpose, topic
        )

        
def list_channel_chunks(channel):
    dir = os.path.join(DUMP_DIR, channel.name)
    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        yield path

        
def parse_message_reactions(data, id_users):
    if data is None:
        return
    for item in data:
        name = item['name']
        for id in item['users']:
            user = id_users[id]
            yield Reaction(name, user)
        
        
def unescape_text(text):
    for pattern, value in [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>')]:
        text = text.replace(pattern, value)
    return text


def parse_tag(tag, id_users, id_channels):
    tag = tag[1:-1]  # strip < >
    start = tag[0]
    body = tag[1:]
    id, _, text = body.partition('|')
    if start == '@':
        user = id_users[id]
        return Token(USER, user)
    elif start == '#':
        if id in id_channels:
            return Token(CHANNEL, id_channels[id])
        else:
            # link to private channel for example
            return Token(UNKNOWN_CHANNEL, UnknownChannel(id))
    elif start == '!':
        return Token(COMMAND, Command(id, text))
    else:
        id, _, text = tag.partition('|')
        return Token(URL, Url(id, text))

    
def make_token(text):
    return Token(TEXT, unescape_text(text))


def parse_text(text, id_users, id_channels):
    matches = list(re.finditer(r'(<[^>]+>)', text))
    if not matches:
        yield make_token(text)
    else:
        previous = 0
        for index, match in enumerate(matches):
            start = match.start()
            if start > previous:
                yield make_token(text[previous:start])
            tag = match.group(1)
            yield parse_tag(tag, id_users, id_channels)
            previous = match.end()
        if previous < len(text):
            yield make_token(text[previous:])


def format_token(token):
    type, value = token
    if type == TEXT:
        return value
    elif type == USER:
        return '@' + value.name
    elif type == CHANNEL:
        return '#' + value.name
    elif type == UNKNOWN_CHANNEL:
        return '#' + value.id
    elif type == COMMAND:
        # NOTE use value.text maybe
        return '@' + value.name
    elif type == URL:
        return value.text or value.href
    else:
        raise TypeError(type)


def format_tokens(tokens):
    return ''.join(format_token(_) for _ in tokens)


def parse_message(record, channel, id_users, id_channels):
    #     [(u'ts', 200045),
    #  (u'type', 200045),
    #  (u'text', 199975),
    #  (u'user', 198552),
    #  (u'subtype', 37946),
    #  (u'reactions', 20432),
    #  (u'attachments', 9820),
    #  (u'edited', 9787),
    #  (u'bot_id', 3084),
    #  (u'username', 2621),
    #  (u'file', 1733),
    #  (u'display_as_bot', 1678),
    #  (u'upload', 1678),
    #  (u'icons', 729),
    #  (u'inviter', 515),
    #  (u'item_type', 212),
    #  (u'topic', 95),
    #  (u'mrkdwn', 76),
    #  (u'purpose', 69),
    #  (u'comment', 40),
    #  (u'is_intro', 40),
    #  (u'old_name', 37),
    #  (u'name', 37),
    #  (u'members', 26),
    #  (u'item', 14)]

    # type is always "message", so use subtype as type
    #     [(None, 162099),
    #  (u'channel_join', 33070),
    #  (u'file_share', 1678),
    #  (u'bot_message', 1453),
    #  (u'channel_leave', 1230),
    #  (u'pinned_item', 212),
    #  (u'channel_topic', 95),
    #  (u'channel_purpose', 69),
    #  (u'file_comment', 40),
    #  (u'channel_name', 37),
    #  (u'channel_archive', 26),
    #  (u'file_mention', 15),
    #  (u'bot_add', 11),
    #  (u'bot_remove', 6),
    #  (u'me_message', 2),
    #  (u'channel_unarchive', 1),
    #  (u'reminder_add', 1)]
    # Replace None with TEXT
    type = record.get('subtype', TEXT)
    
    user = None
    if u'user' in record:
        user = id_users[record['user']]
    
    posted = parse_timestamp(record['ts'])

    text = record.get('text')
    if type == TEXT:
        tokens = list(parse_text(text, id_users, id_channels))
        text = Text(format_tokens(tokens), tokens)
    
    reactions = record.get('reactions')
    reactions = list(parse_message_reactions(reactions, id_users))
    
    return Message(channel, type, user, posted, text, reactions)
        
        
def load_messages(channels, id_users, id_channels):
    for channel in channels:
        for path in list_channel_chunks(channel):
            for record in read_json_list(path):
                yield parse_message(record, channel, id_users, id_channels)


def show_messages_per_week(messages):
    table = pd.Series(
        _.posted for _ in messages
    )
    table = table.value_counts()
    fig, ax = plt.subplots()
    table.resample('W').sum().plot(ax=ax)
    ax.set_ylabel(u'Число сообщений в неделю')


def show_messages_per_week_in_bots_flood(messages):
    data = []
    for record in messages:
        channel = record.channel.name
        if channel not in ('bots', '_random_flood', 'career'):
            channel = OTHER
        data.append((record.posted, channel))
    table = pd.DataFrame(
        data,
        columns=['posted', 'channel']
    )
    table = table.groupby(['posted', 'channel']).size()
    table = table.unstack()
    fig, ax = plt.subplots()
    table.resample('W').sum().plot(ax=ax)
    ax.set_ylabel(u'Число сообщений в неделю')


def show_messages_during_day(messages):
    counts = Counter()
    for record in messages:
        timestamp = record.posted
        day = timestamp.isocalendar()[2]
        day = DAY_NAMES[day - 1]
        time = datetime(2000, 1, 1, hour=timestamp.hour, minute=timestamp.minute)
        counts[time, day] += 1
    table = pd.Series(counts)
    table = table.unstack()
    table = table.reindex(columns=DAY_NAMES)
    table = table.resample('1800s').mean()
    fig, ax = plt.subplots()
    table.plot(ax=ax)
    ax.set_ylabel(u'Число сообщений в час')
    ax.grid('off')
    ax.grid(which='minor')
    ax.xaxis.grid(True)
    ax.set_xticks([])


def show_messages_per_week_by_channels(messages, top=40, cols=5, rows=8, width=15, height=16):
    assert top == cols * rows
    data = []
    for record in messages:
        data.append((record.posted, record.channel.name))
    table = pd.DataFrame(
        data,
        columns=['posted', 'channel']
    )
    channels = table.groupby(['posted', 'channel']).size()
    channels = channels.unstack().resample('W').sum()
    channels = channels.mean(axis=0)
    channels = channels.sort_values(ascending=False)
    channels = channels.head(top).index

    left_bound = float('inf')
    right_bound = 0
    fig, axes = plt.subplots(rows, cols, sharex=True)
    for channel, ax in zip(channels, axes.flatten()):
        view = table[table.channel == channel]
        view = view.posted.value_counts()
        view.resample('W').sum().plot(ax=ax)
        ax.set_title(channel)
        left_bound_, right_bound_ = ax.get_xlim()
        left_bound = min(left_bound, left_bound_)
        right_bound = max(right_bound, right_bound_)
    axes[0][0].set_ylabel(u'Число сообщений\n в неделю')
    for ax in axes.flatten():
        ax.set_xlim((left_bound, right_bound))
    
    fig.set_size_inches((width, height))
    fig.tight_layout()


def round_week(date):
    day = date.isocalendar()[2]
    return date - timedelta(day - 1)


def show_users_per_week(messages):
    counts = defaultdict(set)
    for record in messages:
        if record.channel.name not in ('bots', '_random_flood', 'career'):
            date = record.posted.date()
            date = round_week(date)
            counts[date].add(record.user.name)
    table = pd.Series({date: len(users) for date, users in counts.iteritems()})
    table.index = pd.to_datetime(table.index)
    fig, ax = plt.subplots()
    table.plot(ax=ax)
    ax.set_ylabel(u'Число чатящихся в неделю в other')


def show_messages_per_user_per_week(messages):
    users = defaultdict(set)
    hits = Counter()
    for record in messages:
        if record.channel.name not in ('bots', '_random_flood', 'career'):
            date = record.posted.date()
            date = round_week(date)
            users[date].add(record.user.name)
            hits[date] += 1
    table = pd.DataFrame({
        'users': {date: len(names) for date, names in users.iteritems()},
        'messages': hits
    })
    table.index = pd.to_datetime(table.index)
    table = (table.messages / table.users)
    fig, ax = plt.subplots()
    table.plot(ax=ax)
    ax.set_ylabel(u'Число сообщений на пользователя в other')


def get_fio_gender(fio):
    parts = fio.lower().split()
    bag = set(parts)
    if bag & MALE_NAMES:
        return MALE
    elif bag & FEMALE_NAMES:
        return FEMALE
    else:
        for part in parts:
            if part[-2:] in MALE_SUFFIXES:
                return MALE
            elif part[-3:] in FEMALE_SUFFIXES:
                return FEMALE
        return None


def show_fio_gender_stats(users):
    counts = Counter()
    for record in users:
        fio = record.fio
        if fio:
            gender = get_fio_gender(fio)
            if gender == MALE:
                counts[u'Мужской пол'] += 1
            elif gender == FEMALE:
                counts[u'Женский пол'] += 1
            else:
                counts[u'Не удалось определить пол'] += 1
        else:
            counts[u'Не указано имя'] += 1
    table = pd.Series(counts)
    table = table.reindex(index=[
        u'Не удалось определить пол',
        u'Мужской пол',
        u'Женский пол',
        u'Не указано имя',
    ])
    table.plot(kind='barh')


def is_custom_image(image):
    # ep, not 100% accurate
    return 'secure.gravatar.com' not in image


def wrap_sequence(sequence, size=5):
    count = int(math.ceil(len(sequence) / float(size)))
    for index in xrange(count):
        yield sequence[index * size:(index + 1) * size]

        
def format_images(images, size):
    yield '<table style="border:none">'
    for chunk in wrap_sequence(images, size):
        yield '<tr style="border:none">'
        for image in chunk:
            yield '<td style="border:none">'
            yield '<img src="{image}" style="min-width:100px;max-width:100px"/>'.format(
                image=image
            )
            yield '</td>'
        yield '</tr>'
    yield '</table>'

        
def show_html(html):
    display(HTML(html))


def show_images(images, size=5):
    html = '\n'.join(format_images(images, size))
    show_html(html)


def get_sessions(messages, timeout=30 * 60):
    previous = None
    session = []
    for record in messages:
        posted = record.posted
        if previous is None or (posted - previous).seconds < timeout:
            session.append(record)
        else:
            yield session
            session = [record]
        previous = posted
    if session:
        yield session


def separate_joined_by_default(messages):
#     2016-08-24 22:15:57.001692 deep_learning
# 	2016-08-24 22:15:57.002586 theory_and_practice
# 	2016-08-24 22:15:58.000412 _general
# 	2016-08-24 22:15:58.001208 _meetings
# 	2016-08-24 22:15:58.003388 _random_flood
# 	2016-08-28 09:02:45.000002 business
# 	2016-08-28 09:04:21.000002 org_hse_projects
    sessions = list(get_sessions(messages, timeout=3))
    default = sessions[0]
    custom = [
        record
        for session in sessions[1:]
        for record in session
    ]
    return default, custom


def get_user_channel_edges(messages):
    counts = Counter()
    for record in messages:
        counts[record.user.name, record.channel.name] += 1
    for (user, channel), weight in counts.most_common():
        yield Edge(user, channel, weight)


def invert_edges(edges):
    for source, target, weight in edges:
        yield Edge(target, source, weight)


def normalize_counts(counts):
    total = sum(counts.values())
    return Counter({
        key: float(count) / total
        for key, count in counts.iteritems()
    })


def fold_bimodal(edges):
    b_as = defaultdict(Counter)
    a_bs = defaultdict(Counter)
    for a, b, weight in edges:
        b_as[b][a] += weight
        a_bs[a][b] += weight
    for b in b_as:
        b_as[b] = normalize_counts(b_as[b])
    for a in a_bs:
        a_bs[a] = normalize_counts(a_bs[a])
    counts = Counter()
    for source in b_as:
        for a, b_a in b_as[source].iteritems():
            for target, a_b in a_bs[a].iteritems():
                counts[source, target] += b_a * a_b
    for (source, target), weight in counts.most_common():
        yield Edge(source, target, weight)


def write_edges(edges, path=GRAPH):
    graph = nx.DiGraph()
    for source, target, weight in edges:
        graph.add_edge(source, target, weight=weight)
    nx.write_gexf(graph, path)


def get_user_messages(messages):
    user_messages = defaultdict(list)
    for record in messages:
        user = record.user
        if user:
            user_messages[user.name].append(record)
    return user_messages


def show_users_join(messages):
    counts = Counter()
    user_messages = get_user_messages(messages)
    for user in user_messages:
        records = user_messages[user]
        joined = round_week(records[0].posted.date())
        counts[joined] += 1
    table = pd.Series(counts)
    table.index = pd.to_datetime(table.index)
    fig, ax = plt.subplots()
    # table.cumsum().plot(ax=ax)
    table.plot(ax=ax)
    ax.set_ylabel(u'Число зарегистрировавшихся в неделю')


def round_month(date):
    return datetime(date.year, date.month, 1)


def show_churn(messages):
    total = Counter()
    counts = Counter()
    current = round_month(datetime.now())
    user_messages = get_user_messages(messages)
    for user in user_messages:
        records = user_messages[user]
        joined = round_month(records[0].posted)
        months = set()
        for record in records:
            if record.type == TEXT:
                month = round_month(record.posted)
                if month < current:
                    months.add(month)
        total[joined] += 1
        for month in months:
            counts[joined, month] += 1
    total = pd.Series(total)
    table = pd.Series(counts).unstack()
    table = table.div(total, axis=0)
    
    table.index = [_.strftime('%Y-%m') for _ in table.index]
    table.columns = [_.strftime('%Y-%m') for _ in table.columns]
    fig, ax = plt.subplots()
    sns.heatmap(table, annot=True, fmt='0.2f', ax=ax)
    ax.set_ylabel(u'Месяц регистрации')
    ax.set_xlabel(u'Месяц активности')
    fig.set_size_inches(fig.get_size_inches() * 2.5)


def get_soup(html):
    return BeautifulSoup(html, 'lxml')


def load_text(path):
    with open(path) as file:
        text = file.read()
        text = text.decode('utf8')
        return text


def parse_emoji_menu(html):
    soup = get_soup(html)
    for item in soup.find_all('a', class_='emoji_li'):
        names = item['data-names']
        for name in names.split():
            name = name[1:-1]  # strip : :
            style = item.find('span')['style']
            yield EmojiMenuRecord(name, style)


def load_emoji_menu():
    html = load_text(EMOJI_MENU)
    return parse_emoji_menu(html)


EMOJIES = dict(load_emoji_menu())


def is_custom_emoji_style(style):
    return 'background-position' not in style


def format_emoji(name):
    if name in EMOJIES:
        style = EMOJIES[name]
        if is_custom_emoji_style(style):
            yield '<span style="width: 16px; height: 16px; display: inline-block; background-size: contain; background-repeat: no-repeat; {style}"></span><sub>{name}</sub>'.format(style=style, name=name)
        else:
            yield '<span style="width: 16px; height: 16px; display: inline-block; {style}"></span><sub>{name}</sub>'.format(style=style, name=name)
    else:
        yield name


def show_emoji(name):
    html = '\n'.join(format_emoji(name))
    show_html(html)
    

def show_emojis(names):
    html = '\n'.join(
        line
        for name in names
        for line in format_emoji(name)
    )
    show_html(html)


def get_message_reaction_edges(messages):
    counts = Counter()
    for index, record in enumerate(messages):
        source = str(index)
        for reaction in record.reactions:
            target = reaction.name
            counts[source, target] += 1
    for (source, target), weight in counts.most_common():
        yield Edge(source, target, weight)


def format_reaction_edges(edges, nodes, size=8, top=7):
    counts = defaultdict(Counter)
    for source, target, weight in edges:
        counts[source][target] = weight
    
    yield '<table style="border:none">'
    for chunk in wrap_sequence(nodes, size):
        yield '<tr style="border:none">'
        for source in chunk:
            yield '<td style="border:none">'

            for line in format_emoji(source):
                yield line

            yield ' -> <br/>'
                
            for target, weight in counts[source].most_common(top):
                yield '{:.2f}: '.format(weight)
                for line in format_emoji(target):
                    yield line
                yield '<br/>'
            
            yield '</td>'
        yield '</tr>'
    yield '</table>'

    
def show_reaction_edges(edges, nodes, size=8, top=7):
    html = '\n'.join(format_reaction_edges(edges, nodes, size=size, top=top))
    show_html(html)


def get_reactions_top(messages):
    counts = Counter()
    for record in messages:
        for reaction in record.reactions:
            counts[reaction.name] += 1
    for name, count in counts.most_common():
        yield name


def get_channel_messages(messages):
    channel_messages = defaultdict(list)
    for record in messages:
        channel = record.channel.name
        channel_messages[channel].append(record)
    return channel_messages


def get_user_order_edges(messages, timeout=30):
    counts = Counter()
    channel_messages = get_channel_messages(messages)
    for channel in channel_messages:
        records = channel_messages[channel]
        sessions = get_sessions(records, timeout=timeout)
        for session in sessions:
            for index, record in enumerate(session):
                if index > 0:
                    previous = records[index - 1].user.name
                    name = record.user.name
                    if previous != name:
                        counts[previous, name] += 1
    for (source, target), weight in counts.most_common():
        yield Edge(source, target, weight)


def get_user_mention_edges(messages):
    counts = Counter()
    for record in messages:
        source = record.user
        if not source.bot:
            source = source.name
            for token in record.text.tokens:
                if token.type == USER:
                    target = token.value
                    if not target.bot:
                        target = target.name
                        counts[source, target] += 1
    for (source, target), weight in counts.most_common():
        yield Edge(source, target, weight)


def is_custom_reaction(name):
    if name in EMOJIES:
        style = EMOJIES[name]
        return is_custom_emoji_style(style)


def get_tsne_table(messages):
    counts = Counter()
    for record in messages:
        name = record.user.name
        channel = record.channel.name
        counts[name, channel] += 1

    table = pd.Series(counts)
    table = table.unstack(fill_value=0)

    order = table.sum(axis=1).sort_values(ascending=False)
    table = table.reindex(index=order.index)

    # table = table.div(table.sum(axis=0), axis=1)
    table = table.div(table.sum(axis=1), axis=0)
    return order, table


def tsne_users(table):
    model = TSNE(
        n_jobs=4,
        n_components=2,
        random_state=42,
        n_iter=500,
        perplexity=30
    )
    points = model.fit_transform(table.as_matrix())
    return points


def cluster_tsne_users(points):
    kmeans = KMeans(n_clusters=30, random_state=0).fit(points)
    return kmeans.labels_, kmeans.cluster_centers_


def vector_add(a, b):
    assert len(a) == len(b)
    return [x + y for x, y in zip(a, b)]


def scale_vector(vector, scale):
    return [_ * scale for _ in vector]


def weight_colors(palette, weights):
    accumulator = [0, 0, 0]
    assert len(palette) == len(weights)
    for color, weight in zip(palette, weights):
        accumulator = vector_add(
            accumulator,
            scale_vector(
                color,
                weight
            )
        )
    return accumulator


def get_tsne_colors(table):
    palette = sns.color_palette('husl', 20)
    matrix = table.as_matrix()
    users, channels = table.shape
    channel_colors = []
    for index in xrange(channels):
        color = palette[index % len(palette)]
        channel_colors.append(color)
    colors = []
    for index in xrange(users):
        weights = list(matrix[index])
        color = weight_colors(channel_colors, weights)
        colors.append(color)
    channels = table.columns
    channel_colors = dict(zip(channels, channel_colors))
    return channel_colors, colors


def get_tsne_sizes(order):
    return 2 * np.log(order.values) + 1


def show_tsne_users(order, points, colors, sizes, labels, centers):
    clusters = len(set(labels))
    fig, ax = plt.subplots()
    ax.scatter(points[:, 0], points[:, 1], s=sizes, lw=0, c=colors)
    for index, point in enumerate(centers):
        ax.annotate(index, point)
    ax.axis('off')
    fig.set_size_inches((10, 10))


def get_user_cards(users, messages):
    user_messages = get_user_messages(messages)
    for user in users:
        name = user.name
        image = user.image
        if name in user_messages:
            records = user_messages[name]
            joined = records[0].posted
            welcome_message = None
            channel_messages = Counter()
            channel_date_messages = defaultdict(Counter)
            for record in records:
                if record.type == TEXT:
                    channel = record.channel.name
                    channel_messages[channel] += 1
                    channel_date_messages[channel][record.posted] += 1
                    if channel == 'welcome' and welcome_message is None:
                        welcome_message = record
            top_messages = [
                _ for _ in records
                if _.type == TEXT and _.reactions and _ != welcome_message
            ]
            top_messages = sorted(
                top_messages,
                key=lambda _: len(_.reactions),
                reverse=True
            )
            messages = sum(_.type == TEXT for _ in records)
            yield UserCard(
                name, image, joined,
                messages, welcome_message,
                channel_messages, channel_date_messages, top_messages
            )


def show_card_message(message):
    print message.channel.name, message.posted
    print message.text
    show_emojis([_.name for _ in message.reactions])
    print


def show_message(message):
    print message.channel.name, message.user.name, message.posted
    print message.text
    print
    
    
def show_user_card(record, top_channels=10, top_messages=3):
    print record.name, record.joined.date()
    message = record.welcome_message
    if message:
        show_card_message(message)
    for channel, count in record.channel_messages.most_common(top_channels):
        print '\t', count, '\t', channel
    # print
    # messages = record.top_messages
    # if messages:
    #     for message in messages[:top_messages]:
    #         show_card_message(message)


def show_user_messages_per_date(text_messages, selection):
    counts = Counter()
    for record in text_messages:
        name = record.user.name
        if name == selection:
            channel = record.channel.name
            date = record.posted
            counts[date, channel] += 1

    table = pd.Series(counts)
    table = table.unstack()
    order = table.sum(axis=0).sort_values(ascending=False)
    selection = order.head(5).index
    table = table[selection]
    table = table.resample('M').sum()
    table.plot(kind='area')


def show_channels_created(channels, messages, top=10):
    channel_messages = Counter()
    for record in messages:
        channel_messages[record.channel.name] += 1
        
    user_channels = Counter(_.creator.name for _ in channels)
    users = [user for user, _ in user_channels.most_common()]
    palette = sns.color_palette('deep', len(users))

    fig, ax = plt.subplots()
    X = []
    Y = []
    sizes = []
    texts = []
    colors = []
    random_seed(42)
    order = []
    for record in sorted(channels, key=lambda _: _.created):
        x = record.created
        X.append(x)
        user = record.creator.name
        y = users.index(user)
        if y >= top:
            y = top
        y += (random() - 0.5)  / 2
        Y.append(y)
        size = channel_messages[record.name]
        sizes.append(size)
        text = record.name
        order.append(text)
        text = str(len(order))
        text = ax.text(x, y, text, size=7)
        texts.append(text)
        
        color = palette[users.index(user)]
        colors.append(color)
    sizes = np.sqrt(sizes) + 1

    ax.scatter(X, Y, s=sizes, c=colors, lw=0, alpha=0.75)
    labels = users[:top] + [OTHER]
    ax.set_yticks(range(top + 1))
    ax.set_yticklabels(labels)
    adjust_text(
        texts,
        arrowprops={'arrowstyle': '-', 'color': 'silver', 'lw': 0.5},
    )
    fig.autofmt_xdate()
#     ax.set_axis_bgcolor('white')
    ax.set_xlabel('created')
    for chunk in wrap_sequence(list(enumerate(order, 1)), 5):
        for index, channel in chunk:
            print index, channel,
        print


def parse_date(value):
    return datetime.strptime(value, '%Y-%m-%d')


def serialize_date(date):
    return date.strftime('%Y-%m-%d')


def dump_json(data, path):
    with open(path, 'w') as file:
        json.dump(data, file)


def dump_channels_viz_data(channels, messages, top=7):
    channel_messages = Counter()
    for record in messages:
        channel_messages[record.channel.name] += 1

    data = []
    counts = Counter()
    for record in channels:
        name = record.name
        purpose = record.purpose
        created = record.created
        creator = record.creator.name
        counts[creator] += 1
        members = len(record.members)
        messages = channel_messages[name]
        if members:
            data.append({
                'name': name,
                'purpose': purpose,
                'created': serialize_date(created),
                'creator': creator,
                'members': members,
                'messages': messages,
            })
    order = [user for user, count in counts.most_common(top)]
    dump_json({
        'records': data,
        'order': order
    }, CHANNELS_VIZ_DATA)


def dump_users_viz_data(names, points, clusters, user_cards, top_channels=10):
    mapping = {_.name: _ for _ in user_cards}        
    data = []
    for name, point, cluster in zip(names, points, clusters):
        card = mapping[name]
        x, y = point
        cluster = int(cluster)  # numpy.int is not json serializable
        joined = card.joined
        welcome_message = card.welcome_message
        if welcome_message:
            welcome_message = welcome_message.text
        channel_messages = card.channel_messages
        channel_messages = [
            (channel, messages)
            for channel, messages
            in channel_messages.most_common(top_channels)
        ]
        messages = sum(
            messages for channel, messages
            in channel_messages
        )
        data.append({
            'name': name,
            'cluster': cluster,
            'x': x,
            'y': y,
            'joined': serialize_date(joined),
            'welcome_message': welcome_message,
            'channel_messages': channel_messages,
            'messages': messages
        })
    dump_json(data, USERS_VIZ_DATA)


def dump_messages_by_time(messages):
    filler = u'2016-01-10. В эту неделю случилось то-то и то-то.'
    tooltips = {
        OTHER: {
            '2015-12-13': filler,
            '2016-04-24': filler,
            '2016-09-04': filler,
            '2016-11-20': filler,
        },
        '_random_flood': {
            '2015-10-18': filler,
            '2016-03-06': filler,
        },
        'career': {
            '2016-07-31': filler,
            '2016-11-20': filler,
        },
        'bots': {
            '2016-10-16': filler,
        }
    }
    data = []
    selection = ['bots', '_random_flood', 'career']
    for record in messages:
        channel = record.channel.name
        if channel not in selection:
            channel = OTHER
        data.append((record.posted, channel))
    table = pd.DataFrame(
        data,
        columns=['posted', 'channel']
    )
    table = table.groupby(['posted', 'channel']).size()
    table = table.unstack()
    table = table.resample('W').sum()
    # remove last week since it may be not full
    table = table[table.index < table.index.max()]

    data = {}
    for channel in [OTHER] + selection:
        view = table[channel]
        view = view[~view.isnull()]
        series = {}
        for date, messages in view.iteritems():
            date = serialize_date(date)
            series[date] = messages
        data[channel] = series
    for channel in tooltips:
        for date in tooltips[channel]:
            assert date in data[channel], (channel, date)
    # tooltips = defaultdict(dict)
    # for channel in data:
    #     for date in data[channel]:
    #         tooltips[channel][date] = date
    dump_json({
        'records': data,
        'tooltips': tooltips
    }, MESSAGES_BY_TIME_VIZ_DATA)


def dump_messages_by_channels(messages, top=40):
    data = []
    for record in messages:
        channel = record.channel.name
        data.append((record.posted, channel))
    table = pd.DataFrame(
        data,
        columns=['posted', 'channel']
    )
    table = table.groupby(['posted', 'channel']).size()
    table = table.unstack()
    table = table.resample('W').sum()
    table = table[table.index < table.index.max()]

    channels = table.sum(axis=0)
    channels = channels.sort_values(ascending=False)
    channels = list(channels.head(top).index)

    data = {}
    for channel in channels:
        series = table[channel]
        series = series[~series.isnull()]
        series = {
            serialize_date(date): messages
            for date, messages in series.iteritems()
        }
        data[channel] = series

    filler = u'2016-01-10. В эту неделю случилось то-то и то-то.'
    tooltips = defaultdict(dict)
    for channel in data:
        for date in sample(data[channel], 2):
            tooltips[channel][date] = filler

    dump_json({
        'tooltips': tooltips,
        'records': data,
        'order': channels
    }, MESSAGES_BY_CHANNELS_VIZ_DATA)


def dump_users_by_time(messages):
    filler = u'2016-01-10. В эту неделю случилось то-то и то-то.'
    tooltips = {
        '2015-06-29': filler,
        '2016-01-18': filler,
        '2016-04-11': filler,
        '2016-05-23': filler,
        '2016-09-05': filler,
    }

    dates = []
    counts = Counter()
    user_messages = get_user_messages(messages)
    for user in user_messages:
        records = user_messages[user]
        joined = round_week(records[0].posted.date())
        dates.append(joined)
        counts[joined] += 1
    last = max(dates)
    data = {
        serialize_date(date): users
        for date, users in counts.iteritems()
        if date < last
    }
    for date in tooltips:
        assert date in data, date
    dump_json({
        'records': data,
        'tooltips': tooltips
    }, USERS_BY_TIME_VIZ_DATA)


def color_hex(color):
    r, g, b = color
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return '#{r:02x}{g:02x}{b:02x}'.format(
        r=r,
        g=g,
        b=b
    )


def dump_json2(data, path):
    with open(path, 'w') as file:
        string = json.dumps(data, ensure_ascii=False)
        file.write(string.encode('utf8'))


def get_date_month(date):
    return datetime(date.year, date.month, 1)


def dump_users_viz_data2(names, points, colors, channel_colors, user_cards, top_channels=10):
    mapping = {_.name: _ for _ in user_cards}        
    data = []
    for name, point, color in zip(names, points, colors):
        color = color_hex(color)
        card = mapping[name]
        x, y = point
        joined = card.joined
        welcome_message = card.welcome_message
        if welcome_message:
            welcome_message = welcome_message.text

        top = [
            channel
            for channel, messages
            in card.channel_messages.most_common(top_channels)
        ]
        channel_date_messages = card.channel_date_messages
        months = set()
        channel_month_messages = defaultdict(Counter)
        for channel in channel_date_messages:
            if channel not in top:
                name_  = OTHER
            else:
                name_ = channel
            for date in channel_date_messages[channel]:
                count = channel_date_messages[channel][date]
                month = get_date_month(date)
                months.add(month)
                channel_month_messages[name_][month] += count

        months = sorted(months)
        channels = []
        for channel in top + [OTHER]:
            if channel == OTHER:
                color_ = OTHER_COLOR
            else:
                color_ = color_hex(channel_colors.get(channel, [0.1, 0.1, 0.1]))
            messages = [channel_month_messages[channel][_] for _ in months]
            channels.append(OrderedDict([
                ('name', channel),
                ('color', color_),
                ('messages', messages)
            ]))

        messages = card.messages
        data.append(OrderedDict([
            ('name', name),
            ('color', color),
            ('x', x),
            ('y', y),
            ('joined', serialize_date(joined)),
            ('welcome_message', welcome_message),
            ('messages', messages),
            ('channels', channels),
            ('months', [serialize_date(_) for _ in months])
        ]))
    dump_json2(data, USERS_VIZ_DATA)


def dates_range(start, stop, step):
    while start <= stop:
        yield start
        start += timedelta(days=step)


def dump_channels_viz_data2(channels, messages, top=7):
    channel_messages = Counter()
    channel_week_messages = defaultdict(Counter)
    for record in messages:
        if record.type == TEXT:
            name = record.channel.name
            date = round_week(record.posted.date())
            channel_week_messages[name][date] += 1
            channel_messages[name] += 1

    data = []
    counts = Counter()
    for record in channels:
        name = record.name
        purpose = record.purpose
        created = record.created
        creator = record.creator.name
        counts[creator] += 1
        members = len(record.members)
        messages = channel_messages[name]

        week_messages = channel_week_messages[name]
        if week_messages:
            start = min(week_messages)
            stop = max(week_messages)
            for date in dates_range(start, stop, 7):
                if date not in week_messages:
                    week_messages[date] = None
                
            week_messages = OrderedDict([
                (serialize_date(_), week_messages[_])
                for _ in sorted(week_messages)
            ])

        if members:
            data.append(OrderedDict([
                ('name', name),
                ('purpose', purpose),
                ('created', serialize_date(created)),
                ('creator', creator),
                ('members', members),
                ('messages', messages),
                ('week_messages', week_messages)
            ]))
    order = [user for user, count in counts.most_common(top)]
    dump_json2({
        'records': data,
        'order': order
    }, CHANNELS_VIZ_DATA)
