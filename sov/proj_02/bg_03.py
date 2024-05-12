# dict transform data
def transform(cod):
        codex = {
        9 :('U0','N',7),
        10:('U0','F',7),
        11:('U0','H',7),
        12:('U1','N',7),
        13:('U1','F',7),
        14:('U1','H',7),
        # 15:(U0,F,7),
        # 16:(U0,F,7),
        # 17:(U0,F,7),
        # 18:(U0,F,7),
        # 19:(U0,F,7),
        # 20:(U0,F,7),
        # 21:(U0,F,7),
        # 22:(U0,F,7),
        # 23:(U0,F,7),
        # 24:(U0,F,7),
        # 25:(U0,F,7),
        # 26:(U0,F,7),
        # 27:(U0,F,7),
        # 28:(U0,F,7),
        # 29:(U0,F,7),
        # 30:(U0,F,7),
        # 31:(U0,F,7),
        # 32:(U0,F,7),
        # 33:(U0,F,7),
        # 34:(U0,F,7),
        # 35:(U0,F,7),
        # 36:(U0,F,7),
        # 37:(U0,F,7),
        # 38:(U0,F,7),
        # 39:(U0,F,7),
        # 40:(U0,F,7),
        # 41:(U0,F,7),
        # 42:(U0,F,7),
        # 43:(U0,F,7),
        # 44:(U0,F,7)
    }
        for key, val in codex.items():
            if   key == cod:
                cond_cod = True
                break            
        if cond_cod: 
            return codex[key]
        else: 
            print('code not defined!')
            
