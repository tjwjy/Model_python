import powerlow as pl

def get_simple_grid(dimenssionX,dimenssionY,powerlow_args=0):
    L_Place = []
    tag = 0
    for i in range(1, dimenssionX + 1):
        for j in range(1, dimenssionY + 1):
            L_Place.append([i, j, tag,1])
            tag = tag + 1
    return L_Place
def get_powerlaw_grid(dimenssionX,dimenssionY,powerlow_args=[-2,1,17]):
    beta=powerlow_args[0]
    min=powerlow_args[1]
    max=powerlow_args[2]
    size=dimenssionX*dimenssionY
    pl_rvs=pl.get_int_powerlaw(beta,min,max,size)
    L_Place = []
    tag = 0
    for i in range(1, dimenssionX + 1):
        for j in range(1, dimenssionY + 1):
            L_Place.append([i, j, tag,1])
            tag = tag + 1
    for i,rvs in enumerate(pl_rvs):
        L_Place[i][3]=rvs
    return L_Place

powerlowArgs=[-2,1,13]
grid=get_powerlaw_grid(powerlow_args=powerlowArgs,dimenssionX=20,dimenssionY=20)
a=1

