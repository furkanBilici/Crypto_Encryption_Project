def rail_fence_cipher(text,r):
    sifre=[]
    cycle=2*(r-1)
    lss={}
    for i in range(r):
        lss[i] = []

    for i in range(0,len(text)):
        t=i%cycle
        if t<r:
            lss[t].append(text[i])
        if t>=r:
            lss[cycle-t].append(text[i]) 

    for i in range(0,len(lss)):
        for char in lss[i]:
            sifre.append(char)

    return ''.join(sifre)               
