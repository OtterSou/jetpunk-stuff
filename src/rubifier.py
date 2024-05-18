def kata2hira(s):
    return ''.join(chr(ord(c)-0x60) if 'ァ' <= c <= 'ヶ' else c for c in s)


def rubify(kanji: str, kana: str, sep='|'):
    def is_kana(c):
        return 'ぁ' <= c <= 'ゔ'

    def kksplit(s):
        out = []
        last, last_i = None, 0
        for i, c in enumerate(s):
            x = is_kana(c)
            if last is not None and x != last:
                out.append((s[last_i:i], not x))
                last_i = i
            last = x
        else:
            out.append((s[last_i:], last))
        return out
    if kanji.count(sep) != kana.count(sep):
        raise ValueError('number of separators doesn\'t match')
    elif kanji.count(sep) == 0:
        kanji_parts = kksplit(kanji)
        hira_parts = [kata2hira(x) if b else '' for x, b in kanji_parts]
        print(kanji_parts)
        print(hira_parts)
        if len(kanji_parts) == 0:
            return ''
        
        if kanji_parts[0][1]:
            if not kana.startswith(hira_parts[0]):
                raise ValueError('couldn\'t assign furigana')
            hira_index = len(kanji_parts[0][0])
            kp_index = 1
        else:
            hira_index = 0
            kp_index = 0
        while len(kanji_parts)-kp_index >= 2:
            print(hira_index, kp_index)
            next_hira_index = kana.find(hira_parts[kp_index+1], hira_index)
            next_hira_len = len(hira_parts[kp_index+1])
            if next_hira_index == -1:
                raise ValueError('couldn\'t assign furigana')
            hira_parts[kp_index] = kana[hira_index:next_hira_index]
            hira_index = next_hira_index + next_hira_len
            kp_index += 2
        if kp_index < len(kanji_parts):
            hira_parts[-1] = kana[hira_index:]
        return ''.join(kanji_parts[i][0] if kanji_parts[i][1] or not hira_parts[i] else
                       '<ruby>{}<rt>{}</rt></ruby>'.format(
                           kanji_parts[i][0], hira_parts[i])
                       for i in range(len(kanji_parts)))
    else:
        kanji, kana = kanji.split(sep), kana.split(sep)
        return ''.join(rubify(kj, kn) for kj, kn in zip(kanji, kana))


with open('in.txt', encoding='utf-8') as fi, open('out.txt', 'w', encoding='utf-8') as fo:
    for line in fi:
        kanji, kana, *_ = line.rstrip().split('\t')
        ruby = rubify(kanji, kana)
        print(ruby)
        fo.write(ruby+'\n')
