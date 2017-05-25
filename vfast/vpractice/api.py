#!/use/bin/env python
# encoding: utf-8

def rank_front(rank_result, userid):
    for user in rank_result:
        if user['id'] == userid:
            position = rank_result.index(user)
    if position < 9:
        topten = rank_result[:10]
    else:
        topten = rank_result[:10]
        topten.append(rank_result[position - 1])
        topten.append(rank_result[position])
        try:
            topten.append(rank_result[position + 1])
        except IndexError:
            pass
    for item in topten:
        if item.has_key('repatation'):
            item['repatation'] = str(item['repatation'])
        elif item.has_key('score'):
            item['score'] = str(item['score'])
        else:
            pass
    return topten

