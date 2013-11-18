__author__ = 'a.libkind'
import json
import os

# [cost, ppl gain, ppl need, income gold, max ppl, max warriors]
#buildings = {'house': [5, 0, 0, 0.5, 8, 0],
#             'farm': [10, 0, 0, 3, 0, 0],
#             'smith': [25, 0, 2, 10, 0, 0],
#            'barracks': [50, 0, 2, -5, 0, 20]}

dic = {'name': '', 'cost': 0, 'ppl gain': 0, 'ppl need': 0, 'income gold': 0, 'max ppl': 0, 'max warriors': 0}

vill_name_dict = {'part1': ['Ae', 'Di', 'Mo', 'Fam', 'Hok', 'War', 'Fag', 'Kro', 'Li', 'Mef', 'Ilym', 'As', 'Uet'],
                  'part2': ['dar', 'kil', 'glar', 'tres', 'isk', 'trin', 'ren', 'rtol', 'tan', 'jas', 'lis', 'gitr',
                            'dasg', 'okis', 'tepr', '-Ponyville']}


def dump_all(data):
    for key in data:
        filename = 'buildings\\' + key + '.structure'
        dump = dict()
        dump['name'] = key
        dump['cost'] = data[key][0]
        dump['ppl gain'] = data[key][1]
        dump['ppl need'] = data[key][2]
        dump['income gold'] = data[key][3]
        dump['max ppl'] = data[key][4]
        dump['max warriors'] = data[key][5]
        with open(filename, 'w+') as f:
            f.write(json.dumps(dump))


def load_all():
    data = dict()
    for name in os.listdir('buildings'):
        if len(name.split('.')) > 1:
            if name.split('.')[1] == 'structure' and not name.split('.')[0] == 'template':
                print 'loading ', name
                raw_data = json.loads(open('buildings\\' + name, 'r').read())
                data[raw_data['name']] = parse_data(raw_data)
    return data


def parse_data(raw_data):
    res = []
    res.append(raw_data['cost'])
    res.append(raw_data['ppl gain'])
    res.append(raw_data['ppl need'])
    res.append(raw_data['income gold'])
    res.append(raw_data['max ppl'])
    res.append(raw_data['max warriors'])
    return res


if __name__ == '__main__':

    #dump_all(buildings)
    buildings2 = load_all()
    #print buildings
    print buildings2


