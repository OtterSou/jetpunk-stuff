def hira2kata(s):
    return ''.join(chr(ord(c)+0x60) if 'ぁ' <= c <= 'ゖ' else c for c in s)


def allromaji(kana, table):
    def pipe(lst):
        if len(lst) == 0:
            return ''
        if len(lst) == 1:
            return lst[0]
        else:
            return '(' + '|'.join(lst) + ')'

    def _allromaji(kana):
        if not kana:
            return ''
        match = [k for k in table if kana.startswith(k)]
        if not match:
            raise ValueError(kana + ' is not convertible')
        longest = max(len(x) for x in match)
        out = pipe([pipe(table[x]) + _allromaji(kana[len(x):longest])
                    for x in match])
        out += _allromaji(kana[longest:])
        return out
    return _allromaji(hira2kata(kana))


table = []
with open('romantable.txt', encoding='utf-8') as f:
    for line in f:
        table.append(tuple(line.rstrip().split('\t')))
newtable = []
# add っ-
for romaji, kana in table:
    if romaji[0] in 'bcdfghjklmpqrstvwxyz':
        newtable.append((romaji[0]+romaji, 'ッ'+kana))
table.extend(newtable)
newtable = []
# add ん-
for romaji, kana in table:
    if romaji[0] not in 'aeiouy':
        newtable.append(('n'+romaji, 'ン'+kana))
table.extend(newtable)

k2r = {}
for romaji, kana in table:
    if kana not in k2r:
        k2r[kana] = []
    k2r[kana].append(romaji)

inlist = []
with open('in.txt',encoding='utf-8') as f:
    for line in f:
        inlist.append(line.rstrip('\r\n'))

outlist = ['r:^{}'.format(allromaji(hira,k2r)) for hira in inlist]

with open('out.txt','w',encoding='utf-8') as f:
    for line in outlist:
        f.write(line)
        f.write('\n')
