import database
import tris

def nuova_partita():
   nome1 = input("Nome Giocatore 1 (X): ")
   nome2 = input("Nome Giocatore 2 (O): ")
   while nome1==nome2:
       print("Nome gia' utilizzato, riprova con un altro")
       nome2 = input("Nome Giocatore 2 (O): ")
   # Recuperiamo gli ID (fondamentali per le Foreign Keys)
   id1 = database.ottieni_o_crea_giocatore(nome1)
   id2 = database.ottieni_o_crea_giocatore(nome2)
  
   tabella = tris.crea_tabella()
   turno = "X"
   vincitore_segno = None
  
   while not vincitore_segno:
       tris.stampa_tabella(tabella)
       try:
           attuale_nome = nome1 if turno == "X" else nome2
           mossa = int(input(f"Turno di {turno} ({attuale_nome}). Scegli (0-8): "))
           if 0 <= mossa <= 8 and tabella[mossa] == " ":
               tabella[mossa] = turno
               vincitore_segno = tris.controlla_vittoria(tabella)
               if not vincitore_segno:
                   turno = "O" if turno == "X" else "X"
           else:
               print("Mossa non valida!")
       except ValueError:
           print("Inserisci un numero!")

   tris.stampa_tabella(tabella)

   # Determiniamo l'ID del vincitore
   id_vincitore = None # Default Pareggio
   if vincitore_segno == "X":
       id_vincitore = id1
       print(f"Vince {nome1}!")
   elif vincitore_segno == "O":
       id_vincitore = id2
       print(f"Vince {nome2}!")
   else:
       print("Pareggio!")

   # Salviamo usando gli ID
   database.salva_partita(id1, id2, id_vincitore)

def menu_statistiche():
   print("\n--- STATISTICHE ---")
   print("1. Top 5 Giocatori")
   print("2. Cerca Giocatore")
   scelta = input("Scelta: ")
  
   if scelta == "1":
       top = database.classifica_top_5()
       for i, (nome, vit) in enumerate(top, 1):
           print(f"{i}. {nome} - {vit} vittorie")
   elif scelta == "2":
       nome = input("Inserisci nome: ")
       s = database.statistiche_giocatore(nome)
       if s:
           print(f"\nGiocatore: {nome}")
           print(f"Partite: {s['totali']} | Vinte: {s['vinte']} | Perse: {s['perse']} | Pareggi: {s['pareggi']} | Win Rate: {s['win_rate']:.2f}%")
       else:
           print("Giocatore non trovato.")

def main():
   try:
       database.inizializza_db()
       while True:
           print("\n--- TRIS & SQL ---")
           print("1. Nuova Partita")
           print("2. Statistiche")
           print("3. Esci")
           scelta = input("Scelta: ")
          
           if scelta == "1": nuova_partita()
           elif scelta == "2": menu_statistiche()
           elif scelta == "3": break
   except Exception as e:
       print(f"Errore: {e}")

if __name__ == "__main__":
   main()
