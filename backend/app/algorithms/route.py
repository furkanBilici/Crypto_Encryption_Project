def route_cipher(text, key, saatYonu=True):
    satirlar = [list(text[i:i + key]) for i in range(0, len(text), key)]
    son_satir_uzunlugu = len(satirlar[-1])
    if son_satir_uzunlugu < key:
        satirlar[-1] += ['*'] * (key - son_satir_uzunlugu)

    satir_sayisi = len(satirlar)
    sutun_sayisi = key
    sifre = []

    sol, sag = 0, sutun_sayisi - 1
    ust, alt = 0, satir_sayisi - 1

    while sol <= sag and ust <= alt:
        if saatYonu:
            for i in range(sol, sag + 1):
                sifre.append(satirlar[ust][i])
            ust += 1

            for i in range(ust, alt + 1):
                sifre.append(satirlar[i][sag])
            sag -= 1

            if ust <= alt:
                for i in range(sag, sol - 1, -1):
                    sifre.append(satirlar[alt][i])
                alt -= 1

            if sol <= sag:
                for i in range(alt, ust - 1, -1):
                    sifre.append(satirlar[i][sol])
                sol += 1
        else:
            for i in range(ust, alt + 1):
                sifre.append(satirlar[i][sol])
            sol += 1

            for i in range(sol, sag + 1):
                sifre.append(satirlar[alt][i])
            alt -= 1

            if sol <= sag:
                for i in range(alt, ust - 1, -1):
                    sifre.append(satirlar[i][sag])
                sag -= 1

            if ust <= alt:
                for i in range(sag, sol - 1, -1):
                    sifre.append(satirlar[ust][i])
                ust += 1

    return ''.join(sifre)
