import pymysql

def get_connection():
   return pymysql.connect(
       host="127.0.0.1",
       user="4CTL_stefa.M.061007",
       password="cavalloverde69",
       database="4CTL_stefa.M.061007",
       port=3307,
       connect_timeout=5,
       autocommit=True
   )

def inizializza_db():
   conn = get_connection()
   with conn.cursor() as cursor:
       # Tabella Giocatori
       cursor.execute('''CREATE TABLE IF NOT EXISTS giocatori (
                           id INT AUTO_INCREMENT PRIMARY KEY,
                           nome VARCHAR(255) UNIQUE NOT NULL,
                           partite_giocate INT DEFAULT 0,
                           vittorie INT DEFAULT 0,
                           pareggi INT DEFAULT 0,
                           sconfitte INT DEFAULT 0)''')
      
       # Tabella Partite con FOREIGN KEY reali
       cursor.execute('''CREATE TABLE IF NOT EXISTS partite (
                           id INT AUTO_INCREMENT PRIMARY KEY,
                           id_giocatore1 INT,
                           id_giocatore2 INT,
                           id_vincitore INT NULL,
                           data_ora DATETIME DEFAULT CURRENT_TIMESTAMP,
                           FOREIGN KEY (id_giocatore1) REFERENCES giocatori(id) ON DELETE CASCADE,
                           FOREIGN KEY (id_giocatore2) REFERENCES giocatori(id) ON DELETE CASCADE,
                           FOREIGN KEY (id_vincitore) REFERENCES giocatori(id) ON DELETE SET NULL)''')
   conn.close()

def ottieni_o_crea_giocatore(nome):
   conn = get_connection()
   with conn.cursor() as cursor:
       cursor.execute("INSERT IGNORE INTO giocatori (nome) VALUES (%s)", (nome,))
       cursor.execute("SELECT id FROM giocatori WHERE nome = %s", (nome,))
       id_giocatore = cursor.fetchone()[0]
   conn.close()
   return id_giocatore

def salva_partita(id1, id2, id_vincitore):
   """
   id_vincitore deve essere l'ID del giocatore oppure None in caso di pareggio
   """
   conn = get_connection()
   with conn.cursor() as cursor:
       # salvo la partita usando gli ID
       cursor.execute("INSERT INTO partite (id_giocatore1, id_giocatore2, id_vincitore) VALUES (%s, %s, %s)",
                      (id1, id2, id_vincitore))
      
       # aggiorno statistiche
       cursor.execute("UPDATE giocatori SET partite_giocate = partite_giocate + 1 WHERE id IN (%s, %s)", (id1, id2))
      
       if id_vincitore:
           # Vittoria
           cursor.execute("UPDATE giocatori SET vittorie = vittorie + 1 WHERE id = %s", (id_vincitore,))
           # Sconfitta
           id_perdente = id2 if id_vincitore == id1 else id1
           cursor.execute("UPDATE giocatori SET sconfitte = sconfitte + 1 WHERE id = %s", (id_perdente,))
       else:
           # Pareggio
           cursor.execute("UPDATE giocatori SET pareggi = pareggi + 1 WHERE id IN (%s, %s)", (id1, id2))
   conn.close()

def classifica_top_5():
   conn = get_connection()
   with conn.cursor() as cursor:
       cursor.execute("SELECT nome, vittorie FROM giocatori ORDER BY vittorie DESC LIMIT 5")
       risultati = cursor.fetchall()
   conn.close()
   return risultati

def statistiche_giocatore(nome):
   conn = get_connection()
   with conn.cursor() as cursor:
       cursor.execute("SELECT partite_giocate, vittorie, sconfitte, pareggi FROM giocatori WHERE nome = %s", (nome,))
       res = cursor.fetchone()
       if not res: return None
       totali, vinte, perse, pareggi = res
       win_rate = (vinte / totali * 100) if totali > 0 else 0
   conn.close()
   return {"totali": totali, "vinte": vinte, "perse": perse, "pareggi": pareggi, "win_rate": win_rate}
