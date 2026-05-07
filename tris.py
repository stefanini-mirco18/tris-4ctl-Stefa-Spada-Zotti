#logica del gioco
def crea_tabella():
   return [" " for _ in range(9)]

def stampa_tabella(t):
   for i in range(0, 9, 3):
       print(f" {t[i]} | {t[i+1]} | {t[i+2]} ")
       if i < 6: print("-----------")

def controlla_vittoria(t):
   combo = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
   for a, b, c in combo:
       if t[a] == t[b] == t[c] != " ":
           return t[a]
   if " " not in t:
       return "Pareggio"
   return None
