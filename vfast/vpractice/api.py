#!/use/bin/env python
# encoding: utf-8

def rank_front(rank_result, userid):
    for user in rank_result:
        if user['id'] == userid:
            position = rank_result.index(user)
    if position < 9:
        topten = rank_result[:10]
        rank = 1
        for i in topten:
            i['position'] = rank
            rank += 1
    else:
        topten = rank_result[:10]
        rank = 1
        for i in topten:
            i['position'] = rank
            rank += 1
        front = rank_result[position - 1]
        front['position'] = position -1
        current = rank_result[position]
        current['postion'] = position
        try:
            behind = rank_result[position + 1]
            behind['postion'] = position + 1
            topten.append(front, current,behind)
        except:
            pass
        topten.append(front, current)
    for item in topten:
        if item.has_key('repatation'):
            item['repatation'] = str(item['repatation'])
        elif item.has_key('score'):
            item['score'] = str(item['score'])
        else:
            pass
    return topten

