def rubify(kanji: str, kana: str, sep='|'):
    if not kana:
        return kanji
    if kanji.count(sep) != kana.count(sep):
        raise ValueError('number of separators doesn\'t match')
    elif sep in kanji:
        kanji, kana = kanji.split(sep), kana.split(sep)
        return ''.join(rubify(kj, kn) for kj, kn in zip(kanji, kana))
    else:
        # find longest common substr of kanji and kana
        dplastrow, dprow = None, None
        lcidx = None
        maxl = 0
        for ikj, ckj in enumerate(kanji):
            dprow = [0 for _ in kana]
            for ikn, ckn in enumerate(kana):
                if ckj == ckn:
                    if ikj == 0 or ikn == 0:
                        curl = 1
                    else:
                        curl = dplastrow[ikn-1] + 1
                    dprow[ikn] = curl
                    cond = curl > maxl and \
                        ((ikj-curl+1 == 0) == (ikn-curl+1 == 0)) and \
                        ((ikj == len(kanji)-1) == (ikn == len(kana)-1))
                    if cond:
                        maxl = curl
                        lcidx = (ikj-curl+1, ikn-curl+1, curl)
                else:
                    dprow[ikn] = 0
            dplastrow = dprow
        if lcidx is None:
            # no common part
            return '<ruby>{}<rt>{}</rt></ruby>'.format(kanji, kana)
        else:
            kji1, kji2 = lcidx[0], lcidx[0]+lcidx[2]
            kni1, kni2 = lcidx[1], lcidx[1]+lcidx[2]
            kanji1, kanji2, kanji3 = kanji[:kji1], kanji[kji1:kji2], kanji[kji2:]
            kana1, kana2, kana3 = kana[:kni1], kana[kni1:kni2], kana[kni2:]
            return rubify(kanji1, kana1) + kanji2 + rubify(kanji3, kana3)
        
if __name__ == '__main__':
    with open('in.txt', encoding='utf-8') as fi, open('out.txt', 'w', encoding='utf-8') as fo:
        for line in fi:
            kanji, kana, *_ = line.rstrip().split('\t')
            ruby = rubify(kanji, kana, '/')
            print(ruby)
            fo.write(ruby+'\n')
