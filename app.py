    # -*- coding: utf-8 -*-
    # Génie Civil Pro : application autonome, données séparées du code.
while True:
    SCHEMA_SQL = "CREATE TABLE IF NOT EXISTS utilisateurs (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                identifiant TEXT UNIQUE NOT NULL,\n                nom_complet TEXT NOT NULL,\n                mot_de_passe_hash TEXT NOT NULL,\n                role TEXT NOT NULL,\n                actif INTEGER NOT NULL DEFAULT 1,\n                derniere_connexion TEXT\n            );\nCREATE TABLE IF NOT EXISTS chantiers (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                code TEXT UNIQUE NOT NULL,\n                nom TEXT NOT NULL,\n                budget_fcfa REAL NOT NULL,\n                date_debut TEXT NOT NULL,\n                date_fin_prevue TEXT NOT NULL,\n                client TEXT,\n                localisation TEXT,\n                statut TEXT NOT NULL DEFAULT 'en_cours',\n                supprime INTEGER DEFAULT 0\n            );\nCREATE TABLE IF NOT EXISTS journalier (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                chantier_id INTEGER NOT NULL,\n                date_jour TEXT NOT NULL,\n                meteo TEXT,\n                effectif INTEGER,\n                travaux_realises TEXT,\n                incidents TEXT,\n                supprime INTEGER DEFAULT 0,\n                FOREIGN KEY (chantier_id) REFERENCES chantiers(id)\n            );\nCREATE TABLE IF NOT EXISTS malfacons (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                chantier_id INTEGER NOT NULL,\n                element TEXT NOT NULL,\n                type_defaut TEXT NOT NULL,\n                criticite TEXT NOT NULL,\n                description TEXT,\n                action_corrective TEXT,\n                statut_resolution TEXT NOT NULL DEFAULT 'Ouvert',\n                date_signalement TEXT NOT NULL,\n                supprime INTEGER DEFAULT 0,\n                FOREIGN KEY (chantier_id) REFERENCES chantiers(id)\n            );\nCREATE TABLE IF NOT EXISTS depenses (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                chantier_id INTEGER NOT NULL,\n                categorie TEXT NOT NULL,\n                libelle TEXT NOT NULL,\n                montant_fcfa REAL NOT NULL,\n                date_depense TEXT NOT NULL,\n                reference_piece TEXT,\n                supprime INTEGER DEFAULT 0,\n                FOREIGN KEY (chantier_id) REFERENCES chantiers(id)\n            );\nCREATE TABLE IF NOT EXISTS avancement (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                chantier_id INTEGER NOT NULL,\n                pourcentage REAL NOT NULL,\n                description TEXT,\n                date_saisie TEXT NOT NULL,\n                supprime INTEGER DEFAULT 0,\n                FOREIGN KEY (chantier_id) REFERENCES chantiers(id)\n            );\nCREATE TABLE IF NOT EXISTS materiel (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                chantier_id INTEGER NOT NULL,\n                designation TEXT NOT NULL,\n                quantite REAL NOT NULL,\n                unite TEXT NOT NULL,\n                date_reception TEXT NOT NULL,\n                supprime INTEGER DEFAULT 0,\n                FOREIGN KEY (chantier_id) REFERENCES chantiers(id)\n            );\nCREATE TABLE IF NOT EXISTS devis (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                chantier_id INTEGER NOT NULL,\n                numero TEXT UNIQUE NOT NULL,\n                objet TEXT NOT NULL,\n                tva_pct REAL NOT NULL DEFAULT 19.25,\n                statut TEXT NOT NULL DEFAULT 'brouillon',\n                supprime INTEGER DEFAULT 0,\n                FOREIGN KEY(chantier_id) REFERENCES chantiers(id)\n            );\nCREATE TABLE IF NOT EXISTS lignes_devis (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                devis_id INTEGER NOT NULL,\n                designation TEXT NOT NULL,\n                unite TEXT NOT NULL,\n                quantite REAL NOT NULL,\n                prix_unitaire_fcfa REAL NOT NULL,\n                supprime INTEGER DEFAULT 0,\n                FOREIGN KEY(devis_id) REFERENCES devis(id)\n            );\nCREATE TABLE IF NOT EXISTS historique (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                table_nom TEXT NOT NULL,\n                row_id INTEGER NOT NULL,\n                operation TEXT NOT NULL,\n                nouvelles_valeurs TEXT,\n                utilisateur TEXT,\n                ts TEXT NOT NULL\n            );\n"
    EXTENSIONS_SQL = 'CREATE TABLE IF NOT EXISTS acces_chantiers (\n chantier_id INTEGER NOT NULL REFERENCES chantiers(id),\n utilisateur_id INTEGER NOT NULL REFERENCES utilisateurs(id),\n PRIMARY KEY(chantier_id,utilisateur_id)\n);\nCREATE TABLE IF NOT EXISTS photos (\n id INTEGER PRIMARY KEY AUTOINCREMENT,\n table_nom TEXT NOT NULL,\n row_id INTEGER NOT NULL,\n chantier_id INTEGER NOT NULL REFERENCES chantiers(id),\n phase TEXT NOT NULL,\n contenu BLOB NOT NULL,\n ts TEXT NOT NULL\n);\nCREATE INDEX IF NOT EXISTS idx_photos_chantier ON photos(chantier_id);\nCREATE INDEX IF NOT EXISTS idx_historique_row ON historique(table_nom,row_id);\n'
    STYLE = '<style>\n/* Keyed containers belong to this app; native Streamlit widgets remain intact. */\n[class*="st-key-mobile_"] { display: none; }\n[data-testid="stMainBlockContainer"] { max-width: 1280px; }\n[data-testid="stMarkdownContainer"] { overflow-wrap: anywhere; }\n[data-testid="stMetricValue"] { overflow-wrap: anywhere; white-space: normal; }\n[data-testid="stMetricValue"] > div { white-space: normal; font-size: 1.6rem; }\nbutton p { white-space: normal; overflow-wrap: anywhere; }\n@media (max-width: 768px) {\n  [class*="st-key-desktop_"] { display: none; }\n  [class*="st-key-mobile_"] { display: block; }\n  [data-testid="stMainBlockContainer"] {\n    padding-left: 1rem;\n    padding-right: 1rem;\n    padding-top: 4.2rem;\n  }\n  [data-testid="stMarkdownContainer"] h1 { font-size: 1.75rem; }\n  [data-testid="stMarkdownContainer"] h2 { font-size: 1.4rem; }\n  [data-testid="stMarkdownContainer"] h3 { font-size: 1.15rem; }\n  button { min-height: 44px; }\n  [data-testid="stTextInput"] input { font-size: 16px; }\n  [data-testid="stTextArea"] textarea { font-size: 16px; }\n  [data-testid="stExpander"] summary p { white-space: normal; overflow-wrap: anywhere; }\n}\n@media (max-width: 640px) {\n  [data-testid="stColumn"] { width: 100%; flex: 1 1 100%; min-width: 0; }\n}\n\n:root { color-scheme: light; }\n.stApp { background: #fbfcfd; color: #23333b; }\n[data-testid="stMainBlockContainer"] { padding-top: 4.2rem; padding-bottom: 3rem; max-width: 1380px; }\n[data-testid="stSidebar"] { background: #edf3f5; border-right: 1px solid #dce5e9; }\n[data-testid="stSidebar"] h3 { color: #126c77; }\nh1,h2,h3 { color: #23333b; letter-spacing: 0 !important; }\nh1 { font-size: 2.35rem !important; font-weight: 750 !important; }\nh2 { font-size: 1.55rem !important; }\nh3 { font-size: 1.2rem !important; }\n[data-testid="stCaptionContainer"] { color: #5c737c; }\n[data-testid="stForm"] { background: white; border: 1px solid #dce5e9; border-radius: 6px; padding: 1.25rem; }\n[data-testid="stMetric"] { border-top: 3px solid #1c8391; padding: 1rem 0; }\n[data-testid="stMetricValue"] { color: #116875; }\n[data-testid="stExpander"] { background: white; border-radius: 6px; }\nbutton { border-radius: 5px !important; }\n[data-testid="stFormSubmitButton"] button { background: #126c77; color: white; border-color: #126c77; }\n[data-testid="stFormSubmitButton"] button:hover { background: #0e555e; color: white; border-color: #0e555e; }\n[data-testid="stFormSubmitButton"] button p { color: inherit; }\n[data-testid="stDownloadButton"] button { color: #126c77; border-color: #9abfc5; }\ninput,textarea { color: #23333b; }\n@media (max-width:640px) {\n  h1 { font-size: 1.85rem !important; }\n  [data-testid="stForm"] { padding: .85rem; }\n  [data-testid="stMainBlockContainer"] { padding-left: 1rem; padding-right: 1rem; }\n}\n\n</style>\n'
    import datetime as dt
    import hashlib
    import hmac
    import os
    import secrets
    import sqlite3
    import base64
    import tempfile
    import time
    from pathlib import Path
    ROOT = Path(__file__).resolve().parent
    def _default_data_root():
        """Dossier des données : variable d'environnement, ancienne base si elle existe, sinon Google Drive détecté."""
        env = os.environ.get('GENIE_CIVIL_DATA')
        if env:
            return Path(env)
        legacy = Path.home() / 'GenieCivilProStreamlit'
        if (legacy / 'geniecivil_pro.db').exists():
            return legacy
        for drive in (Path('/content/drive/MyDrive'), Path.home() / 'Google Drive' / 'My Drive', Path.home() / 'My Drive',
                      Path.home() / 'Google Drive', Path('/Volumes/GoogleDrive/My Drive'), Path('G:/My Drive'), Path('/mnt/g/My Drive')):
            try:
                if drive.is_dir():
                    return drive / 'GenieCivilPro'
            except OSError:
                pass
        return legacy
    DATA_ROOT = _default_data_root()
    TABLES = {'chantiers', 'journalier', 'malfacons', 'depenses', 'avancement', 'materiel', 'devis', 'lignes_devis'}
    _CORE_TABLES = ('utilisateurs', 'chantiers', 'journalier', 'malfacons', 'depenses', 'avancement', 'materiel', 'devis', 'lignes_devis', 'historique')
    _EXT_TABLES = ('acces_chantiers', 'photos', 'analyses')
    EXTENSIONS_SQL += """CREATE TABLE IF NOT EXISTS analyses (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     chantier_id INTEGER NOT NULL REFERENCES chantiers(id),
     nom TEXT NOT NULL,
     type TEXT NOT NULL,
     config TEXT NOT NULL,
     resume TEXT NOT NULL,
     auteur TEXT,
     ts TEXT NOT NULL,
     supprime INTEGER DEFAULT 0
    );
    CREATE INDEX IF NOT EXISTS idx_analyses_chantier ON analyses(chantier_id);
    """
    try:
        from zoneinfo import ZoneInfo
        LOCAL_TZ = ZoneInfo(os.environ.get('GENIE_CIVIL_TZ', 'Africa/Douala'))
    except Exception:  # base de fuseaux absente : Cameroun = UTC+1 sans changement d'heure
        LOCAL_TZ = dt.timezone(dt.timedelta(hours=1))
    def local_now():
        return dt.datetime.now(LOCAL_TZ)
    def local_today():
        return local_now().date()
    def storage_label(path):
        """Texte court décrivant où sont les données (pour l'écran Sauvegardes)."""
        text = str(path).replace('\\', '/')
        in_drive = any(mark in text for mark in ('MyDrive', 'My Drive', 'Google Drive', 'GoogleDrive'))
        return text, in_drive
    class LocalDatabase:
        def __init__(self, path=None):
            self.path = Path(path or os.environ.get('GENIE_CIVIL_DB', DATA_ROOT / 'geniecivil_pro.db'))
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.conn = sqlite3.connect(self.path, timeout=15)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute('PRAGMA foreign_keys=ON')
            found = {r[0] for r in self.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if not set(_CORE_TABLES) <= found:
                self.conn.executescript(SCHEMA_SQL)
        def rows(self, sql, args=()):
            return [dict(row) for row in self.conn.execute(sql, args)]
        def write(self, sql, args=()):
            with self.conn:
                return self.conn.execute(sql, args).lastrowid
        def register(self, login, name, password, confirmation):
            login = login.strip().lower()
            if len(login) < 3 or not name.strip():
                raise ValueError('Identifiant de 3 caractères minimum et nom requis.')
            if len(password) < 8 or password != confirmation:
                raise ValueError('Mot de passe de 8 caractères minimum ; confirmations identiques.')
            # Restrict account creation after bootstrap to authenticated administrators.
            with self.conn:
                self.conn.execute('BEGIN IMMEDIATE')
                count = self.conn.execute('SELECT COUNT(*) FROM utilisateurs').fetchone()[0]
                if count and not getattr(self, 'admin', False):
                    raise ValueError('Seul un administrateur peut créer les comptes suivants.')
                salt = secrets.token_hex(16)
                digest = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), 600000).hex()
                self.conn.execute('INSERT INTO utilisateurs (identifiant,nom_complet,mot_de_passe_hash,role) VALUES (?,?,?,?)',
                                  (login, name.strip(), f'pbkdf2$600000${salt}${digest}', 'admin' if count == 0 else 'editeur'))
        def login(self, login, password):
            rows = self.rows('SELECT * FROM utilisateurs WHERE identifiant=? AND actif=1', (login.strip().lower(),))
            if not rows:
                raise ValueError('Identifiant ou mot de passe incorrect.')
            user = rows[0]
            stored = user['mot_de_passe_hash']
            if stored.startswith('pbkdf2$'):
                _, rounds, salt, expected = stored.split('$')
                actual = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), int(rounds)).hex()
            else:
                expected = stored
                actual = hashlib.sha256(password.encode()).hexdigest()
            if not hmac.compare_digest(actual, expected):
                raise ValueError('Identifiant ou mot de passe incorrect.')
            self.write('UPDATE utilisateurs SET derniere_connexion=? WHERE id=?', (dt.datetime.now().isoformat(), user['id']))
            return {k: user[k] for k in ('id', 'identifiant', 'nom_complet', 'role')}
        def insert(self, table, values, user):
            if table not in TABLES or user['role'] not in ('admin', 'editeur'):
                raise ValueError('Action non autorisée.')
            columns = {r['name'] for r in self.conn.execute(f'PRAGMA table_info({table})')}
            if not set(values).issubset(columns):
                raise ValueError('Champs invalides.')
            for key, val in values.items():
                if key in ('code', 'nom', 'libelle', 'designation', 'element', 'type_defaut', 'numero', 'objet', 'unite') and not str(val).strip():
                    raise ValueError('Les champs obligatoires doivent être remplis.')
                if key.startswith('date_'):
                    dt.date.fromisoformat(str(val))
                if key in ('budget_fcfa', 'montant_fcfa', 'quantite', 'prix_unitaire_fcfa') and float(val) < 0:
                    raise ValueError('Les montants et quantités doivent être positifs.')
            if table == 'chantiers' and values['date_fin_prevue'] < values['date_debut']:
                raise ValueError('La fin prévue doit être après le début.')
            if table == 'avancement' and not 0 <= values['pourcentage'] <= 100:
                raise ValueError('Avancement attendu entre 0 et 100 %.')
            with self.conn:
                cur = self.conn.execute(f'INSERT INTO {table} ({",".join(values)}) VALUES ({",".join("?" for _ in values)})', tuple(values.values()))
                return cur.lastrowid
        def backup(self):
            import tempfile
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / 'sauvegarde.db'
                dest = sqlite3.connect(path)
                try:
                    self.conn.backup(dest)
                finally:
                    dest.close()
                return path.read_bytes()
    import datetime as dt
    import io
    import json
    import os
    from contextlib import contextmanager
    from pathlib import Path
    class PgConnection:
        def __init__(self,url):
            import psycopg
            from psycopg.rows import dict_row
            self.raw = psycopg.connect(url,autocommit=True,row_factory=dict_row,connect_timeout=10)
        def execute(self,sql,args=()):
            return self.raw.execute(sql.replace('?', '%s'),args)
        def close(self): self.raw.close()
    class Database(LocalDatabase):
        def __init__(self,path=None,url=None):
            url = url or os.environ.get('DATABASE_URL')
            self.postgres = bool(url)
            self.display_name = None
            if url:
                self.conn = PgConnection(url)
            else:
                super().__init__(path)
            self.ensure_schema()
        def ensure_schema(self):
            """Crée les tables manquantes. Une seule requête de contrôle quand tout existe déjà."""
            if self.postgres:
                found = {r['table_name'] for r in self.rows('SELECT table_name FROM information_schema.tables WHERE table_schema=current_schema()')}
            else:
                found = {r['name'] for r in self.rows("SELECT name FROM sqlite_master WHERE type='table'")}
            convert = lambda text: text.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY').replace(' REAL ', ' DOUBLE PRECISION ').replace(' BLOB ', ' BYTEA ')
            if not set(_CORE_TABLES) <= found:
                if self.postgres:
                    for query in convert(SCHEMA_SQL).split(';'):
                        if query.strip(): self.conn.execute(query)
                else:
                    self.conn.executescript(SCHEMA_SQL)
            if not set(_EXT_TABLES) <= found:
                sql = convert(EXTENSIONS_SQL) if self.postgres else EXTENSIONS_SQL
                with self.transaction():
                    for query in sql.split(';'):
                        if query.strip(): self.conn.execute(query)
        @contextmanager
        def transaction(self):
            if self.postgres:
                with self.conn.raw.transaction():
                    yield
            elif self.conn.in_transaction:
                import secrets
                name='sp_'+secrets.token_hex(8)
                self.conn.execute('SAVEPOINT '+name)
                try:
                    yield
                    self.conn.execute('RELEASE SAVEPOINT '+name)
                except BaseException:
                    self.conn.execute('ROLLBACK TO SAVEPOINT '+name)
                    self.conn.execute('RELEASE SAVEPOINT '+name)
                    raise
            else:
                self.conn.execute('BEGIN IMMEDIATE')
                with self.conn:
                    yield
        def write(self,sql,args=()):
            with self.transaction(): return self.conn.execute(sql,args).rowcount
        def actor(self,user,edit=False,admin=False):
            found=self.rows('SELECT id,identifiant,role FROM utilisateurs WHERE id=? AND actif=1',(user.get('id'),))
            if not found or (edit and found[0]['role'] not in ('admin','editeur')) or (admin and found[0]['role']!='admin'):
                raise ValueError('Action non autorisée.')
            return found[0]
        def access(self,cid,user,edit=False):
            actor=self.actor(user,edit=edit)
            if not self.rows('SELECT id FROM chantiers WHERE id=? AND supprime=0',(cid,)):
                raise ValueError('Chantier indisponible.')
            if actor['role']!='admin' and not self.rows('SELECT chantier_id FROM acces_chantiers WHERE chantier_id=? AND utilisateur_id=?',(cid,actor['id'])):
                raise ValueError('Accès au chantier refusé.')
        def sites(self,user,archived=False):
            actor=self.actor(user)
            if actor['role']=='admin':
                return self.rows('SELECT * FROM chantiers WHERE supprime=? ORDER BY id DESC',(int(archived),))
            return self.rows('SELECT c.* FROM chantiers c JOIN acces_chantiers a ON a.chantier_id=c.id WHERE c.supprime=0 AND a.utilisateur_id=? ORDER BY c.id DESC',(actor['id'],))
        def audit(self,table,rid,operation,values,user):
            self.conn.execute('INSERT INTO historique(table_nom,row_id,operation,nouvelles_valeurs,utilisateur,ts) VALUES(?,?,?,?,?,?)',(table,rid,operation,json.dumps(values,ensure_ascii=False,default=str),(self.display_name or user['identifiant']),dt.datetime.now(dt.timezone.utc).isoformat()))
        def register(self,login,name,password,confirmation,user=None,role='editeur'):
            import hashlib,secrets
            if len(login.strip())<3 or not name.strip() or len(password)<8 or password!=confirmation:
                raise ValueError('Nom et identifiant requis ; mot de passe de 8 caractères et confirmation identique.')
            if role not in ('admin','editeur','lecteur'): raise ValueError('Rôle invalide.')
            with self.transaction():
                if self.postgres: self.conn.execute('LOCK TABLE utilisateurs IN EXCLUSIVE MODE')
                count=self.rows('SELECT COUNT(*) total FROM utilisateurs')[0]['total']
                if count: self.actor(user or {},admin=True)
                salt=secrets.token_hex(16)
                digest=hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(salt),600000).hex()
                self.conn.execute('INSERT INTO utilisateurs(identifiant,nom_complet,mot_de_passe_hash,role) VALUES(?,?,?,?)',(login.strip().lower(),name.strip(),f'pbkdf2$600000${salt}${digest}','admin' if not count else role))
        def scope(self,table,row):
            if table=='chantiers': return row['id']
            if table=='lignes_devis':
                quotes=self.rows('SELECT chantier_id FROM devis WHERE id=? AND supprime=0',(row['devis_id'],))
                if not quotes: raise ValueError('Devis indisponible.')
                return quotes[0]['chantier_id']
            return row['chantier_id']
        DATE_FIELD = {'journalier': 'date_jour', 'malfacons': 'date_signalement', 'depenses': 'date_depense', 'avancement': 'date_saisie', 'materiel': 'date_reception'}
        def normalize(self,table,values):
            """Nettoie les espaces ; codes de chantier et numéros de devis en majuscules."""
            clean={k:(v.strip() if isinstance(v,str) else v) for k,v in values.items()}
            if table=='chantiers' and isinstance(clean.get('code'),str): clean['code']=clean['code'].upper()
            if table=='devis' and isinstance(clean.get('numero'),str): clean['numero']=clean['numero'].upper()
            return clean
        def validate(self,table,values,rid=None,rules=True):
            import math
            if table not in TABLES: raise ValueError('Table invalide.')
            if self.postgres:
                columns={r['column_name'] for r in self.rows('SELECT column_name FROM information_schema.columns WHERE table_name=? AND table_schema=current_schema()',(table,))}
            else:
                columns={r['name'] for r in self.rows(f'PRAGMA table_info({table})')}
            if not set(values).issubset(columns-{'id','supprime'}): raise ValueError('Champs invalides.')
            for key,val in values.items():
                if key in ('code','nom','libelle','designation','element','type_defaut','numero','objet','unite') and not str(val).strip(): raise ValueError('Champs obligatoires manquants.')
                if key.startswith('date_'): dt.date.fromisoformat(str(val))
                if key in ('budget_fcfa','montant_fcfa','quantite','prix_unitaire_fcfa','effectif','pourcentage','tva_pct') and (not math.isfinite(float(val)) or float(val)<0): raise ValueError('Valeur numérique positive attendue.')
            if table=='chantiers' and values['date_fin_prevue']<values['date_debut']: raise ValueError('La fin prévue doit suivre le début.')
            if any(k in values and not 0<=values[k]<=100 for k in ('pourcentage','tva_pct')): raise ValueError('Pourcentage attendu entre 0 et 100 %.')
            enums={'statut_resolution':{'Ouvert','En cours','Résolu'},'criticite':{'Faible','Moyenne','Élevée','Critique'},'categorie':{'materiaux','main_oeuvre','materiel','sous_traitance','transport','autre'}}
            for key,allowed in enums.items():
                if key in values and values[key] not in allowed: raise ValueError('Option invalide : '+key)
            strict={'depenses':{'montant_fcfa':'Le montant doit être supérieur à 0.'},'materiel':{'quantite':'La quantité doit être supérieure à 0.'},
                    'lignes_devis':{'quantite':'La quantité doit être supérieure à 0.','prix_unitaire_fcfa':'Le prix unitaire doit être supérieur à 0.'}}
            for key,message in strict.get(table,{}).items():
                if key in values and float(values[key])<=0: raise ValueError(message)
            if rules: self.business_rules(table,values,rid)
        def business_rules(self,table,values,rid=None):
            """Règles qui dépendent des données déjà enregistrées."""
            other=-1 if rid is None else rid
            if table=='chantiers':
                if values.get('statut') not in (None,*OPTIONS['statut']): raise ValueError('Statut de chantier invalide.')
                if 'code' in values and self.rows('SELECT id FROM chantiers WHERE UPPER(code)=? AND id<>?',(str(values['code']).upper(),other)):
                    raise ValueError('Ce code de chantier existe déjà (majuscules et minuscules ne comptent pas).')
                return
            if table=='devis':
                if values.get('statut') not in (None,'brouillon','envoye','accepte','refuse'): raise ValueError('Statut de devis invalide.')
                if 'numero' in values and self.rows('SELECT id FROM devis WHERE UPPER(numero)=? AND id<>?',(str(values['numero']).upper(),other)):
                    raise ValueError('Ce numéro de devis existe déjà.')
                return
            cid=values.get('chantier_id'); key=self.DATE_FIELD.get(table)
            if cid is None or not key: return
            day=dt.date.fromisoformat(str(values[key]))
            site=self.rows('SELECT date_debut FROM chantiers WHERE id=?',(cid,))
            if site and day<dt.date.fromisoformat(site[0]['date_debut'])-dt.timedelta(days=60):
                raise ValueError(f"Date trop antérieure au début du chantier ({site[0]['date_debut']}).")
            if day>local_today()+dt.timedelta(days=1): raise ValueError('La date ne peut pas être dans le futur.')
            if table=='journalier' and self.rows('SELECT id FROM journalier WHERE chantier_id=? AND date_jour=? AND supprime=0 AND id<>?',(cid,values['date_jour'],other)):
                raise ValueError('Un rapport existe déjà pour cette date : modifiez-le (Modifier ou archiver).')
            if table=='avancement':
                pct=float(values['pourcentage']); date=values['date_saisie']
                before=self.rows('SELECT date_saisie,pourcentage FROM avancement WHERE chantier_id=? AND supprime=0 AND id<>? AND date_saisie<? AND pourcentage>? ORDER BY date_saisie DESC LIMIT 1',(cid,other,date,pct))
                if before: raise ValueError(f"L’avancement ne peut pas diminuer : {float(before[0]['pourcentage']):.1f} % déjà saisi le {before[0]['date_saisie']}.")
                after=self.rows('SELECT date_saisie,pourcentage FROM avancement WHERE chantier_id=? AND supprime=0 AND id<>? AND date_saisie>? AND pourcentage<? ORDER BY date_saisie ASC LIMIT 1',(cid,other,date,pct))
                if after: raise ValueError(f"Une saisie plus récente ({after[0]['date_saisie']}) indique {float(after[0]['pourcentage']):.1f} %, inférieur à cette valeur.")
        def insert(self,table,values,user):
            actor=self.actor(user,edit=True)
            values=self.normalize(table,values)
            self.validate(table,values)
            if table!='chantiers': self.access(self.scope(table,values),user,edit=True)
            try:
                with self.transaction():
                    sql=f'INSERT INTO {table} ({",".join(values)}) VALUES ({",".join("?" for _ in values)})'
                    cur=self.conn.execute(sql+(' RETURNING id' if self.postgres else ''),tuple(values.values()))
                    rid=cur.fetchone()['id'] if self.postgres else cur.lastrowid
                    if table=='chantiers': self.conn.execute('INSERT INTO acces_chantiers(chantier_id,utilisateur_id) VALUES(?,?)',(rid,actor['id']))
                    self.audit(table,rid,'creation',values,actor)
                    return rid
            except Exception as exc:
                if type(exc).__name__ in ('IntegrityError','UniqueViolation'): raise ValueError('Cette valeur existe déjà (code ou numéro unique).') from exc
                raise
        def update(self,table,rid,values,user):
            actor=self.actor(user,edit=True)
            if table not in TABLES: raise ValueError('Table invalide.')
            old=self.rows(f'SELECT * FROM {table} WHERE id=? AND supprime=0',(rid,))
            if not old: raise ValueError('Enregistrement indisponible.')
            self.access(self.scope(table,old[0]),user,edit=True)
            if set(values)&{'id','supprime','chantier_id','devis_id'}: raise ValueError('Références non modifiables.')
            values=self.normalize(table,values)
            merged={k:v for k,v in old[0].items() if k not in ('id','supprime')}
            merged.update(values)
            self.validate(table,merged,rid=rid)
            try:
                with self.transaction():
                    self.conn.execute(f'UPDATE {table} SET {",".join(k+"=?" for k in values)} WHERE id=?',(*values.values(),rid))
                    self.audit(table,rid,'modification',{'avant':old[0],'apres':merged},actor)
            except Exception as exc:
                if type(exc).__name__ in ('IntegrityError','UniqueViolation'): raise ValueError('Cette valeur existe déjà (code ou numéro unique).') from exc
                raise
        def archive(self,table,rid,user,restore=False):
            actor=self.actor(user,edit=True,admin=restore)
            if table not in TABLES: raise ValueError('Table invalide.')
            old=self.rows(f'SELECT * FROM {table} WHERE id=? AND supprime=?',(rid,int(restore)))
            if not old: raise ValueError('Enregistrement indisponible.')
            if not (restore and table=='chantiers'): self.access(self.scope(table,old[0]),user,edit=True)
            with self.transaction():
                self.conn.execute(f'UPDATE {table} SET supprime=? WHERE id=?',(0 if restore else 1,rid))
                self.audit(table,rid,'restauration' if restore else 'archivage',old[0],actor)
        def grant(self,cid,uid,enabled,user):
            actor=self.actor(user,admin=True)
            self.access(cid,user)
            with self.transaction():
                self.conn.execute('DELETE FROM acces_chantiers WHERE chantier_id=? AND utilisateur_id=?',(cid,uid))
                if enabled: self.conn.execute('INSERT INTO acces_chantiers(chantier_id,utilisateur_id) VALUES(?,?)',(cid,uid))
                self.audit('acces_chantiers',cid,'attribution',{'utilisateur_id':uid,'autorise':enabled},actor)
        def photo(self,table,rid,phase,data,user):
            from PIL import Image,ImageOps
            actor=self.actor(user,edit=True)
            if table not in ('malfacons','journalier') or phase not in ('Avant','Après','Journalier'): raise ValueError('Photo invalide.')
            row=self.rows(f'SELECT * FROM {table} WHERE id=? AND supprime=0',(rid,))
            if not row: raise ValueError('Enregistrement indisponible.')
            self.access(row[0]['chantier_id'],user,edit=True)
            if len(data)>5*1024*1024: raise ValueError('Photo limitée à 5 Mo.')
            with Image.open(io.BytesIO(data)) as img:
                if img.width*img.height>20000000: raise ValueError('Photo limitée à 20 mégapixels.')
                img=ImageOps.exif_transpose(img).convert('RGB')
                img.thumbnail((1600,1600))
                out=io.BytesIO()
                img.save(out,format='JPEG',quality=85)
            with self.transaction():
                self.conn.execute('INSERT INTO photos(table_nom,row_id,chantier_id,phase,contenu,ts) VALUES(?,?,?,?,?,?)',(table,rid,row[0]['chantier_id'],phase,out.getvalue(),local_now().isoformat()))
                self.audit(table,rid,'photo',{'phase':phase},actor)
        def summary(self,cid,user):
            self.access(cid,user)
            site=self.rows('SELECT * FROM chantiers WHERE id=?',(cid,))[0]
            total=self.rows('SELECT COALESCE(SUM(montant_fcfa),0) total FROM depenses WHERE chantier_id=? AND supprime=0',(cid,))[0]['total']
            progress=self.rows('SELECT pourcentage FROM avancement WHERE chantier_id=? AND supprime=0 ORDER BY date_saisie DESC,id DESC LIMIT 1',(cid,))
            consumed=total/site['budget_fcfa']*100 if site['budget_fcfa'] else None
            return site,total,progress[0]['pourcentage'] if progress else 0,consumed
        def backup(self):
            if self.postgres: raise ValueError('Utilisez les sauvegardes de votre fournisseur PostgreSQL.')
            return super().backup()
        # ------------------------------------------------------------ accès des rôles non administrateurs
        def sync_viewer_access(self,uid):
            """Donne à un compte non administrateur l'accès à tous les chantiers actifs (une requête de contrôle)."""
            missing=self.rows('SELECT COUNT(*) total FROM chantiers WHERE supprime=0 AND id NOT IN (SELECT chantier_id FROM acces_chantiers WHERE utilisateur_id=?)',(uid,))[0]['total']
            if missing:
                self.write('INSERT INTO acces_chantiers(chantier_id,utilisateur_id) SELECT id,? FROM chantiers WHERE supprime=0 AND id NOT IN (SELECT chantier_id FROM acces_chantiers WHERE utilisateur_id=?)',(uid,uid))
        def is_empty(self):
            return self.rows('SELECT COUNT(*) total FROM chantiers')[0]['total']==0
        def data_version(self):
            """Change à chaque écriture auditée : sert à invalider les PDF déjà préparés."""
            row=self.rows('SELECT COALESCE(MAX(id),0) m, COUNT(*) c FROM historique')[0]
            return (int(row['m']),int(row['c']))
        # ------------------------------------------------------------ analyses enregistrées
        def save_analysis(self,cid,name,kind,config_text,resume,user):
            actor=self.actor(user,edit=True)
            self.access(cid,user,edit=True)
            name=str(name).strip()
            if not 2<=len(name)<=80: raise ValueError('Nom de l’analyse : 2 à 80 caractères.')
            if kind not in ('Coûts','Délais','Matériaux','Poutre'): raise ValueError('Type d’analyse inconnu.')
            json.loads(config_text); json.dumps(resume)
            with self.transaction():
                sql='INSERT INTO analyses(chantier_id,nom,type,config,resume,auteur,ts) VALUES(?,?,?,?,?,?,?)'
                cur=self.conn.execute(sql+(' RETURNING id' if self.postgres else ''),(cid,name,kind,config_text,json.dumps(resume,ensure_ascii=False),self.display_name or actor['identifiant'],local_now().isoformat()))
                rid=cur.fetchone()['id'] if self.postgres else cur.lastrowid
                self.audit('analyses',rid,'creation',{'nom':name,'type':kind},actor)
                return rid
        def analyses(self,cid,user,archived=False):
            self.access(cid,user)
            return self.rows('SELECT * FROM analyses WHERE chantier_id=? AND supprime=? ORDER BY id DESC',(cid,int(archived)))
        def archive_analysis(self,aid,user,restore=False):
            actor=self.actor(user,edit=True)
            row=self.rows('SELECT * FROM analyses WHERE id=?',(aid,))
            if not row: raise ValueError('Analyse indisponible.')
            self.access(row[0]['chantier_id'],user,edit=True)
            with self.transaction():
                self.conn.execute('UPDATE analyses SET supprime=? WHERE id=?',(0 if restore else 1,aid))
                self.audit('analyses',aid,'restauration' if restore else 'archivage',{'nom':row[0]['nom']},actor)
        # ------------------------------------------------------------ instantané JSON (démonstration / transfert)
        SNAP_COLUMNS = {
            'chantiers': ('code','nom','budget_fcfa','date_debut','date_fin_prevue','client','localisation','statut'),
            'journalier': ('chantier_id','date_jour','meteo','effectif','travaux_realises','incidents'),
            'malfacons': ('chantier_id','element','type_defaut','criticite','description','action_corrective','statut_resolution','date_signalement'),
            'depenses': ('chantier_id','categorie','libelle','montant_fcfa','date_depense','reference_piece'),
            'avancement': ('chantier_id','pourcentage','description','date_saisie'),
            'materiel': ('chantier_id','designation','quantite','unite','date_reception'),
            'devis': ('chantier_id','numero','objet','tva_pct','statut'),
            'lignes_devis': ('devis_id','designation','unite','quantite','prix_unitaire_fcfa'),
        }
        def export_snapshot(self,user,include_photos=True):
            actor=self.actor(user,admin=True)
            sites=self.rows('SELECT * FROM chantiers WHERE supprime=0 ORDER BY id')
            ids={r['id'] for r in sites}
            out={'format':'geniecivil-snapshot','version':1,'exporte_le':local_now().isoformat(),'tables':{},'photos':[],'analyses':[]}
            out['tables']['chantiers']=[{'id':r['id'],**{k:r[k] for k in self.SNAP_COLUMNS['chantiers']}} for r in sites]
            devis_ids=set()
            for table in ('journalier','malfacons','depenses','avancement','materiel','devis'):
                rows=[r for r in self.rows(f'SELECT * FROM {table} WHERE supprime=0 ORDER BY id') if r['chantier_id'] in ids]
                out['tables'][table]=[{'id':r['id'],**{k:r[k] for k in self.SNAP_COLUMNS[table]}} for r in rows]
                if table=='devis': devis_ids={r['id'] for r in rows}
            out['tables']['lignes_devis']=[{'id':r['id'],**{k:r[k] for k in self.SNAP_COLUMNS['lignes_devis']}} for r in self.rows('SELECT * FROM lignes_devis WHERE supprime=0 ORDER BY id') if r['devis_id'] in devis_ids]
            for r in self.rows('SELECT * FROM analyses WHERE supprime=0 ORDER BY id'):
                if r['chantier_id'] in ids:
                    out['analyses'].append({'chantier_id':r['chantier_id'],'nom':r['nom'],'type':r['type'],'config':r['config'],'resume':r['resume'],'auteur':r['auteur'],'ts':r['ts']})
            if include_photos:
                alive={t:{r['id'] for r in out['tables'][t]} for t in ('journalier','malfacons')}
                for r in self.rows('SELECT table_nom,row_id,chantier_id,phase,ts,contenu FROM photos ORDER BY id'):
                    if r['table_nom'] in alive and r['row_id'] in alive[r['table_nom']]:
                        out['photos'].append({'table_nom':r['table_nom'],'row_id':r['row_id'],'chantier_id':r['chantier_id'],'phase':r['phase'],'ts':r['ts'],'contenu_b64':base64.b64encode(bytes(r['contenu'])).decode('ascii')})
            return out
        def import_snapshot(self,payload,user):
            """Ajoute les données d'un instantané (nouveaux identifiants). Les codes de chantier déjà présents sont ignorés."""
            actor=self.actor(user,admin=True)
            if not isinstance(payload,dict) or payload.get('format')!='geniecivil-snapshot' or payload.get('version')!=1:
                raise ValueError('Fichier non reconnu : instantané Génie Civil Pro attendu.')
            tables=payload.get('tables')
            if not isinstance(tables,dict): raise ValueError('Instantané invalide.')
            for name,rows in tables.items():
                if name not in self.SNAP_COLUMNS or not isinstance(rows,list) or len(rows)>50000: raise ValueError('Instantané invalide : '+str(name))
            report={'chantiers':0,'ignores':[],'lignes':0,'photos':0,'analyses':0}
            site_map={}; row_map={t:{} for t in self.SNAP_COLUMNS}
            def put(table,row,extra):
                values={k:row.get(k) for k in self.SNAP_COLUMNS[table] if k in row and row.get(k) is not None}
                values.update(extra)
                values=self.normalize(table,values)
                self.validate(table,values,rules=False)
                sql=f'INSERT INTO {table} ({",".join(values)}) VALUES ({",".join("?" for _ in values)})'
                cur=self.conn.execute(sql+(' RETURNING id' if self.postgres else ''),tuple(values.values()))
                rid=cur.fetchone()['id'] if self.postgres else cur.lastrowid
                self.audit(table,rid,'import',{'origine':'instantané'},actor)
                return rid,values
            try:
              with self.transaction():
                for row in tables.get('chantiers',[]):
                    code=str(row.get('code','')).strip().upper()
                    if self.rows('SELECT id FROM chantiers WHERE UPPER(code)=?',(code,)):
                        report['ignores'].append(code); continue
                    rid,_=put('chantiers',row,{})
                    self.conn.execute('INSERT INTO acces_chantiers(chantier_id,utilisateur_id) VALUES(?,?)',(rid,actor['id']))
                    site_map[row['id']]=rid; report['chantiers']+=1
                for table in ('journalier','malfacons','depenses','avancement','materiel','devis'):
                    for row in tables.get(table,[]):
                        if row.get('chantier_id') not in site_map: continue
                        if table=='devis' and self.rows('SELECT id FROM devis WHERE UPPER(numero)=?',(str(row.get('numero','')).upper(),)): continue
                        rid,_=put(table,row,{'chantier_id':site_map[row['chantier_id']]})
                        row_map[table][row['id']]=rid; report['lignes']+=1
                for row in tables.get('lignes_devis',[]):
                    if row.get('devis_id') in row_map['devis']:
                        put('lignes_devis',row,{'devis_id':row_map['devis'][row['devis_id']]}); report['lignes']+=1
                for item in payload.get('analyses',[]):
                    if item.get('chantier_id') in site_map and item.get('type') in ('Coûts','Délais','Matériaux','Poutre'):
                        json.loads(item['config']); json.loads(item['resume'])
                        self.conn.execute('INSERT INTO analyses(chantier_id,nom,type,config,resume,auteur,ts) VALUES(?,?,?,?,?,?,?)',(site_map[item['chantier_id']],str(item['nom'])[:80],item['type'],item['config'],item['resume'],str(item.get('auteur') or 'import')[:80],str(item.get('ts') or local_now().isoformat())))
                        report['analyses']+=1
                from PIL import Image
                for item in payload.get('photos',[]):
                    table=item.get('table_nom')
                    if table in ('journalier','malfacons') and item.get('row_id') in row_map[table] and item.get('chantier_id') in site_map and item.get('phase') in ('Avant','Après','Journalier'):
                        data=base64.b64decode(item['contenu_b64'],validate=True)
                        if len(data)>8*1024*1024: continue
                        with Image.open(io.BytesIO(data)) as img: img.verify()
                        self.conn.execute('INSERT INTO photos(table_nom,row_id,chantier_id,phase,contenu,ts) VALUES(?,?,?,?,?,?)',(table,row_map[table][item['row_id']],site_map[item['chantier_id']],item['phase'],data,str(item.get('ts') or local_now().isoformat())))
                        report['photos']+=1
            except (KeyError,TypeError,AttributeError) as exc:
                raise ValueError('Instantané invalide : donnée manquante ou mal formée ('+str(exc)[:60]+').') from exc
            return report
        # ------------------------------------------------------------ sauvegardes automatiques (SQLite)
        def backup_dir(self):
            return None if self.postgres else self.path.parent/'sauvegardes'
        def list_backups(self):
            folder=self.backup_dir()
            if not folder or not folder.is_dir(): return []
            return [(p.name,p.stat().st_size,dt.datetime.fromtimestamp(p.stat().st_mtime,LOCAL_TZ)) for p in sorted(folder.glob('geniecivil_*.db'),reverse=True)]
        def auto_backup(self,min_minutes=30,keep=12,force=False):
            """Copie horodatée de la base dans le dossier « sauvegardes » (jamais bloquant pour l'application)."""
            if self.postgres: return None
            try:
                if self.is_empty() and not force: return None
                folder=self.backup_dir(); folder.mkdir(parents=True,exist_ok=True)
                existing=sorted(folder.glob('geniecivil_*.db'))
                if existing and not force:
                    if time.time()-existing[-1].stat().st_mtime<min_minutes*60: return None
                    if self.path.stat().st_mtime<=existing[-1].stat().st_mtime: return None
                if self.path.stat().st_size>300*1024*1024: return None
                target=folder/f'geniecivil_{local_now():%Y%m%d_%H%M%S}.db'
                dest=sqlite3.connect(target)
                try: self.conn.backup(dest)
                finally: dest.close()
                for old in sorted(folder.glob('geniecivil_*.db'))[:-keep]: old.unlink()
                return target
            except (OSError,sqlite3.Error):
                return None
        def restore_from_bytes(self,data,user):
            """Remplace le contenu de la base SQLite par une sauvegarde .db validée (copie de sécurité faite avant)."""
            self.actor(user,admin=True)
            if self.postgres: raise ValueError('Restauration automatique disponible uniquement avec SQLite.')
            if len(data)>300*1024*1024: raise ValueError('Fichier trop volumineux (300 Mo maximum).')
            if not data.startswith(b'SQLite format 3\x00'): raise ValueError('Ce fichier n’est pas une base SQLite.')
            with tempfile.TemporaryDirectory() as folder:
                source_path=Path(folder)/'import.db'; source_path.write_bytes(data)
                source=sqlite3.connect(source_path)
                try:
                    if source.execute('PRAGMA integrity_check').fetchone()[0]!='ok': raise ValueError('Sauvegarde corrompue.')
                    names={r[0] for r in source.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                    if not set(_CORE_TABLES)<=names: raise ValueError('Structure inattendue : ce n’est pas une sauvegarde Génie Civil Pro.')
                    self.auto_backup(force=True)
                    source.backup(self.conn)
                finally:
                    source.close()
            self.ensure_schema()
    from pathlib import Path
    import streamlit as st
    LABELS = {
        'identifiant': 'Identifiant', 'nom_complet': 'Nom complet', 'role': 'Rôle',
        'actif': 'Actif', 'code': 'Code', 'nom': 'Nom', 'client': 'Client',
        'localisation': 'Localisation', 'budget_fcfa': 'Budget (FCFA)',
        'date_debut': 'Début', 'date_fin_prevue': 'Fin prévue', 'statut': 'Statut',
        'date_jour': 'Date', 'meteo': 'Météo', 'effectif': 'Effectif',
        'travaux_realises': 'Travaux réalisés', 'incidents': 'Incidents',
        'element': 'Élément', 'type_defaut': 'Défaut', 'criticite': 'Criticité',
        'description': 'Description', 'action_corrective': 'Action corrective',
        'statut_resolution': 'Résolution', 'date_signalement': 'Signalement',
        'categorie': 'Catégorie', 'libelle': 'Libellé', 'montant_fcfa': 'Montant (FCFA)',
        'date_depense': 'Date', 'reference_piece': 'Référence',
        'pourcentage': 'Avancement (%)', 'date_saisie': 'Date',
        'designation': 'Désignation', 'quantite': 'Quantité', 'unite': 'Unité',
        'date_reception': 'Réception', 'numero': 'Numéro', 'objet': 'Objet',
        'tva_pct': 'TVA (%)', 'prix_unitaire_fcfa': 'Prix unitaire (FCFA)',
    }
    def install_layout():
        st.html(STYLE)
    def records(rows, key, title):
        """Both views share data; CSS switches views without a viewport rerun."""
        if not rows:
            st.info('Aucun enregistrement pour le moment.')
            return
        visible = [{LABELS.get(k, k): v for k, v in row.items()
                    if k not in {'supprime', 'chantier_id', 'devis_id'}} for row in rows]
        with st.container(key=f'desktop_{key}'):
            st.dataframe(visible, hide_index=True, width='stretch', alt=title)
        with st.container(key=f'mobile_{key}'):
            count = max(1, (len(rows) + 9) // 10)
            page = st.selectbox('Page', range(1, count + 1), key=f'page_{key}')
            st.caption(f'{len(rows)} enregistrement(s)')
            for row in rows[(page - 1) * 10:page * 10]:
                name = next((str(row[k]) for k in ('nom', 'libelle', 'element', 'designation', 'numero', 'nom_complet', 'date_jour', 'date_saisie') if row.get(k)), str(row.get('id', 'Détail')))
                with st.expander(name):
                    for field, value in row.items():
                        if field in {'supprime', 'chantier_id', 'devis_id', 'id'}:
                            continue
                        st.caption(LABELS.get(field, field))
                        st.text('—' if value is None or value == '' else str(value), width='stretch', wrap=True)
    def metrics(items):
        for offset in range(0, len(items), 2):
            for column, (label, value) in zip(st.columns(2), items[offset:offset + 2]):
                with column:
                    st.metric(label, value)
    import datetime as dt
    import io
    from xml.sax.saxutils import escape
    import streamlit as st
    OPTIONS = {
        'statut_resolution': ['Ouvert','En cours','Résolu'],
        'criticite': ['Faible','Moyenne','Élevée','Critique'],
        'categorie': ['materiaux','main_oeuvre','materiel','sous_traitance','transport','autre'],
        'statut': ['prevu','en_cours','suspendu','termine'],
    }
    NUMBERS = {'budget_fcfa','montant_fcfa','quantite','prix_unitaire_fcfa','tva_pct','pourcentage','effectif'}
    def action(callback):
        try:
            result = callback()
            st.session_state.flash = result if isinstance(result, str) else 'Modification enregistrée.'
            st.session_state.form_nonce = st.session_state.get('form_nonce', 0) + 1
            st.rerun()
        except Exception as exc:
            if isinstance(exc,(ValueError,OSError)):
                st.error(str(exc))
            else:
                st.error('Enregistrement impossible. Vérifiez les valeurs (' + type(exc).__name__ + ').')
    def manage(db,table,rows,user):
        if not rows or user['role'] not in ('admin','editeur'):
            return
        with st.expander('Modifier ou archiver'):
            ids={row['id']:row for row in rows}
            rid=st.selectbox('Enregistrement',list(ids),key=f'edit_id_{table}',format_func=lambda key: f"{key} - "+next((str(ids[key][k]) for k in ('nom','libelle','designation','numero','element','date_jour','date_saisie') if ids[key].get(k)), 'Détail'))
            row=ids[rid]
            with st.form(f'edit_{table}_{rid}'):
                changes={}
                for key,value in row.items():
                    if key in ('id','supprime','chantier_id','devis_id'): continue
                    label=LABELS.get(key,key)
                    if key.startswith('date_'):
                        changes[key]=st.date_input(label,value=dt.date.fromisoformat(value)).isoformat()
                    elif key in NUMBERS:
                        changes[key]=st.number_input(label,min_value=0 if key=='effectif' else 0.0,value=int(value or 0) if key=='effectif' else float(value or 0),max_value=100.0 if key in ('tva_pct','pourcentage') else None)
                    elif key in OPTIONS:
                        options = ['brouillon','envoye','accepte','refuse'] if table=='devis' and key=='statut' else OPTIONS[key]
                        if value not in options: options=[value]+options
                        changes[key]=st.selectbox(label,options,index=options.index(value))
                    else:
                        changes[key]=st.text_area(label,value=str(value or ''))
                if st.form_submit_button('Enregistrer les modifications',icon=':material/save:',width='stretch'):
                    action(lambda:db.update(table,rid,changes,user))
            with st.form(f'archive_{table}'):
                confirm=st.checkbox('Confirmer l’archivage de cet enregistrement')
                if st.form_submit_button('Archiver',icon=':material/archive:',width='stretch'):
                    if confirm: action(lambda:db.archive(table,rid,user))
                    else: st.warning('Confirmez l’archivage.')
    def filter_rows(rows,key):
        if not rows: return rows
        with st.expander('Recherche et filtres'):
            query=st.text_input('Rechercher',key=f'q_{key}').strip().casefold()
            fields=list(rows[0])
            date_key=next((field for field in fields if field.startswith('date_')),None)
            if date_key:
                dates=[dt.date.fromisoformat(row[date_key]) for row in rows if row.get(date_key)]
                interval=st.date_input('Période',value=(min(dates),max(dates)),key=f'dates_{key}_{min(dates)}_{max(dates)}') if dates else ()
            else: interval=()
            category=st.selectbox('Catégorie', ['Toutes']+sorted({row['categorie'] for row in rows}),key=f'cat_{key}') if 'categorie' in fields else 'Toutes'
            amount_filter=st.checkbox('Filtrer par montant',key=f'amount_{key}') if 'montant_fcfa' in fields else False
            minimum=st.number_input('Montant minimum (FCFA)',min_value=0.0,key=f'min_{key}') if amount_filter else 0
            maximum=st.number_input('Montant maximum (FCFA)',min_value=0.0,value=max(float(row['montant_fcfa']) for row in rows),key=f"max_{key}_{int(max(float(row['montant_fcfa']) for row in rows))}") if amount_filter else float('inf')
        result=[]
        for row in rows:
            if query and query not in ' '.join(str(v) for v in row.values()).casefold(): continue
            if category!='Toutes' and row.get('categorie')!=category: continue
            if 'montant_fcfa' in row and not minimum<=row['montant_fcfa']<=maximum: continue
            if len(interval)==2 and not interval[0]<=dt.date.fromisoformat(row[date_key])<=interval[1]: continue
            result.append(row)
        return result
    def photos(db,table,rows,cid,user):
        if not rows: return
        with st.expander('Photos'):
            rid=st.selectbox('Rapport' if table=='journalier' else 'Malfaçon', [r['id'] for r in rows],key=f'photo_record_{table}')
            if user['role'] in ('admin','editeur'):
                with st.form(f'photo_{table}_{rid}'):
                    phase=st.selectbox('Étape', ['Avant','Après'] if table=='malfacons' else ['Journalier'])
                    upload=st.file_uploader('Photo JPG ou PNG',type=['jpg','jpeg','png'],max_upload_size=5)
                    if st.form_submit_button('Ajouter la photo',icon=':material/add_a_photo:',width='stretch'):
                        if upload: action(lambda:db.photo(table,rid,phase,upload.getvalue(),user))
                        else: st.warning('Choisissez une photo.')
            db.access(cid,user)
            images=db.rows('SELECT phase,contenu,ts FROM photos WHERE table_nom=? AND row_id=? AND chantier_id=? ORDER BY id DESC',(table,rid,cid))
            for image in images:
                st.image(bytes(image['contenu']),caption=f"{image['phase']} - {image['ts'][:10]}",width='stretch',alt=f"Photo {image['phase']}")
    def alerts(db,cid,user):
        site,total,progress,consumed=db.summary(cid,user)
        if consumed is not None:
            if consumed>=100: st.error(f'Budget atteint ou dépassé : {consumed:.1f} % consommé.')
            elif consumed>=80: st.warning(f'Budget presque consommé : {consumed:.1f} %.')
            if consumed-progress>=20: st.warning(f'Écart de {consumed-progress:.1f} points entre budget consommé et avancement. À examiner.')
        elif total>0: st.warning('Dépenses présentes mais budget fixé à zéro.')
        if site['date_fin_prevue']<local_today().isoformat() and site['statut']!='termine': st.warning('Échéance du chantier dépassée.')
        critical=db.rows("SELECT COUNT(*) total FROM malfacons WHERE chantier_id=? AND supprime=0 AND criticite='Critique' AND statut_resolution!='Résolu'",(cid,))[0]['total']
        if critical: st.error(f'{critical} malfaçon(s) critique(s) non résolue(s).')
        st.caption(f'Avancement physique : {progress:.1f} % | Budget consommé : '+(f'{consumed:.1f} %' if consumed is not None else 'non calculable'))
    def admin_access(db,cid,user):
        users=db.rows('SELECT id,identifiant,nom_complet,role FROM utilisateurs ORDER BY id')
        if not cid: st.info('Créez ou sélectionnez un chantier.'); return
        with st.form('grant'):
            uid=st.selectbox('Utilisateur',[u['id'] for u in users],format_func=lambda key: next(u['nom_complet']+' ('+u['role']+')' for u in users if u['id']==key))
            enabled=st.checkbox('Autoriser ce chantier',value=True)
            if st.form_submit_button('Appliquer l’accès',icon=':material/key:',width='stretch'):
                action(lambda:db.grant(cid,uid,enabled,user))
        records(db.rows('SELECT u.identifiant,u.nom_complet,u.role FROM utilisateurs u JOIN acces_chantiers a ON a.utilisateur_id=u.id WHERE a.chantier_id=?',(cid,)),'grants','Accès au chantier')
        st.caption('Les administrateurs ont accès à tous les chantiers. Les autres comptes accèdent uniquement aux chantiers attribués.')
    STYLE = STYLE.replace('</style>', '\n[data-testid="stBaseButton-primary"] { background:#126c77 !important; border-color:#126c77 !important; color:white !important; }\n[data-testid="stBaseButton-primary"]:hover { background:#0e555e !important; }\n[data-testid="stCaptionContainer"] p { color:#5c737c !important; }\n</style>')
    # This source is embedded in the delivered app.py by the packaging step.
    import hashlib
    import json
    import math
    import textwrap
    from graphlib import TopologicalSorter, CycleError
    import numpy as np
    from scipy import stats
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    ANALYSIS_KINDS = ['Coûts', 'Délais', 'Matériaux', 'Poutre']
    LAWS = ['Lognormale', 'Uniforme positive']
    ASSUMPTIONS = {
        'Coûts': 'C = somme(Qi × Pi). Quantités et prix indépendants entre eux et entre postes. Aucun effet macroéconomique commun ni corrélation modélisé. Les valeurs P80/P95 sont des quantiles prédictifs conditionnels au modèle, pas des intervalles de confiance.',
        'Délais': 'Planning acyclique, tâches non préemptives, débuts au plus tôt, ressources illimitées. Durées indépendantes. Chaque tâche commence après la fin de tous ses prédécesseurs ; les branches parallèles ne sont pas additionnées.',
        'Matériaux': 'Échantillon supposé représentatif, observations indépendantes et strictement positives. Le seuil est choisi par l’utilisateur, sans qualification réglementaire. Une loi lognormale ajustée est une hypothèse, pas un fait démontré.',
        'Poutre': 'Poutre droite rectangulaire pleine en matériau élastique homogène ; deux appuis simples, charge centrale P et charge uniforme q. Euler-Bernoulli, petites déformations. Pas de poids propre automatique, de fissuration, de flambement, de déversement ni de vérification normative. Variables indépendantes. Un dépassement simulé n’est pas une probabilité universelle de rupture.',
    }
    REFERENCES = [
        ('SymPy : poutres', 'https://docs.sympy.org/latest/modules/physics/continuum_mechanics/beam.html'),
        ('SciPy : intervalle binomial exact', 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html'),
        ('SciPy : corrélation de Spearman', 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html'),
    ]
    def finite_number(value, label, low=0, strict=False, high=None):
        if isinstance(value, bool) or not isinstance(value, (int,float)): raise ValueError(label + ' : nombre attendu.')
        try: value = float(value)
        except (TypeError, ValueError): raise ValueError(label + ' : nombre attendu.')
        if not math.isfinite(value) or (value <= low if strict else value < low) or (high is not None and value > high):
            raise ValueError(label + ' : valeur hors limites.')
        return value
    def validate_analysis(c):
        if not isinstance(c, dict) or c.get('kind') not in ANALYSIS_KINDS: raise ValueError('Analyse inconnue.')
        if c.get('law') not in LAWS: raise ValueError('Loi inconnue.')
        for key, lo, hi in [('n',1000,100000),('seed',0,2147483647)]:
            if isinstance(c.get(key), bool) or not isinstance(c.get(key), int) or not lo<=c[key]<=hi: raise ValueError(key + ' invalide.')
        k = c['kind']
        if k in ('Coûts','Délais'):
            rows=c.get('rows')
            if not isinstance(rows,list) or not 1<=len(rows)<=50: raise ValueError('Entre 1 et 50 lignes attendues.')
            finite_number(c.get('limit'),'Budget / échéance',strict=True)
            for row in rows:
                if not isinstance(row,dict): raise ValueError('Ligne invalide.')
                keys = ['quantite','prix'] if k=='Coûts' else ['duree']
                for name in keys:
                    finite_number(row.get(name),name,strict=True)
                    finite_number(row.get('cv_'+name),'CV '+name,high=.5)
            if k=='Délais': planning_order(rows)
        elif k=='Matériaux':
            vals=c.get('values')
            if not isinstance(vals,list) or not 3<=len(vals)<=20000: raise ValueError('Entre 3 et 20 000 essais attendus.')
            for v in vals: finite_number(v,'Résultat d’essai',strict=True)
            finite_number(c.get('limit'),'Seuil',strict=True)
            if not isinstance(c.get('unit'),str) or not 1<=len(c['unit'])<=30: raise ValueError('Unité attendue (30 caractères maximum).')
        else:
            for name in ('L','b','h','E','fy','ratio'):
                finite_number(c.get(name),name,strict=True)
            for name in ('P','q'): finite_number(c.get(name),name)
            for name in ('P','q','b','h','fy'): finite_number(c.get('cv_'+name),'CV '+name,high=.5)
        return c
    def planning_order(rows):
        ids=[str(r.get('id','')).strip() for r in rows]
        if any(not i or len(i)>30 for i in ids) or len(set(ids))!=len(ids): raise ValueError('Identifiants de tâches uniques requis.')
        deps={i:[x.strip() for x in str(r.get('predecesseurs','')).split(',') if x.strip()] for i,r in zip(ids,rows)}
        if any(p not in ids for values in deps.values() for p in values): raise ValueError('Prédécesseur inconnu.')
        try: order=list(TopologicalSorter(deps).static_order())
        except CycleError: raise ValueError('Cycle détecté dans le planning.')
        return order,deps
    def draw_positive(rng, mean, cv, n, law):
        z=rng.standard_normal(n)
        if cv==0 or mean==0: return np.full(n,mean,dtype=float)
        if law=='Lognormale':
            sigma=np.sqrt(np.log1p(cv*cv))
            return mean*np.exp(sigma*z-sigma*sigma/2)
        return mean*(1+np.sqrt(3)*cv*(2*stats.norm.cdf(z)-1))
    def exact_probability(mask):
        n=len(mask); count=int(np.count_nonzero(mask))
        ci=stats.binomtest(count,n).proportion_ci(confidence_level=.95,method='exact')
        return dict(p=count/n,low=float(ci.low),high=float(ci.high),count=count,n=n)@st.cache_resource
    def beam_influences():
        import sympy as sp
        from sympy.physics.continuum_mechanics.beam import Beam
        x=sp.Symbol('x',real=True)
        output=[]
        for uniform in (False,True):
            beam=Beam(1,1,1,variable=x)
            ra=beam.apply_support(0,'pin'); rb=beam.apply_support(1,'roller')
            beam.apply_load(-1,0,0,end=1) if uniform else beam.apply_load(-1,sp.Rational(1,2),-1)
            beam.solve_for_reaction_loads(ra,rb)
            output.append({name:sp.lambdify(x,expr.rewrite(sp.Piecewise),'numpy') for name,expr in [('V',beam.shear_force()),('M',beam.bending_moment()),('y',beam.deflection())]})
        return output
    def beam_nominal(c):
        length=c['L']; b=c['b']/1000; h=c['h']/1000
        inertia=b*h**3/12; section=b*h*h/6
        moment=c['P']*1000*length/4+c['q']*1000*length*length/8
        stress=moment/section/1e6
        deflection=(c['P']*1000*length**3/48+5*c['q']*1000*length**4/384)/(c['E']*1e9*inertia)*1000
        return dict(M=moment/1000,sigma=stress,delta=deflection,I=inertia,W=section)@st.cache_data(ttl=1800,max_entries=6)
    def compute_analysis(serialized):
        c=validate_analysis(json.loads(serialized)); k=c['kind']; n=c['n']; rng=np.random.default_rng(c['seed']); inputs={}
        if k=='Coûts':
            values=np.zeros(n)
            for i,r in enumerate(c['rows']):
                quantity=draw_positive(rng,float(r['quantite']),float(r['cv_quantite']),n,c['law'])
                price=draw_positive(rng,float(r['prix']),float(r['cv_prix']),n,c['law'])
                values+=quantity*price
                inputs[f'Quantité {i+1}']=quantity; inputs[f'Prix {i+1}']=price
            mask=values>c['limit']; unit='FCFA'; label='Coût total'; limit=c['limit']
        elif k=='Délais':
            order,deps=planning_order(c['rows']); rows={str(r['id']).strip():r for r in c['rows']}; ends={}
            for task in order:
                r=rows[task]; duration=draw_positive(rng,float(r['duree']),float(r['cv_duree']),n,c['law'])
                start=np.maximum.reduce([ends[p] for p in deps[task]]) if deps[task] else np.zeros(n)
                ends[task]=start+duration; inputs[task]=duration
            values=np.maximum.reduce(list(ends.values())); mask=values>c['limit']; unit='jours'; label='Durée du projet'; limit=c['limit']
        elif k=='Matériaux':
            values=np.asarray(c['values'],dtype=float); mask=values<c['limit']; unit=c['unit']; label='Résultat d’essai'; limit=c['limit']
        else:
            for name in ('P','q','b','h','fy'): inputs[name]=draw_positive(rng,float(c[name]),float(c['cv_'+name]),n,c['law'])
            moment=inputs['P']*1000*c['L']/4+inputs['q']*1000*c['L']**2/8
            section=(inputs['b']/1000)*(inputs['h']/1000)**2/6
            values=inputs['fy']-moment/section/1e6
            mask=values<0; unit='MPa'; label='Marge g = fy − σ'; limit=0
        if not np.all(np.isfinite(values)): raise ValueError('Résultats non finis : vérifiez les ordres de grandeur.')
        risk=exact_probability(mask)
        checkpoints=np.unique(np.linspace(min(20,len(values)),len(values),45,dtype=int)); cumulative=np.cumsum(mask)
        sensitivity=[]
        if np.ptp(values)>0:
            for name,arr in inputs.items():
                if np.ptp(arr)>0:
                    rho=float(stats.spearmanr(arr,values).statistic)
                    if math.isfinite(rho): sensitivity.append((name,rho))
        result=dict(values=values,mask=mask,risk=risk,unit=unit,label=label,limit=limit,sensitivity=sensitivity,inputs=inputs,
                    convergence=[(int(i),float(cumulative[i-1]/i)) for i in checkpoints],config=c)
        if k=='Matériaux':
            logs=np.log(values); sd=float(np.std(logs,ddof=0)); mu=float(np.mean(logs))
            result['fitted_p']=float(stats.norm.cdf((math.log(limit)-mu)/sd)) if sd>1e-12 else None
        return result
    def chart_style(fig,title,xlabel,ylabel,height=360):
        title_lines=textwrap.wrap(title,width=28)
        fig.update_layout(title=dict(text='<br>'.join(title_lines),font=dict(size=14)),template='plotly_white',height=height,
                          margin=dict(l=16,r=16,t=35+20*len(title_lines),b=65),font=dict(size=12,color='#23333b'),
                          paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='#f4f8fa',showlegend=False)
        fig.update_xaxes(title=xlabel,automargin=True); fig.update_yaxes(title=ylabel,automargin=True)
        return fig
    def result_charts(r):
        vals=r['values']; unit=r['unit']; xlabel=r['label']+' ('+unit+')'
        hist=go.Figure(go.Histogram(x=vals,nbinsx=45,marker_color='#177e89',name='Observations'))
        hist.add_vline(x=r['limit'],line_color='#c84c50',line_dash='dash',name='Seuil',showlegend=True)
        for quantile,color,name in [(.8,'#af7413','P80'),(.95,'#5577a4','P95')]:
            hist.add_vline(x=float(np.quantile(vals,quantile)),line_color=color,line_dash='dot',name=name,showlegend=True)
        cdf=go.Figure(go.Scatter(x=np.sort(vals)[::max(1,len(vals)//2000)],y=np.arange(1,len(vals)+1)[::max(1,len(vals)//2000)]/len(vals),line=dict(color='#177e89')))
        cdf.add_vline(x=r['limit'],line_color='#c84c50',line_dash='dash')
        conv=go.Figure(go.Scatter(x=[x for x,y in r['convergence']],y=[100*y for x,y in r['convergence']],line=dict(color='#af7413')))
        charts=[chart_style(hist,'Distribution et seuil',xlabel,'Effectif'),chart_style(cdf,'Répartition empirique',xlabel,'Fréquence cumulée'),chart_style(conv,'Fréquence cumulée selon le nombre d’observations' if r['config']['kind']=='Matériaux' else 'Convergence Monte-Carlo','Observations' if r['config']['kind']=='Matériaux' else 'Tirages','Fréquence (%)')]
        charts[0].update_layout(showlegend=True,height=420,legend=dict(orientation='h',y=-.35,yanchor='top',x=0,font=dict(size=10)),margin=dict(b=110))
        if r['sensitivity']:
            rows=sorted(r['sensitivity'],key=lambda v:abs(v[1]))
            sens=go.Figure(go.Bar(x=[v for _,v in rows],y=[key for key,_ in rows],orientation='h',marker_color='#5577a4'))
            sens.update_xaxes(range=[-1,1]); charts.append(chart_style(sens,'Sensibilité exploratoire','Corrélation de Spearman','Variable',max(330,min(1000,25*len(rows)+120))))
        return charts
    def beam_charts(c):
        length=c['L']; u=np.linspace(0,1,201); point,uniform=beam_influences()
        P=c['P']*1000; q=c['q']*1000; ei=c['E']*1e9*beam_nominal(c)['I']
        curves={name:(P*length**a*np.asarray(point[name](u))+q*length**(a+1)*np.asarray(uniform[name](u))) for name,a in [('V',0),('M',1),('y',3)]}
        # Downward loading is negative; display sagging moment positive, deflection downward.
        curves['M']=-curves['M']/1000; curves['V']=-curves['V']/1000; curves['y']=-np.abs(curves['y']/ei)*1000
        schematic=go.Figure(go.Scatter(x=[0,length],y=[0,0],mode='lines',line=dict(width=9,color='#23333b')))
        schematic.add_trace(go.Scatter(x=[0,length],y=[-.08,-.08],mode='markers',marker=dict(symbol='triangle-up',size=18,color='#23333b')))
        if P:
            schematic.add_annotation(x=length/2,y=.02,ax=length/2,ay=.7,axref='x',ayref='y',text=f'P = {c["P"]:g} kN',showarrow=True,arrowhead=2,arrowcolor='#c84c50')
        if q:
            for pos in np.linspace(.05*length,.95*length,8):
                schematic.add_annotation(x=pos,y=.03,ax=pos,ay=.35,axref='x',ayref='y',text='',showarrow=True,arrowhead=2,arrowcolor='#af7413')
            schematic.add_annotation(x=0,y=.55,text=f'q = {c["q"]:g} kN/m',showarrow=False,xanchor='left')
        schematic.update_yaxes(range=[-.25,1],visible=False)
        schematic.update_xaxes(range=[-.1*length,1.1*length])
        output=[chart_style(schematic,'Chargement et appuis simples','Position x (m)','',300)]
        section=go.Figure(go.Scatter(x=[0,c['b'],c['b'],0,0],y=[0,0,c['h'],c['h'],0],mode='lines',fill='toself',fillcolor='#dceef0',line=dict(color='#177e89',width=3)))
        section.add_trace(go.Scatter(x=[-c['b']*.2,c['b']*1.2],y=[c['h']/2]*2,mode='lines',line=dict(dash='dash',color='#5577a4')))
        section.add_trace(go.Scatter(x=[c['b']/2]*2,y=[-c['h']*.15,c['h']*1.15],mode='lines',line=dict(dash='dash',color='#5577a4')))
        section.update_yaxes(scaleanchor='x',scaleratio=1)
        output.append(chart_style(section,'Section pleine et axes centroidaux','Largeur b (mm)','Hauteur h (mm)',300))
        for key,title,unit in [('V','Effort tranchant','kN'),('M','Moment fléchissant','kN·m'),('y','Déformée élastique (réelle, non amplifiée)','mm')]:
            fig=go.Figure(go.Scatter(x=u*length,y=curves[key],mode='lines',fill='tozeroy',line=dict(color='#177e89')))
            output.append(chart_style(fig,title,'Position x (m)',unit,300))
        return output
    def analysis_pdf(r):
        import matplotlib
        matplotlib.use('Agg')
        from matplotlib.figure import Figure
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
        from xml.sax.saxutils import escape
        out=io.BytesIO(); styles=getSampleStyleSheet(); story=[]
        def p(s,style='BodyText'):
            s=str(s).replace('σ','sigma').replace('−','-')
            return Paragraph(escape(s),styles[style])
        c=r['config']; risk=r['risk']
        story.extend([p('Génie Civil Pro — Analyse probabiliste','Title'),p(c['kind'],'Heading1'),p('Provenance : '+c.get('origin','Données saisies')),p(ASSUMPTIONS[c['kind']]),Spacer(1,10)])
        story.append(p(f"Événements : {risk['count']} / {risk['n']} ; fréquence {risk['p']:.3%} ; IC binomial exact 95 % [{risk['low']:.3%} ; {risk['high']:.3%}]."))
        story.append(p('L’IC quantifie l’incertitude d’échantillonnage, pas l’erreur du modèle. Zéro événement ne signifie pas risque nul.'))
        story.append(p('Paramètres et hypothèses','Heading2'))
        for key,val in c.items():
            if key in ('rows','values'): continue
            story.append(p(f'{key} : {val}'))
        if 'rows' in c:
            for row in c['rows']: story.append(p(' | '.join(f'{key} : {value}' for key,value in row.items())))
        if 'values' in c:
            story.append(p(f"Essais : {len(c['values'])}, données complètes disponibles dans le JSON de l’étude."))
        story.append(p('Résultats et quantiles prédictifs conditionnels','Heading2'))
        story.append(p(f"Moyenne : {np.mean(r['values']):.4g} {r['unit']} ; P50/P80/P95 : {np.quantile(r['values'],[.5,.8,.95])} {r['unit']}"))
        if c['kind']=='Matériaux': story.append(p(f"Probabilité sous le seuil, modèle lognormal ajusté : {r.get('fitted_p')} (sans intervalle de confiance d’ajustement)."))
        def image_figure(fig):
            buf=io.BytesIO(); fig.savefig(buf,format='png',dpi=145,bbox_inches='tight');buf.seek(0)
            story.append(Image(buf,width=475,height=245));story.append(Spacer(1,8))
        fig=Figure(figsize=(8,4));ax=fig.subplots();ax.hist(r['values'],bins=35,color='#177e89');ax.axvline(r['limit'],color='#c84c50',linestyle='--');ax.set(xlabel=r['label']+' ('+r['unit']+')',ylabel='Effectif',title='Distribution et seuil');image_figure(fig)
        fig=Figure(figsize=(8,4));ax=fig.subplots();ax.plot(*zip(*r['convergence']),color='#af7413');ax.set(xlabel='Observations / tirages',ylabel='Fréquence cumulée',title='Convergence');image_figure(fig)
        if r['sensitivity']:
            rows=sorted(r['sensitivity'],key=lambda x:abs(x[1]),reverse=True)[:12]
            fig=Figure(figsize=(8,4));ax=fig.subplots();ax.barh([k for k,v in rows],[v for k,v in rows],color='#5577a4');ax.set(xlim=(-1,1),xlabel='Spearman',title='Sensibilité exploratoire (12 variables maximum)');image_figure(fig)
            story.append(p('Les corrélations de rang ne sont ni des causalités ni des contributions additives au risque.'))
        if c['kind']=='Poutre':
            story.append(p('Mécanique nominale : '+str(beam_nominal(c))))
            for diagram in beam_charts(c):
                if len(diagram.data[0].x)>20:
                    fig=Figure(figsize=(8,4));ax=fig.subplots();ax.plot(diagram.data[0].x,diagram.data[0].y,color='#177e89');ax.set(xlabel='Position x (m)',ylabel=diagram.layout.yaxis.title.text,title=diagram.layout.title.text.replace('<br>','\n'));image_figure(fig)
            story.append(p('g = fy − M/W en MPa ; I = bh³/12 ; W = bh²/6 ; Mmax = PL/4 + qL²/8.'))
        story.append(p('Sources','Heading2'))
        for name,url in REFERENCES: story.append(p(name+' : '+url))
        def footer(canvas,doc):
            canvas.setFont('Helvetica',8);canvas.drawString(40,24,'Génie Civil Pro — Étude conditionnelle, non réglementaire');canvas.drawRightString(555,24,str(doc.page))
        SimpleDocTemplate(out,leftMargin=40,rightMargin=40,topMargin=40,bottomMargin=40).build(story,onFirstPage=footer,onLaterPages=footer)
        return out.getvalue()
    def default_analysis(kind):
        common=dict(kind=kind,n=10000,seed=42,law=LAWS[0],origin='Exemple pédagogique fictif — à remplacer')
        if kind=='Coûts': return dict(common,limit=15000000,rows=[dict(poste='Béton',quantite=100.,prix=95000.,cv_quantite=.1,cv_prix=.15),dict(poste='Acier',quantite=4.,prix=800000.,cv_quantite=.1,cv_prix=.2)])
        if kind=='Délais': return dict(common,limit=45.,rows=[dict(id='A',tache='Fondations',predecesseurs='',duree=15.,cv_duree=.2),dict(id='B',tache='Structure',predecesseurs='A',duree=20.,cv_duree=.15),dict(id='C',tache='Approvisionnement',predecesseurs='',duree=25.,cv_duree=.25),dict(id='D',tache='Assemblage',predecesseurs='B,C',duree=8.,cv_duree=.1)])
        if kind=='Matériaux': return dict(common,limit=25.,unit='MPa',values=[24.,28.,31.,26.,29.,33.,25.,30.,32.,27.])
        return dict(common,L=4.,b=100.,h=160.,E=210.,fy=235.,P=65.,q=0.,ratio=300.,cv_P=.2,cv_q=.1,cv_b=.02,cv_h=.02,cv_fy=.1)
    def canonical(c): return json.dumps(c,sort_keys=True,ensure_ascii=False,allow_nan=False)
    def analysis_workspace(db,cid,user):
        db.access(cid,user)
        scope=f'{user["id"]}:{cid}'
        # Keep studies scoped by account and chantier, including after logout/login.
        if st.session_state.get('analysis_scope')!=scope:
            for key in list(st.session_state):
                if key.startswith('ana_'): del st.session_state[key]
            st.session_state.analysis_scope=scope
        st.caption('ÉTUDES CONDITIONNELLES · HYPOTHÈSES EXPLICITES')
        kind=st.selectbox('Analyse',ANALYSIS_KINDS,key='ana_kind')
        base=st.session_state.get('ana_loaded',{}).get(kind,default_analysis(kind))
        with st.expander('Importer une étude JSON'):
            upload=st.file_uploader('Étude complète',type=['json'],max_upload_size=2,key='ana_import')
            if st.button('Charger les paramètres',icon=':material/upload:') and upload:
                try:
                    imported=validate_analysis(json.loads(upload.getvalue()))
                    st.session_state.setdefault('ana_loaded',{})[imported['kind']]=imported
                    for key in list(st.session_state):
                        if key.startswith('ana_param_') or key.startswith('ana_editor_'): del st.session_state[key]
                    st.session_state.ana_notice='Étude importée : sélectionner '+imported['kind']+'.'
                    st.rerun()
                except (ValueError,TypeError,KeyError) as exc: st.error(str(exc))
        if 'ana_notice' in st.session_state: st.info(st.session_state.pop('ana_notice'))
        st.info(base.get('origin','Données saisies'))
        c=dict(base)
        c['origin']=st.text_input('Provenance des données',value=base.get('origin','Données saisies'),max_chars=160,key='ana_param_origin_'+kind)
        if kind!='Matériaux':
            col1,col2=st.columns(2)
            c['n']=int(col1.number_input('Nombre de tirages',min_value=1000,max_value=100000,value=base['n'],step=1000,key='ana_param_n_'+kind))
            c['seed']=int(col2.number_input('Graine aléatoire',min_value=0,max_value=2147483647,value=base['seed'],key='ana_param_seed_'+kind))
            c['law']=st.selectbox('Loi des variables positives',LAWS,index=LAWS.index(base['law']),key='ana_param_law_'+kind)
            st.caption('CV = écart-type / moyenne, saisi entre 0 et 0,50. CV nul : variable déterministe. Les lois uniformes restent positives sur cette plage.')
        else:
            st.caption('Tous les essais sont utilisés. Pas de simulation ni de graine pour cette analyse. L’ajustement paramétrique proposé est lognormal.')
        if kind in ('Coûts','Délais'):
            st.caption('Coûts en FCFA.' if kind=='Coûts' else 'Durées en jours ; prédécesseurs séparés par des virgules. Les identifiants doivent être uniques.')
            table=st.data_editor(pd.DataFrame(base['rows']),num_rows='dynamic',hide_index=True,key='ana_editor_'+kind,width='stretch')
            c['rows']=clean_editor_rows(table.to_dict('records'),kind)
            c['limit']=st.number_input('Budget cible (FCFA)' if kind=='Coûts' else 'Échéance après début (jours)',min_value=.01,value=float(base['limit']),key='ana_param_limit_'+kind)
            if kind=='Délais':
                try:
                    order,deps=planning_order(c['rows'])
                    levels={}; positions={}; counts={}
                    for task in order:
                        level=max([levels[p]+1 for p in deps[task]],default=0)
                        levels[task]=level;offset=counts.get(level,0);counts[level]=offset+1;positions[task]=(level,offset)
                    graph=go.Figure()
                    for task in order:
                        x,y=positions[task]
                        for pred in deps[task]:
                            px,py=positions[pred];graph.add_annotation(x=x,y=y,ax=px,ay=py,axref='x',ayref='y',text='',showarrow=True,arrowhead=2,arrowcolor='#8ca6af')
                    graph.add_trace(go.Scatter(x=[positions[t][0] for t in order],y=[positions[t][1] for t in order],text=order,mode='markers+text',textposition='top center',marker=dict(size=18,color='#177e89')))
                    st.plotly_chart(chart_style(graph,'Dépendances du planning','Niveau de dépendance','Branche',300),key='ana_planning_graph',width='stretch')
                except ValueError as exc: st.warning(str(exc))
        elif kind=='Matériaux':
            file=st.file_uploader('Résultats CSV ou Excel',type=['csv','xlsx'],max_upload_size=5,key='ana_material_file')
            if file:
                try:
                    frame=pd.read_csv(file) if file.name.lower().endswith('.csv') else pd.read_excel(file)
                    if len(frame)>20000: raise ValueError('Maximum 20 000 essais.')
                    column=st.selectbox('Colonne de mesure',list(frame.columns),key='ana_material_column')
                    numeric=pd.to_numeric(frame[column],errors='raise')
                    if numeric.isna().any(): raise ValueError('Valeurs manquantes : nettoyer le fichier avant calcul.')
                    c['values']=numeric.astype(float).tolist();c['origin']='Fichier importé : '+file.name
                    st.dataframe(frame.head(20),hide_index=True,width='stretch')
                except Exception as exc:
                    st.error('Import impossible : '+str(exc)); return
            else:
                text=st.text_area('Mesures (une par ligne ou séparées par ;)',value='\n'.join(map(str,base['values'])),key='ana_param_values')
                try: c['values']=[float(v.strip().replace(',','.')) for v in text.replace(';','\n').splitlines() if v.strip()]
                except ValueError: st.error('Mesures numériques attendues.'); return
            c['unit']=st.text_input('Unité des essais',value=base['unit'],max_chars=30,key='ana_param_unit')
            c['limit']=st.number_input('Seuil inférieur choisi',min_value=.001,value=float(base['limit']),key='ana_param_limit_Matériaux')
        else:
            names={'L':'Portée L (m)','b':'Largeur b (mm)','h':'Hauteur h (mm)','E':'Module E (GPa)','fy':'Résistance fy (MPa)','P':'Charge centrale P (kN)','q':'Charge répartie q (kN/m)','ratio':'Limite de flèche L /'}
            cols=st.columns(2)
            for i,(key,label) in enumerate(names.items()):
                c[key]=cols[i%2].number_input(label,min_value=0. if key in ('P','q') else .001,value=float(base[key]),key='ana_param_'+key)
            with st.expander('Incertitudes de la poutre'):
                for name in ('P','q','b','h','fy'): c['cv_'+name]=st.number_input('CV '+name,min_value=0.,max_value=.5,value=float(base['cv_'+name]),key='ana_param_cv_'+name)
            try:
                validate_analysis(c)
                nominal=beam_nominal(c)
                metrics([('Moment max.',f'{nominal["M"]:.2f} kN·m'),('Contrainte max.',f'{nominal["sigma"]:.2f} MPa'),('Flèche élastique',f'{nominal["delta"]:.2f} mm'),('Limite choisie',f'{c["L"]*1000/c["ratio"]:.2f} mm')])
                limit_mm=c['L']*1000/c['ratio']
                if nominal['sigma']<=c['fy']: st.success(f'Contrainte nominale conforme : {nominal["sigma"]:.1f} MPa ≤ fy = {c["fy"]:.1f} MPa ({100*nominal["sigma"]/c["fy"]:.0f} % de la résistance).')
                else: st.error(f'Contrainte nominale NON conforme : {nominal["sigma"]:.1f} MPa > fy = {c["fy"]:.1f} MPa.')
                if nominal['delta']<=limit_mm: st.success(f'Flèche nominale conforme : {nominal["delta"]:.2f} mm ≤ {limit_mm:.2f} mm (L/{c["ratio"]:g}).')
                else: st.error(f'Flèche nominale NON conforme : {nominal["delta"]:.2f} mm > {limit_mm:.2f} mm (L/{c["ratio"]:g}).')
                for i,fig in enumerate(beam_charts(c)): st.plotly_chart(fig,key='ana_beam_'+str(i),width='stretch')
                if nominal['sigma']>c['fy']: st.warning('Résistance nominale dépassée : la déformée élastique est une extrapolation hors domaine du matériau.')
            except (ValueError,OverflowError,ZeroDivisionError) as exc: st.error(str(exc)); return
        with st.expander('Hypothèses, équations et sources'):
            st.write(ASSUMPTIONS[kind])
            st.latex({'Coûts':r'C=\sum_i Q_iP_i', 'Délais':r'T_i=D_i+\max_{j\in Pred(i)}T_j,\quad T=\max_i T_i', 'Matériaux':r'\hat p=\frac{1}{n}\sum_i 1_{X_i<s}', 'Poutre':r'g=f_y-\frac{M}{W},\quad M=\frac{PL}{4}+\frac{qL^2}{8},\quad W=\frac{bh^2}{6},\quad I=\frac{bh^3}{12}'}[kind])
            for name,url in REFERENCES: st.markdown(f'[{name}]({url})')
            st.caption('Flèche nominale : PL³/(48EI) + 5qL⁴/(384EI). La probabilité de la poutre porte uniquement sur g < 0, pas sur la limite de flèche.')
        try: validate_analysis(c); serialized=canonical(c)
        except (ValueError,TypeError,KeyError) as exc: st.error(str(exc)); return
        fingerprint=hashlib.sha256(serialized.encode()).hexdigest()
        if st.button('Calculer l’analyse',icon=':material/calculate:',type='primary',key='ana_calculate'):
            try:
                with st.spinner('Calcul en cours…'): result=compute_analysis(serialized)
                st.session_state.ana_result=(fingerprint,result)
                st.session_state.pop('ana_pdf',None)
            except (ValueError,OverflowError,ZeroDivisionError) as exc: st.error(str(exc))
        stored=st.session_state.get('ana_result')
        if not stored: return
        if stored[0]!=fingerprint:
            st.warning('Paramètres modifiés : relancez le calcul pour actualiser les résultats et les exports.'); return
        r=stored[1]; vals=r['values']; risk=r['risk']
        st.subheader('Résultats de l’étude')
        event='Proportion observée sous le seuil' if kind=='Matériaux' else 'P(g < 0), estimation' if kind=='Poutre' else 'Probabilité de dépassement, estimation'
        metrics([(event,f'{100*risk["p"]:.2f} %'),('Moyenne',f'{np.mean(vals):,.2f} {r["unit"]}'),('P80',f'{np.quantile(vals,.8):,.2f} {r["unit"]}'),('P95',f'{np.quantile(vals,.95):,.2f} {r["unit"]}')])
        st.write(f'IC binomial exact 95 % : [{100*risk["low"]:.3f} % ; {100*risk["high"]:.3f} %] · {risk["count"]} événements / {risk["n"]} observations.')
        st.caption('L’intervalle de confiance concerne l’échantillonnage, pas la validité des hypothèses. P80/P95 sont des quantiles prédictifs conditionnels. Zéro événement observé ne signifie pas risque nul.')
        st.write(f'Médiane : {np.median(vals):,.3g} {r["unit"]} · Écart-type observé : {np.std(vals,ddof=1):,.3g} {r["unit"]}')
        if kind=='Matériaux':
            st.write('Probabilité sous le seuil selon la loi lognormale ajustée : '+(f'{r["fitted_p"]:.2%}' if r['fitted_p'] is not None else 'non identifiable : observations constantes.'))
            st.caption('Estimation paramétrique distincte de la fréquence observée ; l’incertitude de l’ajustement n’est pas quantifiée ici.')
        for i,fig in enumerate(result_charts(r)): st.plotly_chart(fig,key='ana_result_chart_'+str(i),width='stretch')
        if r['sensitivity']: st.caption('Spearman mesure une association monotone au résultat. Ce n’est ni une causalité ni une contribution additive au risque.')
        save_analysis_form(db,cid,user,kind,serialized,r)
        st.subheader('Scénarios et exports')
        if st.button('Mémoriser comme scénario B',icon=':material/bookmark:',key='ana_snapshot'):
            st.session_state.ana_comparison=r
        other=st.session_state.get('ana_comparison')
        if other and other['config']['kind']==kind and other['unit']==r['unit']:
            st.dataframe([dict(Scénario=label,Moyenne=float(np.mean(item['values'])),P95=float(np.quantile(item['values'],.95)),Fréquence=item['risk']['p'],Unité=item['unit']) for label,item in [('A · actif',r),('B · mémorisé',other)]],hide_index=True,width='stretch')
            fig=go.Figure()
            for label,item,color in [('A',r,'#177e89'),('B',other,'#af7413')]:
                data=np.sort(item['values']);stride=max(1,len(data)//1500)
                fig.add_trace(go.Scatter(x=data[::stride],y=np.arange(1,len(data)+1)[::stride]/len(data),name=label,line=dict(color=color)))
            fig=chart_style(fig,'Comparaison des répartitions',r['unit'],'Fréquence cumulée');fig.update_layout(showlegend=True)
            st.plotly_chart(fig,width='stretch')
            st.download_button('Paramètres du scénario B',canonical(other['config']).encode(),file_name='scenario-B.json',mime='application/json',icon=':material/download:')
        st.caption('Scénarios conservés dans la session de ce compte et chantier. Téléchargez le JSON pour les conserver durablement puis les réimporter.')
        st.download_button('Enregistrer l’étude JSON',serialized.encode(),file_name='etude-'+kind+'.json',mime='application/json',icon=':material/download:')
        csv=pd.DataFrame({r['label']+' ('+r['unit']+')':vals,'evenement':r['mask'].astype(int),**r['inputs']}).to_csv(index=False).encode('utf-8-sig')
        st.download_button('Résultats CSV',csv,file_name='resultats.csv',mime='text/csv',icon=':material/download:')
        if st.button('Préparer le PDF de l’analyse',icon=':material/picture_as_pdf:'):
            st.session_state.ana_pdf=(fingerprint,analysis_pdf(r))
        if st.session_state.get('ana_pdf',(None,))[0]==fingerprint:
            st.download_button('Télécharger le PDF de l’analyse',st.session_state.ana_pdf[1],file_name='analyse.pdf',mime='application/pdf',icon=':material/download:')
    def report_with_analysis(db,cid,user):
        from pypdf import PdfReader, PdfWriter
        db.access(cid,user)
        writer=PdfWriter()
        writer.append(PdfReader(io.BytesIO(report_pdf(db,cid,user))))
        stored=st.session_state.get('ana_result')
        if stored and st.session_state.get('analysis_scope')==f'{user["id"]}:{cid}':
            writer.append(PdfReader(io.BytesIO(analysis_pdf(stored[1]))))
        output=io.BytesIO();writer.write(output)
        return output.getvalue()
    STYLE = STYLE.replace('</style>', '''
    .stApp { background:#f5f7fb; }[data-testid="stSidebar"] { background:#fff; border-right:1px solid #e2e7ef; }
    [data-testid="stSidebar"] h3 { color:#2563ba; }[data-testid="stMainBlockContainer"] { max-width:1480px; }
    h1 { font-size:2rem !important; }[data-testid="stBaseButton-primary"], [data-testid="stFormSubmitButton"] button { background:#2563ba !important; border-color:#2563ba !important; }[data-testid="stBaseButton-primary"]:hover { background:#1b4c93 !important; }[class*="st-key-dash_kpi_"] { background:#fff; border:1px solid #e2e7ef; border-radius:8px; padding:18px; min-height:150px; }
    [class*="st-key-dash_kpi_"] [data-testid="stMetric"] { border:0; padding:0; }.st-key-dash_kpi_budget { background:#eaf1ff; border-top:4px solid #3679d8; }
    .st-key-dash_kpi_spent { background:#fff3e4; border-top:4px solid #d89021; }
    .st-key-dash_kpi_progress { background:#e5f5ef; border-top:4px solid #22865e; }
    .st-key-dash_kpi_quality { background:#fcecef; border-top:4px solid #c74c6a; }
    .st-key-dash_kpi_budget [data-testid="stMetricValue"] { color:#245eac; }.st-key-dash_kpi_spent [data-testid="stMetricValue"] { color:#995c09; }.st-key-dash_kpi_progress [data-testid="stMetricValue"] { color:#19704c; }.st-key-dash_kpi_quality [data-testid="stMetricValue"] { color:#ad3653; }[class*="st-key-dash_action_"] button { min-height:50px; width:100%; border:1px solid #d6dfef; background:white; font-weight:600; }
    .st-key-dash_action_cost button { color:#995c09; background:#fff3e4; border-color:#f0d29e; }
    .st-key-dash_action_quality button { color:#ad3653; background:#fcecef; border-color:#efc4ce; }.st-key-dash_action_analysis button { color:#245eac; background:#eaf1ff; border-color:#bbd1f2; }
    .st-key-dash_action_daily button { color:#19704c; background:#e5f5ef; border-color:#b9dfce; }[data-testid="stCaptionContainer"] { color:#607185; }
    @media(max-width:640px) {
     [class*="st-key-dash_kpi_"] { min-height:132px; padding:14px; }
    }
    </style>''')
    def dashboard_route(domain, section):
        st.session_state.domain = domain
        st.session_state.section = section
    def dashboard(db, cid, user):
        db.access(cid, user)
        site, spent, progress, consumed = db.summary(cid, user)
        defects = db.rows("SELECT COUNT(*) total FROM malfacons WHERE chantier_id=? AND supprime=0 AND statut_resolution!='Résolu'", (cid,))[0]['total']
        has_progress = bool(db.rows('SELECT id FROM avancement WHERE chantier_id=? AND supprime=0 LIMIT 1', (cid,)))
        budget = float(site['budget_fcfa'])
        remaining = budget - spent
        st.badge(STATUT_LABELS.get(site['statut'], site['statut']), color='green' if site['statut']=='termine' else 'blue')
        st.write(f"**{site['nom']}** · {site.get('localisation') or 'Localisation non renseignée'}")
        columns = st.columns(4)
        values = [
            ('budget', 'account_balance_wallet', 'Budget du chantier', f'{budget:,.0f}', 'FCFA · enveloppe prévue'),
            ('spent', 'payments', 'Dépenses engagées', f'{spent:,.0f}', f'{consumed:.1f} % du budget' if consumed is not None else 'Budget non défini'),
            ('progress', 'trending_up', 'Avancement physique', f'{progress:.1f} %' if has_progress else '—', 'Dernière saisie' if has_progress else 'Aucune saisie'),
            ('quality', 'verified', 'Malfaçons ouvertes', str(defects), 'Ouvertes ou en cours'),
        ]
        for column, (key, icon, label, value, detail) in zip(columns, values):
            with column:
                with st.container(key='dash_kpi_'+key):
                    st.markdown(f':material/{icon}: **{label}**')
                    st.metric(label, value, label_visibility='collapsed')
                    st.caption(detail)
        st.space('small')
        st.subheader('Actions rapides')
        actions=[('daily','Rapport du jour','edit_note','Chantiers','Rapport du jour'),
                 ('cost','Dépenses','add_card','Finances','Dépenses'),
                 ('quality','Qualité','fact_check','Qualité','Malfaçons'),
                 ('analysis','Analyses probabilistes','query_stats','Analyses probabilistes','Analyses probabilistes')]
        for column,(key,label,icon,domain,section) in zip(st.columns(4),actions):
            with column:
                with st.container(key='dash_action_'+key):
                    st.button(label,icon=f':material/{icon}:',on_click=dashboard_route,args=(domain,section),width='stretch',key='dash_go_'+key)
        st.space('small')
        left,right=st.columns(2)
        with left:
            st.subheader('Répartition des dépenses')
            totals=db.rows('SELECT categorie,SUM(montant_fcfa) total FROM depenses WHERE chantier_id=? AND supprime=0 GROUP BY categorie',(cid,))
            names={'materiaux':'Matériaux','main_oeuvre':'Main-d’œuvre','materiel':'Matériel','transport':'Transport','sous_traitance':'Sous-traitance','autre':'Autre'}
            if totals and sum(float(row['total']) for row in totals)>0:
                fig=go.Figure(go.Pie(labels=[names.get(row['categorie'],row['categorie']) for row in totals],values=[row['total'] for row in totals],hole=.68,textinfo='percent',textposition='inside',marker=dict(colors=['#3679d8','#26a47d','#e4a331','#cc6080','#6c7f94','#56adca']),hovertemplate='%{label}<br>%{value:,.0f} FCFA<extra></extra>'))
                fig.update_layout(height=320,margin=dict(l=10,r=10,t=15,b=70),paper_bgcolor='rgba(0,0,0,0)',font=dict(color='#35445c'),legend=dict(orientation='h',y=-.12,x=0))
                st.plotly_chart(fig,width='stretch',key='dash_costs')
            else:
                st.info('Aucune dépense enregistrée pour ce chantier.')
        with right:
            st.subheader('Évolution de l’avancement')
            rows=db.rows('SELECT date_saisie,pourcentage FROM avancement WHERE chantier_id=? AND supprime=0 ORDER BY date_saisie,id',(cid,))
            if rows:
                # Use the latest entry of each day, not an average of successive updates.
                daily={row['date_saisie']:float(row['pourcentage']) for row in rows}
                fig=go.Figure(go.Scatter(x=list(daily),y=list(daily.values()),mode='lines+markers',fill='tozeroy',fillcolor='rgba(38,164,125,.12)',line=dict(color='#26a47d',width=3),marker=dict(size=8),hovertemplate='%{x}<br>%{y:.1f} %<extra></extra>'))
                fig=chart_style(fig,'','Date','Avancement (%)',320)
                fig.update_yaxes(range=[0,100]);fig.update_xaxes(type='date')
                st.plotly_chart(fig,width='stretch',key='dash_progress')
            else:
                st.info('Aucun avancement saisi pour ce chantier.')
        st.subheader('Situation du chantier')
        a,b=st.columns(2)
        with a:
            if budget>0:
                st.progress(min(1.,max(0.,spent/budget)),text=f'Budget consommé : {spent/budget:.1%}')
                if remaining<0: st.error(f'Dépassement du budget : {-remaining:,.0f} FCFA')
                else: st.success(f'Budget restant : {remaining:,.0f} FCFA')
            else: st.info('Définissez un budget pour suivre sa consommation.')
        with b:
            st.progress(min(1.,max(0.,progress/100)),text=f'Avancement physique : {progress:.1f} %' if has_progress else 'Avancement non renseigné')
            if defects: st.warning(f'{defects} malfaçon(s) à traiter')
            else: st.success('Aucune malfaçon ouverte enregistrée')
        st.subheader('Dernières dépenses')
        latest=db.rows('SELECT date_depense,libelle,categorie,montant_fcfa FROM depenses WHERE chantier_id=? AND supprime=0 ORDER BY date_depense DESC,id DESC LIMIT 5',(cid,))
        records(latest,'dashboard_latest','Dernières dépenses')
        with st.expander('Alertes du chantier'):
            alerts(db,cid,user)
    STATUT_LABELS={'prevu':'Prévu','en_cours':'En cours','suspendu':'Suspendu','termine':'Terminé'}
    STYLE = STYLE.replace('</style>', '''
    .stApp { background:#eef3f5; }[data-testid="stSidebar"] { background:#173f3c; border-right:0; }[data-testid="stSidebar"] h3, [data-testid="stSidebar"] label,[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color:#edf7f4 !important; }[data-testid="stSidebar"] button[kind="secondary"] { background:#244f4b; color:#fff; border-color:#3b6963; text-align:left; }[data-testid="stSidebar"] button:hover { border-color:#50d6b0; }[data-testid="stSidebar"] [data-testid="stBadge"] { color:#e9fff6 !important; background:#285b51 !important; }
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"] { background:#147c68 !important; border-color:#50bda3 !important; }
    .app-masthead { background:#173f3c; border-bottom:6px solid #24b991; padding:26px 30px; margin:0 0 22px; color:white; position:relative; overflow:hidden; }.app-masthead h1 { color:white !important; margin:0 !important; padding:0 !important; font-size:2rem !important; line-height:1.25; }
    .app-masthead p { color:#d2e9e3; margin:10px 0 0; }
    .app-masthead .eyebrow { color:#83e6c8; font-size:12px; font-weight:700; margin:0 0 8px; letter-spacing:0; }
    .masthead-colors { display:flex; height:7px; margin-top:22px; width:180px; max-width:100%; }
    .masthead-colors span { flex:1; background:#42c9a1; }
    .masthead-colors span:nth-child(2) { background:#4285de; }
    .masthead-colors span:nth-child(3) { background:#f2b847; }
    .masthead-colors span:nth-child(4) { background:#e56687; }[class*="st-key-dash_kpi_"] { border:0; border-radius:6px; box-shadow:none; }.st-key-dash_kpi_budget { background:#2564b4; }
    .st-key-dash_kpi_spent { background:#a95b17; }.st-key-dash_kpi_progress { background:#14745c; }.st-key-dash_kpi_quality { background:#ab3d62; }[class*="st-key-dash_kpi_"] [data-testid="stMetricValue"],[class*="st-key-dash_kpi_"] [data-testid="stMetricLabel"],[class*="st-key-dash_kpi_"] [data-testid="stCaptionContainer"],[class*="st-key-dash_kpi_"] p { color:white !important; }
    [class*="st-key-dash_kpi_"] [data-testid="stCaptionContainer"] { opacity:1 !important; }
    [data-testid="stForm"] { background:#f7fbfa; border:1px solid #cadbd7; border-top:4px solid #159a78; border-radius:6px; }[data-testid="stBaseButton-primary"], [data-testid="stFormSubmitButton"] button { background:#14745c !important; border-color:#14745c !important; color:white !important; }[data-testid="stBaseButton-primary"]:hover { background:#0f5947 !important; }[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input, textarea { background:#fff; }
    .st-key-dash_action_daily button { background:#14745c; color:white; border-color:#14745c; }
    .st-key-dash_action_cost button { background:#a95b17; color:white; border-color:#a95b17; }
    .st-key-dash_action_quality button { background:#ab3d62; color:white; border-color:#ab3d62; }.st-key-dash_action_analysis button { background:#2564b4; color:white; border-color:#2564b4; }
    .empty-workspace { border-left:5px solid #159a78; padding:18px 22px; background:#dceee8; margin:16px 0; }.empty-workspace h3 { color:#173f3c; margin:0 0 6px; font-size:1.25rem; }.empty-workspace p { color:#31564d; margin:0; }
    @media(max-width:640px) {
     .app-masthead { padding:22px 18px; }
     .app-masthead h1 { font-size:1.7rem !important; }
     .app-masthead p { font-size:14px; }
    }
    </style>''')
    # STREAMLIT APPLICATION
    # ======================================================================================# LABORATOIRE DE PROBABILITÉS : calculs et courbes (matplotlib, aucune dépendance en plus)
    # ======================================================================================
    from matplotlib.figure import Figure
    from matplotlib.ticker import FuncFormatter
    C_MAIN = '#177e89'
    C_ALT = '#af7413'
    C_OK = '#26a47d'
    C_BAD = '#c0392b'
    C_GREY = '#8ca6af'
    def new_fig(width=7.4, height=3.7, cols=1):
        fig = Figure(figsize=(width, height), dpi=110)
        axes = fig.subplots(1, cols) if cols > 1 else fig.subplots()
        return fig, axes
    def style_axes(ax, title='', xlabel='', ylabel=''):
        ax.set_title(title, fontsize=10.5, loc='left', color='#23333b', fontweight='bold')
        ax.set_xlabel(xlabel, fontsize=9)
        ax.set_ylabel(ylabel, fontsize=9)
        ax.grid(True, color='#dfe8ec', linewidth=.7)
        ax.set_axisbelow(True)
        for side in ('top', 'right'):
            ax.spines[side].set_visible(False)
        ax.tick_params(labelsize=8)
        ax.set_facecolor('#f8fbfc')
    def fig_png(fig):
        fig.tight_layout()
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
        return buf.getvalue()
    def money_axis(ax, axis='y'):
        """Graduations en millions (12 M) au lieu de la notation scientifique."""
        fmt = FuncFormatter(lambda v, _: f'{v / 1e6:g} M')
        (ax.yaxis if axis == 'y' else ax.xaxis).set_major_formatter(fmt)
    def short_number(v, unit=''):
        """Nombre lisible : 12 345 678 -> 12.3 M ; pour les axes et les légendes."""
        a = abs(v)
        if a >= 1e9: text = f'{v / 1e9:.2f} G'
        elif a >= 1e6: text = f'{v / 1e6:.2f} M'
        elif a >= 1e4: text = f'{v / 1e3:.1f} k'
        elif a >= 100: text = f'{v:,.0f}'
        else: text = f'{v:.3g}'
        return (text + ' ' + unit).strip()
    # ---------------------------------------------------------------- échantillon et lois ajustées
    def describe_sample(x):
        x = np.asarray(x, float)
        n = x.size
        sd = float(np.std(x, ddof=1)) if n > 1 else 0.0
        mean = float(x.mean())
        return dict(n=n, mean=mean, median=float(np.median(x)), sd=sd, cv=(sd / mean if mean else float('nan')),
                    skew=float(stats.skew(x, bias=False)) if n > 2 and sd > 0 else float('nan'),
                    kurt=float(stats.kurtosis(x, bias=False)) if n > 3 and sd > 0 else float('nan'),
                    p5=float(np.quantile(x, .05)), p95=float(np.quantile(x, .95)), min=float(x.min()), max=float(x.max()))
    def fit_positive(x):
        """Ajuste Lognormale, Gamma, Weibull et Normale. Retourne (lois, tableau classé par AIC)."""
        x = np.asarray(x, float)
        if x.size < 5 or np.any(x <= 0) or np.ptp(x) == 0:
            raise ValueError('Au moins 5 valeurs strictement positives, non toutes identiques.')
        fits = {}
        for name, build in (('Lognormale', lambda: stats.lognorm(*(lambda p: (p[0], 0, p[2]))(stats.lognorm.fit(x, floc=0)))),
                            ('Gamma', lambda: stats.gamma(*(lambda p: (p[0], 0, p[2]))(stats.gamma.fit(x, floc=0)))),
                            ('Weibull', lambda: stats.weibull_min(*(lambda p: (p[0], 0, p[2]))(stats.weibull_min.fit(x, floc=0)))),
                            ('Normale', lambda: stats.norm(*stats.norm.fit(x)))):
            try:
                fits[name] = build()
            except Exception:
                continue
        table = []
        for name, d in list(fits.items()):
            ll = float(np.sum(d.logpdf(x)))
            if not np.isfinite(ll):
                del fits[name]
                continue
            ks = stats.kstest(x, d.cdf)
            table.append(dict(loi=name, aic=4 - 2 * ll, ks_stat=float(ks.statistic), ks_p=float(ks.pvalue)))
        if not table:
            raise ValueError('Aucune loi ne peut être ajustée à ces valeurs.')
        table.sort(key=lambda r: r['aic'])
        return fits, table
    def fig_fit_hist(x, fits, best, unit, title):
        fig, ax = new_fig()
        x = np.asarray(x, float)
        ax.hist(x, bins=min(25, max(5, int(np.sqrt(x.size)) + 1)), density=True, color='#bfdde1', edgecolor='white', label='Données')
        grid = np.linspace(max(x.min() * .7, 1e-12) if x.min() > 0 else x.min() - np.ptp(x) * .1, x.max() * 1.15, 400)
        palette = {'Lognormale': C_MAIN, 'Gamma': C_ALT, 'Weibull': C_OK, 'Normale': C_GREY}
        for name, d in fits.items():
            ax.plot(grid, d.pdf(grid), color=palette.get(name, C_GREY), lw=2.6 if name == best else 1.2, ls='-' if name == best else '--', label=name + (' (meilleure)' if name == best else ''))
        style_axes(ax, title, unit, 'Densité de probabilité')
        if unit == 'FCFA':
            money_axis(ax, 'x')
            ax.set_yticks([])
            ax.set_ylabel('Densité (échelle relative)', fontsize=9)
        ax.legend(fontsize=8, frameon=False)
        return fig
    def fig_fit_cdf_qq(x, fits, best, unit):
        fig, (a1, a2) = new_fig(7.4, 3.5, cols=2)
        x = np.sort(np.asarray(x, float))
        n = x.size
        ecdf = np.arange(1, n + 1) / n
        a1.step(x, ecdf, where='post', color='#23333b', lw=1.6, label='Empirique')
        grid = np.linspace(x.min(), x.max(), 300)
        a1.plot(grid, fits[best].cdf(grid), color=C_MAIN, lw=2.4, label=best)
        style_axes(a1, 'Fonction de répartition', unit, 'P(X ≤ x)')
        if unit == 'FCFA': money_axis(a1, 'x')
        a1.legend(fontsize=8, frameon=False)
        q = (np.arange(1, n + 1) - .5) / n
        theo = fits[best].ppf(q)
        a2.scatter(theo, x, s=14, color=C_MAIN, alpha=.8)
        lim = [min(theo.min(), x.min()), max(theo.max(), x.max())]
        a2.plot(lim, lim, color=C_BAD, lw=1.4)
        style_axes(a2, f'Diagramme Q-Q ({best})', 'Quantiles théoriques', 'Quantiles observés')
        if unit == 'FCFA':
            money_axis(a2, 'x'); money_axis(a2, 'y')
        return fig
    # ---------------------------------------------------------------- comptages : Poisson, Gamma-Poisson, Beta-Binomiale
    def period_counts(dates, start, end, days=7):
        n = max(1, (end - start).days // days + 1)
        counts = np.zeros(n, int)
        for d in dates:
            k = (d - start).days // days
            if 0 <= k < n:
                counts[int(k)] += 1
        return counts
    def poisson_summary(counts):
        counts = np.asarray(counts, int)
        n = counts.size
        mean = float(counts.mean())
        var = float(counts.var(ddof=1)) if n > 1 else float('nan')
        if mean > 0 and n > 1:
            disp = var / mean
            p_over = float(stats.chi2.sf((n - 1) * var / mean, n - 1))
        else:
            disp = p_over = float('nan')
        return dict(n=n, total=int(counts.sum()), mean=mean, var=var, dispersion=disp, p_overdispersion=p_over)
    def fig_poisson(counts, summary, unit_label='semaine'):
        fig, ax = new_fig()
        counts = np.asarray(counts, int)
        kmax = int(max(counts.max(), stats.poisson.ppf(.999, max(summary['mean'], .1)))) + 1
        ks = np.arange(0, kmax + 1)
        observed = np.array([(counts == k).mean() for k in ks])
        ax.bar(ks - .18, observed, width=.36, color='#bfdde1', label='Observé')
        ax.bar(ks + .18, stats.poisson.pmf(ks, summary['mean']), width=.36, color=C_MAIN, label=f'Poisson (λ = {summary["mean"]:.2f})')
        style_axes(ax, f'Événements par {unit_label} : observé et loi de Poisson', f'Nombre par {unit_label}', 'Probabilité')
        ax.set_xticks(ks)
        ax.legend(fontsize=8, frameon=False)
        return fig
    def gamma_poisson_posterior(counts, a0=.5, b0=0.0):
        counts = np.asarray(counts, int)
        a = a0 + counts.sum()
        b = b0 + counts.size
        post = stats.gamma(a, scale=1 / b)
        return post, dict(mean=float(a / b), low=float(post.ppf(.025)), high=float(post.ppf(.975)))
    def fig_rate_posterior(post, info, target):
        fig, ax = new_fig()
        lo, hi = post.ppf(.0005), post.ppf(.9995)
        grid = np.linspace(lo, hi, 400)
        ax.plot(grid, post.pdf(grid), color=C_MAIN, lw=2.4)
        inside = (grid >= info['low']) & (grid <= info['high'])
        ax.fill_between(grid[inside], post.pdf(grid[inside]), color=C_MAIN, alpha=.18, label=f'Intervalle de crédibilité 95 % : [{info["low"]:.2f} ; {info["high"]:.2f}]')
        ax.axvline(target, color=C_BAD, ls='--', lw=1.4, label=f'Seuil λ = {target:.2f} : P(λ > seuil) = {post.sf(target):.1%}')
        style_axes(ax, 'Loi a posteriori du taux d’événements λ (Gamma-Poisson)', 'λ (événements par période)', 'Densité')
        ax.legend(fontsize=8, frameon=False)
        return fig
    def beta_posterior(successes, total, a0=1.0, b0=1.0):
        post = stats.beta(a0 + successes, b0 + total - successes)
        return post, dict(mean=float(post.mean()), low=float(post.ppf(.025)), high=float(post.ppf(.975)))
    def fig_beta(post, prior, info, threshold, label):
        fig, ax = new_fig()
        grid = np.linspace(0, 1, 500)
        ax.plot(grid, prior.pdf(grid), color=C_GREY, ls='--', lw=1.4, label='A priori Bêta(1 ; 1)')
        ax.plot(grid, post.pdf(grid), color=C_MAIN, lw=2.4, label='A posteriori')
        inside = (grid >= info['low']) & (grid <= info['high'])
        ax.fill_between(grid[inside], post.pdf(grid[inside]), color=C_MAIN, alpha=.18, label=f'Crédibilité 95 % : [{info["low"]:.2f} ; {info["high"]:.2f}]')
        ax.axvline(threshold, color=C_BAD, ls='--', lw=1.4, label=f'P(p > {threshold:.0%}) = {post.sf(threshold):.1%}')
        style_axes(ax, f'Probabilité inconnue : {label}', 'p', 'Densité')
        ax.legend(fontsize=8, frameon=False)
        return fig
    # ---------------------------------------------------------------- prévision du délai (régression de l'avancement)
    def daily_progress(rows):
        last = {}
        for r in sorted(rows, key=lambda r: (r['date_saisie'], r.get('id', 0))):
            last[dt.date.fromisoformat(r['date_saisie'])] = float(r['pourcentage'])
        return sorted(last.items())
    def forecast_progress(points, deadline, n=20000, seed=42):
        if len(points) < 3:
            raise ValueError('Au moins 3 dates d’avancement sont nécessaires pour une prévision.')
        x = np.array([(d - points[0][0]).days for d, _ in points], float)
        y = np.array([p for _, p in points], float)
        if np.ptp(x) == 0:
            raise ValueError('Dates d’avancement identiques : régression impossible.')
        lr = stats.linregress(x, y)
        df = len(x) - 2
        last_d, last_y = points[-1]
        rng = np.random.default_rng(seed)
        slopes = lr.slope + (lr.stderr if np.isfinite(lr.stderr) else 0.0) * rng.standard_t(df, n)
        remaining = max(0.0, 100.0 - last_y)
        safe = np.where(slopes > 0, slopes, 1.0)
        days = np.where(slopes > 0, remaining / safe, np.inf)
        allowed = (deadline - last_d).days
        p_deadline = 1.0 if remaining == 0 else float(np.mean(days <= allowed)) if allowed >= 0 else 0.0
        def date_at(q):
            v = float(np.quantile(days, q))
            return last_d + dt.timedelta(days=int(np.ceil(v))) if np.isfinite(v) and v < 3650 else None
        return dict(points=points, x=x, y=y, slope=float(lr.slope), intercept=float(lr.intercept), stderr=float(lr.stderr), r2=float(lr.rvalue ** 2),
                    p_deadline=p_deadline, days=days, slopes=slopes, last_d=last_d, last_y=last_y, deadline=deadline,
                    dates={50: date_at(.5), 80: date_at(.8), 95: date_at(.95)}, df=df, p_finish=float(np.mean(np.isfinite(days))))
    def fig_progress_forecast(res):
        fig, ax = new_fig()
        pts = res['points']
        ax.plot([d for d, _ in pts], [p for _, p in pts], 'o-', color=C_MAIN, lw=2, label='Avancement saisi')
        last_d, last_y = res['last_d'], res['last_y']
        for q, color, ls, label in ((.5, C_ALT, '-', 'Tendance centrale'), (.9, C_OK, '--', 'Scénario rapide (pente haute, P90)'), (.1, C_BAD, '--', 'Scénario lent (pente basse, P10)')):
            slope = float(np.quantile(res['slopes'], q))
            if slope <= 0:
                continue
            days = min((100 - last_y) / slope, 1500)
            ax.plot([last_d, last_d + dt.timedelta(days=days)], [last_y, last_y + slope * days], color=color, ls=ls, lw=1.6, label=label)
        ax.axhline(100, color='#23333b', lw=.8)
        ax.axvline(res['deadline'], color=C_BAD, lw=1.4)
        ax.annotate(f"Échéance\nP(terminer à temps) = {res['p_deadline']:.0%}", (res['deadline'], 8), fontsize=8, color=C_BAD, ha='right')
        ax.set_ylim(0, 108)
        style_axes(ax, 'Avancement : tendance linéaire et scénarios', 'Date', 'Avancement (%)')
        ax.tick_params(axis='x', labelrotation=25)
        ax.legend(fontsize=8, frameon=False, loc='upper left')
        return fig
    def fig_completion_cdf(res):
        fig, ax = new_fig()
        days = np.minimum(res['days'], 3650)
        ordered = np.sort(days)
        cdf = np.arange(1, ordered.size + 1) / ordered.size
        stride = max(1, ordered.size // 1500)
        ax.plot(ordered[::stride], cdf[::stride], color=C_MAIN, lw=2.4)
        allowed = (res['deadline'] - res['last_d']).days
        ax.axvline(allowed, color=C_BAD, lw=1.4, label=f"Échéance : P = {res['p_deadline']:.1%}")
        for q, color in ((50, C_OK), (80, C_ALT), (95, C_GREY)):
            d = res['dates'][q]
            if d is not None:
                ax.axvline((d - res['last_d']).days, color=color, ls=':', lw=1.4, label=f'P{q} : {d.isoformat()}')
        finite = ordered[ordered < 3650]
        ax.set_xlim(0, max(allowed * 1.3, float(np.quantile(finite, .97)) if finite.size else 30, 10))
        style_axes(ax, 'Date de fin : probabilité de terminer au plus tard', f"Jours après la dernière saisie ({res['last_d'].isoformat()})", 'Probabilité cumulée')
        ax.legend(fontsize=8, frameon=False, loc='lower right')
        return fig
    # ---------------------------------------------------------------- prévision du coût final
    def cost_pairs(progress_rows, expense_rows):
        expenses = sorted((dt.date.fromisoformat(r['date_depense']), float(r['montant_fcfa'])) for r in expense_rows)
        pairs = []
        for d, p in daily_progress(progress_rows):
            pairs.append((d, p, sum(a for ed, a in expenses if ed <= d)))
        return pairs
    def forecast_cost(pairs, budget):
        if len(pairs) < 3:
            raise ValueError('Au moins 3 dates d’avancement sont nécessaires pour une prévision de coût.')
        x = np.array([p for _, p, _ in pairs], float)
        y = np.array([c for *_, c in pairs], float)
        if np.ptp(x) == 0:
            raise ValueError('Avancements identiques : régression impossible.')
        n = x.size
        xbar = x.mean()
        sxx = float(np.sum((x - xbar) ** 2))
        b = float(np.sum((x - xbar) * (y - y.mean())) / sxx)
        a = float(y.mean() - b * xbar)
        df = n - 2
        s = float(np.sqrt(np.sum((y - (a + b * x)) ** 2) / df))
        def predict(x0):
            fit = a + b * np.asarray(x0, float)
            se = s * np.sqrt(1 + 1 / n + (np.asarray(x0, float) - xbar) ** 2 / sxx)
            return fit, se
        fit100, se100 = predict(100.0)
        p_over = float(stats.t.sf((budget - fit100) / se100, df)) if se100 > 0 else float(fit100 > budget)
        rho = stats.spearmanr(x, y).statistic if n >= 3 else float('nan')
        t80, t95 = stats.t.ppf(.9, df), stats.t.ppf(.975, df)
        return dict(x=x, y=y, a=a, b=b, s=s, df=df, fit100=float(fit100), se100=float(se100), p_over=p_over, rho=float(rho),
                    low80=float(fit100 - t80 * se100), high80=float(fit100 + t80 * se100), low95=float(fit100 - t95 * se100), high95=float(fit100 + t95 * se100),
                    budget=float(budget), predict=predict, t80=float(t80), t95=float(t95))
    def fig_cost_forecast(res):
        fig, ax = new_fig()
        grid = np.linspace(0, 100, 200)
        fit, se = res['predict'](grid)
        ax.fill_between(grid, fit - res['t95'] * se, fit + res['t95'] * se, color=C_MAIN, alpha=.10, label='Intervalle de prédiction 95 %')
        ax.fill_between(grid, fit - res['t80'] * se, fit + res['t80'] * se, color=C_MAIN, alpha=.18, label='Intervalle de prédiction 80 %')
        ax.plot(grid, fit, color=C_MAIN, lw=2.2, label='Régression')
        ax.scatter(res['x'], res['y'], color='#23333b', zorder=3, s=26, label='Dépenses cumulées observées')
        ax.axhline(res['budget'], color=C_BAD, lw=1.5, label=f"Budget : {short_number(res['budget'])} FCFA")
        ax.scatter([100], [res['fit100']], color=C_ALT, zorder=4, s=40, label=f"Coût final prévu : {short_number(res['fit100'])} FCFA")
        ax.set_xlim(0, 104)
        style_axes(ax, f"Coût final à 100 % : P(dépasser le budget) = {res['p_over']:.1%}", 'Avancement (%)', 'Dépenses cumulées (FCFA)')
        money_axis(ax, 'y')
        ax.legend(fontsize=7.5, frameon=False, loc='upper left')
        return fig
    # ---------------------------------------------------------------- matériaux : intervalles, test, valeur caractéristique
    def material_inference(values, required, conf=.95):
        x = np.asarray(values, float)
        n = x.size
        if n < 3:
            raise ValueError('Au moins 3 essais sont nécessaires.')
        mean, sd = float(x.mean()), float(x.std(ddof=1))
        if sd <= 0:
            raise ValueError('Essais tous identiques : écart-type nul, inférence impossible.')
        se = sd / np.sqrt(n)
        tcrit = float(stats.t.ppf(1 - (1 - conf) / 2, n - 1))
        chi_hi, chi_lo = stats.chi2.ppf(1 - (1 - conf) / 2, n - 1), stats.chi2.ppf((1 - conf) / 2, n - 1)
        t_stat = (mean - required) / se
        k = float(stats.nct.ppf(.95, df=n - 1, nc=stats.norm.ppf(.95) * np.sqrt(n)) / np.sqrt(n))
        rng = np.random.default_rng(42)
        reps = int(min(5000, max(300, 2_000_000 // n)))
        boot = rng.choice(x, size=(reps, n)).mean(axis=1)
        return dict(n=n, mean=mean, sd=sd, se=float(se), tcrit=tcrit, ci_mean=(mean - tcrit * se, mean + tcrit * se),
                    ci_sd=(float(sd * np.sqrt((n - 1) / chi_hi)), float(sd * np.sqrt((n - 1) / chi_lo))),
                    t_stat=float(t_stat), p_greater=float(stats.t.sf(t_stat, n - 1)), k=k, fk=mean - k * sd, fk_simple=mean - 1.645 * sd,
                    p_below=float(stats.norm.cdf((required - mean) / sd)), boot=boot, ci_boot=(float(np.quantile(boot, .025)), float(np.quantile(boot, .975))),
                    required=float(required), values=x)
    def fig_material_hist(res, unit):
        fig, ax = new_fig()
        x = res['values']
        ax.hist(x, bins=min(20, max(4, int(np.sqrt(x.size)) + 1)), density=True, color='#bfdde1', edgecolor='white', label='Essais')
        grid = np.linspace(res['mean'] - 4 * res['sd'], res['mean'] + 4 * res['sd'], 400)
        ax.plot(grid, stats.norm.pdf(grid, res['mean'], res['sd']), color=C_MAIN, lw=2.4, label='Loi normale ajustée')
        below = grid <= res['required']
        ax.fill_between(grid[below], stats.norm.pdf(grid[below], res['mean'], res['sd']), color=C_BAD, alpha=.25, label=f"Sous le seuil : {res['p_below']:.2%}")
        ax.axvline(res['required'], color=C_BAD, lw=1.4)
        ax.axvline(res['fk'], color=C_ALT, ls='--', lw=1.6, label=f"Valeur caractéristique (fractile 5 %) : {res['fk']:.2f} {unit}")
        style_axes(ax, 'Distribution des essais et seuil requis', unit, 'Densité')
        ax.legend(fontsize=8, frameon=False)
        return fig
    def fig_t_test(res):
        fig, ax = new_fig()
        df = res['n'] - 1
        lim = max(4.5, abs(res['t_stat']) * 1.15)
        grid = np.linspace(-lim, lim, 500)
        ax.plot(grid, stats.t.pdf(grid, df), color=C_MAIN, lw=2.4)
        crit = stats.t.ppf(.95, df)
        ax.fill_between(grid[grid >= crit], stats.t.pdf(grid[grid >= crit], df), color=C_OK, alpha=.25, label=f'Zone de rejet de H0 (5 %) : t ≥ {crit:.2f}')
        ax.axvline(res['t_stat'], color=C_BAD, lw=1.8, label=f"t observé = {res['t_stat']:.2f} ; p = {res['p_greater']:.3f}")
        style_axes(ax, f'Test unilatéral H1 : moyenne supérieure au seuil (Student, {df} ddl)', 't', 'Densité')
        ax.legend(fontsize=8, frameon=False)
        return fig
    def fig_bootstrap(res, unit):
        fig, ax = new_fig()
        ax.hist(res['boot'], bins=40, density=True, color='#bfdde1', edgecolor='white', label='Moyennes rééchantillonnées (bootstrap)')
        for ci, color, label in ((res['ci_boot'], C_ALT, 'IC 95 % bootstrap'), (res['ci_mean'], C_MAIN, 'IC 95 % de Student')):
            ax.axvline(ci[0], color=color, ls='--', lw=1.6, label=f'{label} : [{ci[0]:.2f} ; {ci[1]:.2f}]')
            ax.axvline(ci[1], color=color, ls='--', lw=1.6)
        style_axes(ax, 'Incertitude sur la moyenne', unit, 'Densité')
        ax.legend(fontsize=7.5, frameon=False)
        return fig
    # ---------------------------------------------------------------- calculateur de lois
    LAB_LAWS = {
        'Normale': dict(usage='Résistances, erreurs de mesure, somme de nombreux petits aléas.', discrete=False,
                        params=[('mu', 'Moyenne μ', 0.0, None, None), ('sigma', 'Écart-type σ', 1.0, 1e-6, None)]),
        'Lognormale': dict(usage='Coûts, prix, charges : valeurs positives et asymétriques.', discrete=False,
                           params=[('mu', 'μ du logarithme', 0.0, None, None), ('sigma', 'σ du logarithme', .5, 1e-6, None)]),
        'Exponentielle': dict(usage='Temps entre deux pannes ou deux incidents (sans mémoire).', discrete=False,
                              params=[('lam', 'Taux λ (1 / unité)', 1.0, 1e-6, None)]),
        'Weibull': dict(usage='Durée de vie, fatigue, résistance de matériaux fragiles.', discrete=False,
                        params=[('k', 'Forme k', 2.0, 1e-3, None), ('lam', 'Échelle λ', 1.0, 1e-6, None)]),
        'Gamma': dict(usage='Cumul de durées ou de coûts, somme d’exponentielles.', discrete=False,
                      params=[('k', 'Forme k', 2.0, 1e-3, None), ('theta', 'Échelle θ', 1.0, 1e-6, None)]),
        'Bêta': dict(usage='Proportions et probabilités inconnues (entre 0 et 1), avancement.', discrete=False,
                     params=[('a', 'Forme α', 2.0, 1e-3, None), ('b', 'Forme β', 5.0, 1e-3, None)]),
        'Uniforme': dict(usage='Aucune information sauf les bornes.', discrete=False,
                         params=[('a', 'Minimum a', 0.0, None, None), ('b', 'Maximum b', 1.0, None, None)]),
        'Triangulaire': dict(usage='Estimation à trois valeurs : optimiste, probable, pessimiste.', discrete=False,
                             params=[('a', 'Minimum a', 0.0, None, None), ('c', 'Valeur probable c', 1.0, None, None), ('b', 'Maximum b', 3.0, None, None)]),
        'Binomiale': dict(usage='Nombre de non-conformités sur n contrôles indépendants.', discrete=True,
                          params=[('n', 'Nombre d’essais n', 20, 1, 1000), ('p', 'Probabilité p', .1, 0.0, 1.0)]),
        'Poisson': dict(usage='Nombre d’incidents ou de défauts par période.', discrete=True,
                        params=[('lam', 'Moyenne λ', 3.0, 1e-6, None)]),
    }
    def build_law(name, p):
        if name == 'Normale': return stats.norm(p['mu'], p['sigma'])
        if name == 'Lognormale': return stats.lognorm(p['sigma'], scale=float(np.exp(p['mu'])))
        if name == 'Exponentielle': return stats.expon(scale=1 / p['lam'])
        if name == 'Weibull': return stats.weibull_min(p['k'], scale=p['lam'])
        if name == 'Gamma': return stats.gamma(p['k'], scale=p['theta'])
        if name == 'Bêta': return stats.beta(p['a'], p['b'])
        if name == 'Uniforme':
            if not p['b'] > p['a']: raise ValueError('Il faut b > a.')
            return stats.uniform(p['a'], p['b'] - p['a'])
        if name == 'Triangulaire':
            if not (p['a'] < p['b'] and p['a'] <= p['c'] <= p['b']): raise ValueError('Il faut a < b et a ≤ c ≤ b.')
            return stats.triang((p['c'] - p['a']) / (p['b'] - p['a']), loc=p['a'], scale=p['b'] - p['a'])
        if name == 'Binomiale': return stats.binom(int(p['n']), p['p'])
        if name == 'Poisson': return stats.poisson(p['lam'])
        raise ValueError('Loi inconnue.')
    def describe_law(d):
        mean, var, skew, kurt = (float(v) for v in d.stats(moments='mvsk'))
        return dict(mean=mean, var=var, sd=float(np.sqrt(var)), skew=skew, kurt=kurt,
                    quantiles={q: float(d.ppf(q)) for q in (.05, .5, .8, .95, .99)})
    def fig_law(d, discrete, a, b, name):
        fig, (ax, bx) = new_fig(7.6, 3.5, cols=2)
        lo, hi = float(d.ppf(.0005)), float(d.ppf(.9995))
        if discrete:
            lo, hi = int(max(0, np.floor(lo))), int(np.ceil(hi))
            ks = np.arange(lo, hi + 1)
            inside = (ks >= a) & (ks <= b)
            ax.bar(ks[~inside], d.pmf(ks[~inside]), color='#bfdde1', width=.8)
            ax.bar(ks[inside], d.pmf(ks[inside]), color=C_MAIN, width=.8)
            style_axes(ax, f'{name} : loi de probabilité', 'x', 'P(X = x)')
            bx.step(ks, d.cdf(ks), where='post', color=C_MAIN, lw=2.2)
            prob = float(d.cdf(np.floor(b)) - d.cdf(np.ceil(a) - 1))
        else:
            grid = np.linspace(lo, hi, 500)
            ax.plot(grid, d.pdf(grid), color=C_MAIN, lw=2.4)
            inside = (grid >= a) & (grid <= b)
            ax.fill_between(grid[inside], d.pdf(grid[inside]), color=C_MAIN, alpha=.3)
            style_axes(ax, f'{name} : densité', 'x', 'f(x)')
            bx.plot(grid, d.cdf(grid), color=C_MAIN, lw=2.4)
            prob = float(d.cdf(b) - d.cdf(a))
        ax.set_title(ax.get_title() + f'   P({a:g} ≤ X ≤ {b:g}) = {prob:.3f}', fontsize=8.5, loc='left')
        for v in (a, b):
            bx.axvline(v, color=C_ALT, ls='--', lw=1.1)
        style_axes(bx, 'Fonction de répartition', 'x', 'P(X ≤ x)')
        return fig, prob
    # ---------------------------------------------------------------- loi des grands nombres, théorème central limite
    def sim_lgn(d, n=2000, runs=6, seed=1):
        rng = np.random.default_rng(seed)
        sample = np.atleast_2d(d.rvs(size=(runs, n), random_state=rng))
        return np.cumsum(sample, axis=1) / np.arange(1, n + 1)
    def fig_lgn(running, true_mean):
        fig, ax = new_fig()
        n = running.shape[1]
        for row in running:
            ax.plot(np.arange(1, n + 1), row, lw=1.1, alpha=.85)
        ax.axhline(true_mean, color='#23333b', ls='--', lw=1.6, label=f'Espérance théorique = {true_mean:.3g}')
        ax.set_xscale('log')
        style_axes(ax, 'Loi des grands nombres : la moyenne converge vers l’espérance', 'Nombre d’observations n (échelle log)', 'Moyenne empirique')
        ax.legend(fontsize=8, frameon=False)
        return fig
    def sim_tcl(d, k, reps=4000, seed=2):
        rng = np.random.default_rng(seed)
        means = np.atleast_2d(d.rvs(size=(reps, k), random_state=rng)).mean(axis=1)
        mu, sd = float(d.mean()), float(d.std())
        return means, mu, sd / np.sqrt(k)
    def tcl_skew_curve(d, ks=(1, 2, 5, 10, 30, 100), reps=3000, seed=3):
        rng = np.random.default_rng(seed)
        out = []
        for k in ks:
            means = np.atleast_2d(d.rvs(size=(reps, k), random_state=rng)).mean(axis=1)
            out.append(float(stats.skew(means)) if np.std(means) > 0 else 0.0)
        return list(ks), out
    def fig_tcl(means, mu, se, k, name, ks, skews):
        fig, (ax, bx) = new_fig(7.6, 3.5, cols=2)
        ax.hist(means, bins=40, density=True, color='#bfdde1', edgecolor='white', label=f'Moyennes de {k} tirages')
        grid = np.linspace(means.min(), means.max(), 400)
        ax.plot(grid, stats.norm.pdf(grid, mu, se), color=C_MAIN, lw=2.4, label=f'Normale(μ, σ/√{k})')
        style_axes(ax, f'{name} : distribution des moyennes', 'Moyenne', 'Densité')
        ax.legend(fontsize=7.5, frameon=False)
        bx.plot(ks, skews, 'o-', color=C_ALT, lw=2)
        bx.axhline(0, color='#23333b', lw=.8)
        bx.set_xscale('log')
        style_axes(bx, 'Asymétrie des moyennes selon n', 'n (échelle log)', 'Asymétrie')
        return fig
    # ---------------------------------------------------------------- fiabilité et fragilité de la poutre
    def fragility_curve(c, factors, n=6000):
        out = []
        for f in factors:
            c2 = dict(c, P=float(c['P']) * f, q=float(c['q']) * f, n=n)
            r = compute_analysis(canonical(c2))
            k, v = r['risk'], r['values']
            sd = float(np.std(v, ddof=1))
            beta = float(np.mean(v) / sd) if sd > 0 else float('inf')
            out.append(dict(f=float(f), p=k['p'], low=k['low'], high=k['high'], beta=beta,
                            pf_cornell=float(stats.norm.cdf(-beta)) if np.isfinite(beta) else 0.0))
        return out
    def fig_fragility(curve):
        fig, ax = new_fig()
        f = np.array([r['f'] for r in curve])
        floor = 1e-5
        p = np.maximum([r['p'] for r in curve], floor)
        ax.fill_between(f, np.maximum([r['low'] for r in curve], floor), np.maximum([r['high'] for r in curve], floor), color=C_MAIN, alpha=.18, label='IC 95 % (Monte-Carlo)')
        ax.plot(f, p, 'o-', color=C_MAIN, lw=2.2, ms=4, label='Monte-Carlo')
        ax.plot(f, np.maximum([r['pf_cornell'] for r in curve], floor), '--', color=C_ALT, lw=1.8, label='Indice de Cornell : Φ(−β)')
        for pf, label in ((1e-3, '10⁻³'), (1e-4, '10⁻⁴')):
            ax.axhline(pf, color=C_GREY, lw=.9, ls=':')
            ax.text(f[0], pf * 1.15, 'repère ' + label, fontsize=7, color=C_GREY)
        ax.set_yscale('log')
        ax.set_ylim(floor * .8, 1.2)
        style_axes(ax, 'Courbe de fragilité : probabilité de ruine selon la charge', 'Facteur multiplicatif des charges (P et q)', 'P(g < 0)  (échelle log)')
        ax.legend(fontsize=8, frameon=False, loc='lower right')
        return fig
    def fig_margin(values, risk):
        fig, ax = new_fig()
        v = np.asarray(values, float)
        mu, sd = float(v.mean()), float(v.std(ddof=1))
        ax.hist(v, bins=60, density=True, color='#bfdde1', edgecolor='white', label='Marge g simulée')
        grid = np.linspace(v.min(), v.max(), 400)
        ax.plot(grid, stats.norm.pdf(grid, mu, sd), color=C_MAIN, lw=2.2, label='Normale équivalente')
        neg = grid <= 0
        ax.fill_between(grid[neg], stats.norm.pdf(grid[neg], mu, sd), color=C_BAD, alpha=.3, label=f"Ruine g < 0 : {risk['p']:.3%} (MC)")
        ax.axvline(0, color=C_BAD, lw=1.4)
        beta = mu / sd if sd > 0 else float('inf')
        style_axes(ax, f'Marge de sécurité g = fy − σ   (indice de fiabilité β = {beta:.2f})', 'g (MPa)', 'Densité')
        ax.legend(fontsize=8, frameon=False)
        return fig
    # ======================================================================================# ACCÈS, DONNÉES DE DÉMONSTRATION, SAUVEGARDES, RAPPORTS, ANALYSES ENREGISTRÉES, LABORATOIRE
    # ======================================================================================
    ROLE_LABELS = {'admin': 'Administrateur', 'editeur': 'Testeur (saisie)', 'lecteur': 'Lecture seule'}
    WORKSPACE_IDENTITIES = {'admin': ('__geniecivil_local_workspace__', 'Espace local'),
                            'editeur': ('__geniecivil_testeur__', 'Espace testeur'),
                            'lecteur': ('__geniecivil_lecture__', 'Espace lecture seule')}
    DEMO_FILE = Path(os.environ.get('GENIE_CIVIL_DEMO', ROOT / 'demo_data.json'))
    MONEY_FIELDS = {'montant_fcfa', 'budget_fcfa', 'prix_unitaire_fcfa', 'total_ht'}
    REPORT_LABELS_OVERRIDE = {'date_signalement': 'Date', 'statut_resolution': 'Statut', 'type_defaut': 'Défaut', 'action_corrective': 'Action'}
    def _secret(name):
        """Lit un secret Streamlit, sinon une variable d'environnement. Jamais d'erreur si absent."""
        value = None
        try:
            value = st.secrets.get(name, None)
        except Exception:
            value = None
        if value in (None, ''):
            value = os.environ.get(name)
        return str(value) if value not in (None, '') else None
    def access_gate():
        """Mots de passe optionnels : ADMIN_PASSWORD, EDITOR_PASSWORD, VIEWER_PASSWORD (secrets Streamlit).
        Aucun mot de passe configuré = accès direct (usage local)."""
        passwords = {role: _secret(key) for role, key in (('admin', 'ADMIN_PASSWORD'), ('editeur', 'EDITOR_PASSWORD'), ('lecteur', 'VIEWER_PASSWORD'))}
        configured = {role: pwd for role, pwd in passwords.items() if pwd}
        if not configured:
            return {'role': 'admin', 'name': 'Espace local', 'open': True}
        auth = st.session_state.get('auth')
        if isinstance(auth, dict) and auth.get('role') in configured:
            return {'role': auth['role'], 'name': auth.get('name', ''), 'open': False}
        st.subheader('Accès protégé')
        st.caption('Saisissez votre nom et le mot de passe qui vous a été communiqué.')
        with st.form('login'):
            name = st.text_input('Votre nom', max_chars=60, help='Affiché dans le journal des modifications.')
            password = st.text_input('Mot de passe', type='password')
            submitted = st.form_submit_button('Entrer', icon=':material/login:', type='primary', width='stretch')
        if submitted:
            clean = ' '.join(name.split())
            match = next((role for role in ('admin', 'editeur', 'lecteur') if role in configured and hmac.compare_digest(password.encode(), configured[role].encode())), None)
            if len(clean) < 2:
                st.error('Indiquez votre nom (2 caractères minimum).')
            elif match is None:
                st.session_state.login_fails = st.session_state.get('login_fails', 0) + 1
                time.sleep(min(st.session_state.login_fails, 5))
                st.error('Mot de passe incorrect.')
            else:
                st.session_state.auth = {'role': match, 'name': clean[:60]}
                st.session_state.login_fails = 0
                st.rerun()
        st.stop()
    def logout():
        for key in list(st.session_state):
            if key in ('auth', 'user', 'report', 'excel', 'bk_db', 'snap') or key.startswith('ana_') or key.startswith('analysis'):
                del st.session_state[key]
    def workspace_user(database, role='admin'):
        """Compte technique du rôle choisi (créé au besoin). Les droits réels sont appliqués par la base."""
        identity, label = WORKSPACE_IDENTITIES[role]
        query = 'SELECT id,identifiant,nom_complet,role,actif FROM utilisateurs WHERE identifiant=?'
        rows = database.rows(query, (identity,))
        if not rows:
            with database.transaction():
                if database.postgres:
                    database.conn.execute('LOCK TABLE utilisateurs IN EXCLUSIVE MODE')
                rows = database.rows(query, (identity,))
                if not rows:
                    # Vérificateur aléatoire : ce n'est pas un mot de passe partagé et il n'est jamais affiché.
                    verifier = hashlib.sha256(secrets.token_bytes(64)).hexdigest()
                    database.conn.execute('INSERT INTO utilisateurs(identifiant,nom_complet,mot_de_passe_hash,role) VALUES(?,?,?,?)', (identity, label, verifier, role))
                    rows = database.rows(query, (identity,))
        user = rows[0]
        if not user['actif'] or user['role'] != role:
            raise ValueError('L’identité technique est inactive ou incompatible. Vérifiez la base de données utilisée.')
        return {key: user[key] for key in ('id', 'identifiant', 'nom_complet', 'role')}
    def local_workspace_user(database):
        return workspace_user(database, 'admin')
    # ---------------------------------------------------------------- données de démonstration
    def demo_available():
        try:
            return DEMO_FILE.is_file()
        except OSError:
            return False
    def snapshot_message(report):
        text = f"{report['chantiers']} chantier(s) importé(s), {report['lignes']} enregistrement(s), {report['photos']} photo(s), {report['analyses']} analyse(s)."
        if report['ignores']:
            text += ' Codes déjà présents (ignorés) : ' + ', '.join(report['ignores']) + '.'
        return text
    def load_demo(database):
        payload = json.loads(DEMO_FILE.read_text(encoding='utf-8'))
        return snapshot_message(database.import_snapshot(payload, workspace_user(database, 'admin')))
    def maybe_seed_demo(database):
        """Base vide + fichier demo_data.json à côté de app.py : chargement automatique (AUTO_DEMO=0 pour l'empêcher)."""
        try:
            if str(_secret('AUTO_DEMO') or '').strip().lower() in ('0', 'false', 'non', 'no'):
                return
            if demo_available() and database.is_empty():
                load_demo(database)
        except Exception as exc:  # ne jamais bloquer l'application pour des données de démonstration
            st.session_state['seed_error'] = 'Données de démonstration non chargées : ' + str(exc)[:160]
    # ---------------------------------------------------------------- formulaires et actions
    def form_key(name):
        """Clé de formulaire qui change après un enregistrement réussi : les champs sont alors vidés."""
        return f"{name}_{st.session_state.get('form_nonce', 0)}"
    def clean_editor_rows(rows, kind):
        """Cellules vides d'un tableau éditable (None, NaN) : texte vide pour les colonnes texte."""
        cleaned = []
        for row in rows:
            item = dict(row)
            for key in ('id', 'tache', 'predecesseurs', 'poste'):
                if key in item:
                    value = item[key]
                    empty = value is None or (isinstance(value, float) and value != value) or str(value).strip().lower() in ('none', 'nan')
                    item[key] = '' if empty else str(value).strip()
            cleaned.append(item)
        return cleaned
    # ---------------------------------------------------------------- historique (requêtes groupées)
    def history(db, cid, user):
        if not cid:
            st.info('Sélectionnez un chantier.')
            return
        db.access(cid, user)
        rows = db.rows('SELECT * FROM historique ORDER BY id DESC LIMIT 5000')
        wanted = {}
        for row in rows:
            if row['table_nom'] in ('depenses', 'avancement', 'journalier', 'malfacons', 'materiel', 'devis', 'lignes_devis', 'analyses'):
                wanted.setdefault(row['table_nom'], set()).add(row['row_id'])
        owner = {}
        for table, ids in wanted.items():
            ids = sorted(ids)
            for start in range(0, len(ids), 500):
                chunk = ids[start:start + 500]
                marks = ','.join('?' for _ in chunk)
                if table == 'lignes_devis':
                    found = db.rows(f'SELECT l.id AS rid, d.chantier_id AS cid FROM lignes_devis l JOIN devis d ON d.id=l.devis_id WHERE l.id IN ({marks})', tuple(chunk))
                else:
                    found = db.rows(f'SELECT id AS rid, chantier_id AS cid FROM {table} WHERE id IN ({marks})', tuple(chunk))
                for item in found:
                    owner[(table, item['rid'])] = item['cid']
        visible = []
        for row in rows:
            table = row['table_nom']
            if table in ('acces_chantiers', 'chantiers'):
                related = row['row_id'] == cid
            else:
                related = owner.get((table, row['row_id'])) == cid
            if related:
                visible.append(row)
        records(visible, 'history', 'Historique des modifications')
    # ---------------------------------------------------------------- rapport PDF (tableaux, police Unicode, prévisions)
    def _pdf_fonts():
        """DejaVu Sans (fournie avec matplotlib) pour afficher tous les caractères ; Helvetica en secours."""
        try:
            import matplotlib
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            folder = Path(matplotlib.get_data_path()) / 'fonts' / 'ttf'
            regular, bold = folder / 'DejaVuSans.ttf', folder / 'DejaVuSans-Bold.ttf'
            if not regular.exists():
                return 'Helvetica', 'Helvetica-Bold'
            if 'GCP-Regular' not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont('GCP-Regular', str(regular)))
                pdfmetrics.registerFont(TTFont('GCP-Bold', str(bold if bold.exists() else regular)))
            return 'GCP-Regular', 'GCP-Bold'
        except Exception:
            return 'Helvetica', 'Helvetica-Bold'
    REPORT_SECTIONS = [
        ('depenses', 'Dépenses', ['date_depense', 'categorie', 'libelle', 'montant_fcfa', 'reference_piece'], [.12, .15, .36, .17, .20]),
        ('avancement', 'Avancement', ['date_saisie', 'pourcentage', 'description'], [.15, .15, .70]),
        ('journalier', 'Rapports journaliers', ['date_jour', 'meteo', 'effectif', 'travaux_realises', 'incidents'], [.12, .12, .08, .38, .30]),
        ('malfacons', 'Malfaçons', ['date_signalement', 'element', 'type_defaut', 'criticite', 'statut_resolution', 'description', 'action_corrective'], [.10, .12, .13, .09, .09, .23, .24]),
        ('materiel', 'Matériel', ['designation', 'quantite', 'unite', 'date_reception'], [.46, .14, .14, .26]),
        ('devis', 'Devis', ['numero', 'objet', 'statut', 'tva_pct'], [.18, .50, .16, .16]),
    ]
    def report_pdf(db, cid, user):
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
        regular, bold = _pdf_fonts()
        teal = colors.HexColor('#126c77')
        s_title = ParagraphStyle('t', fontName=bold, fontSize=18, leading=22, textColor=teal, spaceAfter=4)
        s_h1 = ParagraphStyle('h1', fontName=bold, fontSize=12.5, leading=16, textColor=teal, spaceBefore=12, spaceAfter=5)
        s_body = ParagraphStyle('b', fontName=regular, fontSize=9, leading=12.5)
        s_cell = ParagraphStyle('c', fontName=regular, fontSize=7.6, leading=9.8)
        s_head = ParagraphStyle('hd', fontName=bold, fontSize=7.6, leading=9.8, textColor=colors.white)
        width = A4[0] - 80
        def text(value, style=s_body):
            return Paragraph(escape(str(value)).replace('\n', '<br/>'), style)
        def money(value):
            return f'{float(value):,.0f}'.replace(',', ' ')
        def cell(value, field=None):
            if value is None or value == '':
                return '-'
            if field in MONEY_FIELDS:
                return money(value)
            if isinstance(value, float):
                return f'{value:g}'
            return value
        def grid(rows, fields, shares, labels=None):
            data = [[Paragraph(escape((labels or LABELS).get(f, f)), s_head) for f in fields]]
            for row in rows:
                data.append([Paragraph(escape(str(cell(row.get(f), f))).replace('\n', '<br/>'), s_cell) for f in fields])
            table = Table(data, colWidths=[width * share for share in shares], repeatRows=1)
            table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), teal), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                       ('GRID', (0, 0), (-1, -1), .4, colors.HexColor('#c9d6db')),
                                       ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#eef4f6')]),
                                       ('LEFTPADDING', (0, 0), (-1, -1), 3), ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                                       ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
            return table
        story = []
        site, total, progress, consumed = db.summary(cid, user)
        story += [text('Génie Civil Pro – Rapport de chantier', s_title), text(site['nom'], s_h1),
                  text(f"Code : {site['code']} | Client : {site['client'] or '-'} | Localisation : {site['localisation'] or '-'}"),
                  text(f"Période : {site['date_debut']} au {site['date_fin_prevue']} | Édité le {local_today().isoformat()}"), Spacer(1, 8)]
        kpis = [['Budget', 'Dépenses', 'Avancement', 'Budget consommé'],
                [f"{money(site['budget_fcfa'])} FCFA", f'{money(total)} FCFA', f'{progress:.1f} %', f'{consumed:.1f} %' if consumed is not None else 'Non calculable']]
        kt = Table([[Paragraph(escape(v), s_head if i == 0 else s_body) for v in row] for i, row in enumerate(kpis)], colWidths=[width / 4] * 4)
        kt.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), teal), ('GRID', (0, 0), (-1, -1), .4, colors.HexColor('#c9d6db')), ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
        story.append(kt)
        for table, title, fields, shares in REPORT_SECTIONS:
            story.append(text(title, s_h1))
            rows = db.rows(f'SELECT * FROM {table} WHERE chantier_id=? AND supprime=0 ORDER BY id', (cid,))
            if not rows:
                story.append(text('Aucun enregistrement.'))
                continue
            story.append(grid(rows, fields, shares, {**LABELS, **REPORT_LABELS_OVERRIDE}))
            if table == 'devis':
                for quote in rows:
                    lines = db.rows('SELECT * FROM lignes_devis WHERE devis_id=? AND supprime=0 ORDER BY id', (quote['id'],))
                    if not lines:
                        continue
                    for line in lines:
                        line['total_ht'] = line['quantite'] * line['prix_unitaire_fcfa']
                    ht = sum(line['total_ht'] for line in lines)
                    story.append(Spacer(1, 4))
                    story.append(text(f"Lignes du devis {quote['numero']}", s_body))
                    story.append(grid(lines, ['designation', 'unite', 'quantite', 'prix_unitaire_fcfa', 'total_ht'], [.40, .10, .12, .19, .19], {**LABELS, 'total_ht': 'Total HT (FCFA)'}))
                    story.append(text(f"Total HT : {money(ht)} FCFA | Total TTC : {money(ht * (1 + quote['tva_pct'] / 100))} FCFA"))
        saved = db.analyses(cid, user)
        story.append(text('Analyses probabilistes enregistrées', s_h1))
        if saved:
            table_rows = []
            for item in saved:
                resume = json.loads(item['resume'])
                table_rows.append({'nom': item['nom'], 'type': item['type'], 'p': f"{100 * resume['p']:.2f} %", 'moy': f"{resume['mean']:,.2f} {resume['unit']}".replace(',', ' '),
                                   'p95': f"{resume['p95']:,.2f} {resume['unit']}".replace(',', ' '), 'date': str(item['ts'])[:10]})
            story.append(grid(table_rows, ['nom', 'type', 'p', 'moy', 'p95', 'date'], [.25, .11, .11, .20, .20, .13],
                              {'nom': 'Nom', 'type': 'Type', 'p': 'Probabilité', 'moy': 'Moyenne', 'p95': 'P95', 'date': 'Date'}))
        else:
            story.append(text('Aucune analyse enregistrée.'))
        story.append(text('Prévisions probabilistes à partir des données du chantier', s_h1))
        forecasts = 0
        try:
            progress_rows = db.rows('SELECT id,date_saisie,pourcentage FROM avancement WHERE chantier_id=? AND supprime=0', (cid,))
            res = forecast_progress(daily_progress(progress_rows), dt.date.fromisoformat(site['date_fin_prevue']))
            end = res['dates'][50].isoformat() if res['dates'][50] else 'non atteinte'
            story.append(text(f"Délai : fin médiane prévue le {end} ; probabilité de terminer avant le {site['date_fin_prevue']} : {res['p_deadline']:.0%} (hypothèse : vitesse d’avancement constante)."))
            story.append(Image(io.BytesIO(fig_png(fig_progress_forecast(res))), width=width * .92, height=width * .92 * .5))
            forecasts += 1
        except ValueError as exc:
            story.append(text('Prévision du délai : ' + str(exc)))
        try:
            expense_rows = db.rows('SELECT date_depense,montant_fcfa FROM depenses WHERE chantier_id=? AND supprime=0', (cid,))
            if site['budget_fcfa'] > 0:
                cres = forecast_cost(cost_pairs(progress_rows, expense_rows), float(site['budget_fcfa']))
                story.append(text(f"Coût final prévu à 100 % : {money(cres['fit100'])} FCFA (intervalle 80 % : {money(cres['low80'])} à {money(cres['high80'])}) ; probabilité de dépasser le budget : {cres['p_over']:.1%} (hypothèse : dépenses cumulées linéaires selon l’avancement)."))
                story.append(Image(io.BytesIO(fig_png(fig_cost_forecast(cres))), width=width * .92, height=width * .92 * .5))
                forecasts += 1
        except ValueError as exc:
            story.append(text('Prévision du coût : ' + str(exc)))
        for table in ('malfacons', 'journalier'):
            for photo in db.rows(f'SELECT p.phase,p.contenu,p.row_id FROM photos p JOIN {table} m ON p.row_id=m.id WHERE p.chantier_id=? AND p.table_nom=? AND m.supprime=0 ORDER BY p.id', (cid, table)):
                img = Image(io.BytesIO(bytes(photo['contenu'])))
                scale = min(450 / img.imageWidth, 260 / img.imageHeight)
                img.drawWidth = img.imageWidth * scale
                img.drawHeight = img.imageHeight * scale
                story.append(KeepTogether([text(f"Photo {table} {photo['row_id']} – {photo['phase']}", s_h1), img]))
        def footer(canvas, doc):
            canvas.setFont(regular, 8)
            canvas.drawString(40, 25, 'Génie Civil Pro – ' + local_today().isoformat())
            canvas.drawRightString(A4[0] - 40, 25, f'Page {doc.page}')
        out = io.BytesIO()
        SimpleDocTemplate(out, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40).build(story, onFirstPage=footer, onLaterPages=footer)
        return out.getvalue()
    def export_excel(db, cid, user):
        db.access(cid, user)
        output = io.BytesIO()
        drop = {'supprime', 'chantier_id', 'devis_id'}
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for table in ('depenses', 'avancement', 'journalier', 'malfacons', 'materiel', 'devis'):
                frame = pd.DataFrame(db.rows(f'SELECT * FROM {table} WHERE chantier_id=? AND supprime=0 ORDER BY id', (cid,)))
                if not frame.empty:
                    frame = frame.drop(columns=[c for c in drop if c in frame.columns]).rename(columns=LABELS)
                frame.to_excel(writer, sheet_name=table, index=False)
            lines = pd.DataFrame(db.rows('SELECT d.numero, l.designation, l.unite, l.quantite, l.prix_unitaire_fcfa FROM lignes_devis l JOIN devis d ON d.id=l.devis_id WHERE d.chantier_id=? AND l.supprime=0 AND d.supprime=0 ORDER BY l.id', (cid,)))
            if not lines.empty:
                lines['Total HT (FCFA)'] = lines['quantite'] * lines['prix_unitaire_fcfa']
                lines = lines.rename(columns=LABELS)
            lines.to_excel(writer, sheet_name='lignes_devis', index=False)
            analyses = []
            for item in db.analyses(cid, user):
                resume = json.loads(item['resume'])
                analyses.append({'Nom': item['nom'], 'Type': item['type'], 'Auteur': item['auteur'], 'Date': str(item['ts'])[:16], 'Probabilité': resume.get('p'),
                                 'IC bas': resume.get('low'), 'IC haut': resume.get('high'), 'Moyenne': resume.get('mean'), 'P80': resume.get('p80'), 'P95': resume.get('p95'), 'Unité': resume.get('unit')})
            pd.DataFrame(analyses).to_excel(writer, sheet_name='analyses', index=False)
        return output.getvalue()
    # ---------------------------------------------------------------- centre de sauvegarde
    def backup_center(db, cid, user, gate):
        is_admin = user['role'] == 'admin'
        st.caption('SAUVEGARDES · DONNÉES · EXPORTS')
        if gate.get('open'):
            st.warning('Accès libre : aucun mot de passe configuré. Avant de partager le lien, définissez ADMIN_PASSWORD et VIEWER_PASSWORD dans les secrets de l’hébergement.')
        if db.postgres:
            st.info('Base PostgreSQL externe : les données sont conservées par votre fournisseur de base. Utilisez aussi l’instantané JSON comme copie de secours.')
        else:
            path, in_drive = storage_label(db.path)
            st.info('Emplacement de la base : ' + path)
            if in_drive:
                st.success('Dossier Google Drive détecté : la base et ses sauvegardes sont synchronisées par Drive.')
            else:
                st.caption('Pour garder vos données dans Google Drive, placez le dossier de données dans Drive (variable GENIE_CIVIL_DATA). Voir le guide fourni.')
        if is_admin and not db.postgres:
            with st.expander('Sauvegardes de la base', expanded=True):
                st.caption(f'Une copie horodatée est créée automatiquement (au plus toutes les 30 minutes, 12 conservées) dans : {db.backup_dir()}')
                backups = db.list_backups()
                if backups:
                    st.dataframe([{'Fichier': name, 'Taille (Ko)': round(size / 1024), 'Date': when.strftime('%Y-%m-%d %H:%M')} for name, size, when in backups], hide_index=True, width='stretch')
                else:
                    st.caption('Aucune sauvegarde automatique pour le moment.')
                if st.button('Créer une sauvegarde maintenant', icon=':material/save:', key='bk_now'):
                    target = db.auto_backup(force=True)
                    if target:
                        st.success('Sauvegarde créée : ' + target.name)
                    else:
                        st.warning('Sauvegarde impossible : dossier inaccessible.')
                if st.button('Préparer le fichier .db à télécharger', icon=':material/database:', key='bk_prepare'):
                    st.session_state.bk_db = (db.data_version(), db.backup())
                stored = st.session_state.get('bk_db')
                if stored:
                    if stored[0] != db.data_version():
                        st.info('Les données ont changé depuis la préparation : préparez à nouveau.')
                    st.download_button('Télécharger la sauvegarde SQLite', stored[1], file_name=f'genie-civil-{local_today()}.db', mime='application/octet-stream', icon=':material/download:', width='stretch')
                    st.caption('Contient aussi les photos. Conservez ce fichier dans un emplacement privé, par exemple votre Drive.')
            with st.expander('Restaurer une sauvegarde .db'):
                upload = st.file_uploader('Fichier de sauvegarde', type=['db', 'sqlite', 'sqlite3'], max_upload_size=200, key='bk_restore_file')
                confirm = st.checkbox('Je confirme : les données actuelles seront remplacées (une copie de sécurité est faite avant).', key='bk_restore_confirm')
                if st.button('Restaurer', icon=':material/restore:', key='bk_restore'):
                    if not upload:
                        st.warning('Choisissez un fichier.')
                    elif not confirm:
                        st.warning('Cochez la confirmation.')
                    else:
                        action(lambda: (db.restore_from_bytes(upload.getvalue(), user), 'Sauvegarde restaurée.')[1])
        if is_admin:
            with st.expander('Instantané JSON : données de démonstration et transfert', expanded=True):
                st.caption('L’instantané regroupe chantiers, saisies, photos et analyses enregistrées. Placé sous le nom demo_data.json à côté de app.py, il est rechargé automatiquement quand la base est vide (utile sur un hébergement gratuit).')
                with_photos = st.checkbox('Inclure les photos', value=True, key='snap_photos')
                if st.button('Préparer l’instantané', icon=':material/inventory_2:', key='snap_prepare'):
                    st.session_state.snap = (db.data_version(), json.dumps(db.export_snapshot(user, include_photos=with_photos), ensure_ascii=False).encode('utf-8'))
                snap = st.session_state.get('snap')
                if snap:
                    if snap[0] != db.data_version():
                        st.info('Les données ont changé depuis la préparation : préparez à nouveau.')
                    st.download_button('Télécharger demo_data.json', snap[1], file_name='demo_data.json', mime='application/json', icon=':material/download:', width='stretch')
                    st.caption(f'Taille : {len(snap[1]) / 1024:.0f} Ko')
                imported = st.file_uploader('Importer un instantané', type=['json'], max_upload_size=40, key='snap_file')
                if st.button('Importer l’instantané', icon=':material/upload:', key='snap_import'):
                    if imported:
                        action(lambda: snapshot_message(db.import_snapshot(json.loads(imported.getvalue()), user)))
                    else:
                        st.warning('Choisissez un fichier JSON.')
                if demo_available():
                    if st.button('Charger les données de démonstration', icon=':material/science:', key='demo_load'):
                        action(lambda: load_demo(db))
                else:
                    st.caption('Aucun fichier demo_data.json à côté de app.py.')
        if cid:
            with st.expander('Rapport PDF et export Excel du chantier', expanded=True):
                version = db.data_version()
                if st.button('Préparer le rapport PDF', icon=':material/picture_as_pdf:', width='stretch', key='bk_report'):
                    with st.spinner('Création du PDF…'):
                        st.session_state.report = (cid, version, report_with_analysis(db, cid, user))
                stored = st.session_state.get('report')
                if stored and stored[0] == cid:
                    if stored[1] == version:
                        st.download_button('Télécharger le rapport PDF', stored[2], file_name=f'chantier-{cid}.pdf', mime='application/pdf', width='stretch')
                    else:
                        st.info('Les données ont changé : préparez à nouveau le rapport.')
                if st.button('Préparer l’export Excel', icon=':material/table_view:', width='stretch', key='bk_excel'):
                    st.session_state.excel = (cid, version, export_excel(db, cid, user))
                stored = st.session_state.get('excel')
                if stored and stored[0] == cid:
                    if stored[1] == version:
                        st.download_button('Télécharger l’export Excel', stored[2], file_name=f'chantier-{cid}.xlsx', icon=':material/download:', width='stretch')
                    else:
                        st.info('Les données ont changé : préparez à nouveau l’export.')
        st.caption('Google Drive : déposez les fichiers téléchargés dans votre dossier Drive ou placez directement le dossier de données dans Drive (voir le guide).')
    # ---------------------------------------------------------------- analyses enregistrées
    def analysis_resume(r):
        vals = np.asarray(r['values'], float)
        risk = r['risk']
        return dict(label=r['label'], unit=r['unit'], p=risk['p'], low=risk['low'], high=risk['high'], count=risk['count'], n=risk['n'],
                    mean=float(vals.mean()), sd=float(vals.std(ddof=1)) if vals.size > 1 else 0.0,
                    p50=float(np.quantile(vals, .5)), p80=float(np.quantile(vals, .8)), p95=float(np.quantile(vals, .95)))
    def save_analysis_form(db, cid, user, kind, serialized, r):
        if user['role'] not in ('admin', 'editeur'):
            return
        with st.form(form_key('save_analysis')):
            name = st.text_input('Nom de l’analyse à enregistrer', value=f'{kind} - {local_today().isoformat()}', max_chars=80)
            if st.form_submit_button('Enregistrer cette analyse dans le chantier', icon=':material/save:', width='stretch'):
                action(lambda: (db.save_analysis(cid, name, kind, serialized, analysis_resume(r), user), 'Analyse enregistrée dans le chantier.')[1])
    def load_saved_analysis(config_text):
        try:
            config = validate_analysis(json.loads(config_text))
        except Exception as exc:
            st.session_state['saved_error'] = 'Analyse illisible : ' + str(exc)[:120]
            return
        st.session_state.setdefault('ana_loaded', {})[config['kind']] = config
        for key in list(st.session_state):
            if key.startswith('ana_param_') or key.startswith('ana_editor_'):
                del st.session_state[key]
        st.session_state['ana_kind'] = config['kind']
        st.session_state.pop('ana_result', None)
        st.session_state['ana_notice'] = 'Analyse chargée : ' + config['kind'] + '. Cliquez sur « Calculer l’analyse ».'
        dashboard_route('Analyses probabilistes', 'Analyses probabilistes')
    def show_fig(fig):
        st.image(fig_png(fig), width='stretch')
    def fig_compare(ra, rb, name_a, name_b):
        fig, ax = new_fig()
        for r, name, color in ((ra, name_a, C_MAIN), (rb, name_b, C_ALT)):
            data = np.sort(np.asarray(r['values'], float))
            stride = max(1, data.size // 1500)
            ax.plot(data[::stride], (np.arange(1, data.size + 1) / data.size)[::stride], color=color, lw=2.2, label=f"{name} : P = {100 * r['risk']['p']:.2f} %")
            ax.axvline(float(np.quantile(data, .95)), color=color, ls=':', lw=1.2)
        style_axes(ax, 'Comparaison des répartitions (pointillés : P95)', ra['unit'], 'Probabilité cumulée')
        ax.legend(fontsize=8, frameon=False, loc='lower right')
        return fig
    def saved_analyses_workspace(db, cid, user):
        db.access(cid, user)
        st.caption('ANALYSES ENREGISTRÉES DANS CE CHANTIER')
        if 'saved_error' in st.session_state:
            st.error(st.session_state.pop('saved_error'))
        rows = db.analyses(cid, user)
        if not rows:
            st.info('Aucune analyse enregistrée. Calculez une analyse, puis utilisez « Enregistrer cette analyse dans le chantier ».')
            return
        table = []
        for row in rows:
            resume = json.loads(row['resume'])
            table.append({'N°': row['id'], 'Nom': row['nom'], 'Type': row['type'], 'Probabilité': f"{100 * resume['p']:.2f} %",
                          'Moyenne': f"{resume['mean']:,.2f} {resume['unit']}", 'P95': f"{resume['p95']:,.2f} {resume['unit']}",
                          'Auteur': row['auteur'], 'Date': str(row['ts'])[:16].replace('T', ' ')})
        st.dataframe(table, hide_index=True, width='stretch')
        ids = {row['id']: row for row in rows}
        chosen = st.selectbox('Analyse', list(ids), format_func=lambda key: f"{key} - {ids[key]['nom']}", key='saved_choice')
        row = ids[chosen]
        left, right = st.columns(2)
        left.button('Recharger dans l’outil', icon=':material/upload:', on_click=load_saved_analysis, args=(row['config'],), key='saved_load', width='stretch')
        if user['role'] in ('admin', 'editeur') and right.button('Archiver', icon=':material/archive:', key='saved_archive', width='stretch'):
            action(lambda: db.archive_analysis(chosen, user))
        same = [item for item in rows if item['type'] == row['type'] and item['id'] != chosen]
        if same:
            with st.expander('Comparer avec une autre analyse du même type'):
                other_id = st.selectbox('Comparer avec', [item['id'] for item in same], format_func=lambda key: f"{key} - {ids[key]['nom']}", key='saved_other')
                try:
                    ra, rb = compute_analysis(row['config']), compute_analysis(ids[other_id]['config'])
                    if ra['unit'] == rb['unit']:
                        show_fig(fig_compare(ra, rb, row['nom'], ids[other_id]['nom']))
                    else:
                        st.warning('Unités différentes : comparaison impossible.')
                except (ValueError, KeyError) as exc:
                    st.error(str(exc))
    # ---------------------------------------------------------------- laboratoire : modules
    LAB_MODULES = ['Dépenses : ajustement de lois', 'Malfaçons : Poisson et Bayes', 'Prévision du délai', 'Prévision du coût final',
                   'Matériaux : intervalles et tests', 'Poutre : fiabilité et fragilité', 'Calculateur de lois de probabilité',
                   'Grands nombres et théorème central limite']
    def _money(v):
        return f'{v:,.0f} FCFA'
    def lab_expenses(db, cid, user):
        rows = db.rows('SELECT * FROM depenses WHERE chantier_id=? AND supprime=0', (cid,))
        category = st.selectbox('Catégorie', ['Toutes'] + sorted({r['categorie'] for r in rows}), key='lab_exp_cat')
        values = [float(r['montant_fcfa']) for r in rows if category == 'Toutes' or r['categorie'] == category]
        st.markdown('Les montants de dépenses sont **positifs et asymétriques**. On compare plusieurs lois (lognormale, gamma, Weibull, normale) ; le critère **AIC** les classe : plus il est bas, mieux le modèle est soutenu par les données.')
        if len(values) < 5:
            st.info(f'{len(values)} dépense(s) dans cette sélection : au moins 5 sont nécessaires.')
            return
        fits, table = fit_positive(values)
        best = table[0]['loi']
        d = describe_sample(values)
        metrics([('Dépenses', str(d['n'])), ('Moyenne', _money(d['mean'])), ('Médiane', _money(d['median'])), ('Écart-type', _money(d['sd'])),
                 ('Coefficient de variation', f"{d['cv']:.2f}"), ('Asymétrie', f"{d['skew']:.2f}" if np.isfinite(d['skew']) else '—')])
        show_fig(fig_fit_hist(values, fits, best, 'FCFA', 'Montant des dépenses : histogramme et lois ajustées'))
        show_fig(fig_fit_cdf_qq(values, fits, best, 'FCFA'))
        st.dataframe([{'Loi': r['loi'], 'AIC': round(r['aic'], 1), 'Écart de Kolmogorov-Smirnov': round(r['ks_stat'], 3), 'p-valeur KS (indicative)': round(r['ks_p'], 3)} for r in table], hide_index=True, width='stretch')
        st.caption('La p-valeur de KS est indicative : les paramètres sont estimés sur les mêmes données.')
        threshold = st.number_input('Seuil de dépense (FCFA)', min_value=1.0, value=float(max(1, round(d['p95']))), key=f'lab_exp_thr_{category}')
        observed = float(np.mean(np.asarray(values) > threshold))
        st.write(f'Probabilité qu’une dépense dépasse {_money(threshold)} : **{fits[best].sf(threshold):.1%}** selon la loi {best} ; fréquence observée : {observed:.1%}.')
    def lab_incidents(db, cid, user):
        site = db.rows('SELECT * FROM chantiers WHERE id=?', (cid,))[0]
        rows = db.rows('SELECT * FROM malfacons WHERE chantier_id=? AND supprime=0', (cid,))
        st.markdown('Le **nombre de malfaçons par période** suit souvent une loi de **Poisson**. Le taux λ est estimé avec une approche **bayésienne** (loi Gamma a posteriori) ; la proportion de malfaçons résolues l’est avec une loi **Bêta**.')
        if len(rows) < 3:
            st.info(f'{len(rows)} malfaçon(s) enregistrée(s) : au moins 3 sont nécessaires.')
            return
        days = 7 if st.radio('Période de comptage', ['Semaine', 'Mois'], horizontal=True, key='lab_inc_period') == 'Semaine' else 30
        label = 'semaine' if days == 7 else 'mois'
        dates = [dt.date.fromisoformat(r['date_signalement']) for r in rows]
        start = min(dt.date.fromisoformat(site['date_debut']), min(dates))
        end = max(local_today(), max(dates))
        counts = period_counts(dates, start, end, days)
        if counts.size < 3:
            st.info('Période d’observation trop courte pour estimer une fréquence.')
            return
        summary = poisson_summary(counts)
        metrics([('Périodes observées', str(summary['n'])), ('Malfaçons au total', str(summary['total'])), (f'Moyenne par {label} (λ)', f"{summary['mean']:.2f}"),
                 ('Indice de dispersion', f"{summary['dispersion']:.2f}" if np.isfinite(summary['dispersion']) else '—')])
        show_fig(fig_poisson(counts, summary, label))
        if np.isfinite(summary['p_overdispersion']):
            verdict = 'La dispersion est compatible avec une loi de Poisson.' if summary['p_overdispersion'] > .05 else 'Sur-dispersion : les malfaçons arrivent en grappes, le modèle de Poisson est trop optimiste.'
            st.write(f"Test du khi-deux de dispersion : p = {summary['p_overdispersion']:.3f}. {verdict}")
        mean_rate = max(summary['mean'], .1)
        st.write(f"Avec ce taux, la probabilité d’avoir **au moins 3 malfaçons** dans une même {label} est de **{stats.poisson.sf(2, mean_rate):.1%}** et celle de n’en avoir **aucune** de **{stats.poisson.pmf(0, mean_rate):.1%}**.")
        target = st.number_input(f'Taux cible λ (malfaçons par {label})', min_value=.05, value=max(round(summary['mean'], 1), .5), step=.1, key='lab_inc_target')
        post, info = gamma_poisson_posterior(counts)
        show_fig(fig_rate_posterior(post, info, target))
        st.caption('A priori de Jeffreys Gamma(0,5 ; 0). L’intervalle de crédibilité contient λ avec 95 % de probabilité, sous le modèle.')
        choice = st.selectbox('Proportion étudiée', ['Taux de résolution', 'Part des malfaçons élevées ou critiques'], key='lab_inc_prop')
        hits = sum(1 for r in rows if (r['statut_resolution'] == 'Résolu' if choice == 'Taux de résolution' else r['criticite'] in ('Élevée', 'Critique')))
        threshold = st.slider('Seuil de comparaison', .05, .95, .5, .05, key='lab_inc_threshold')
        bpost, binfo = beta_posterior(hits, len(rows))
        show_fig(fig_beta(bpost, stats.beta(1, 1), binfo, threshold, f'{choice.lower()} ({hits} sur {len(rows)})'))
    def lab_schedule(db, cid, user):
        site = db.rows('SELECT * FROM chantiers WHERE id=?', (cid,))[0]
        rows = db.rows('SELECT id,date_saisie,pourcentage FROM avancement WHERE chantier_id=? AND supprime=0', (cid,))
        st.markdown('La **régression linéaire** de l’avancement donne une vitesse moyenne et son **incertitude** (loi de Student). On en déduit la **loi de la date de fin** et la probabilité de respecter l’échéance. Hypothèse : vitesse constante, alors qu’un chantier réel suit plutôt une courbe en S.')
        res = forecast_progress(daily_progress(rows), dt.date.fromisoformat(site['date_fin_prevue']))
        fin = res['dates'][50]
        metrics([('Vitesse moyenne', f"{res['slope']:.2f} %/jour"), ('Qualité R²', f"{res['r2']:.3f}"), ('Fin médiane prévue', fin.isoformat() if fin else 'non atteinte'),
                 ('P(terminer avant l’échéance)', f"{res['p_deadline']:.1%}")])
        show_fig(fig_progress_forecast(res))
        show_fig(fig_completion_cdf(res))
        st.write('Dates de fin : ' + ' · '.join(f"P{q} = {d.isoformat() if d else 'non atteinte'}" for q, d in res['dates'].items()) + f" · échéance contractuelle : {site['date_fin_prevue']}.")
        if res['df'] < 3:
            st.warning('Moins de 5 dates d’avancement : l’incertitude est très grande, les prévisions sont à prendre avec prudence.')
    def lab_cost(db, cid, user):
        site = db.rows('SELECT * FROM chantiers WHERE id=?', (cid,))[0]
        progress = db.rows('SELECT id,date_saisie,pourcentage FROM avancement WHERE chantier_id=? AND supprime=0', (cid,))
        expenses = db.rows('SELECT date_depense,montant_fcfa FROM depenses WHERE chantier_id=? AND supprime=0', (cid,))
        st.markdown('On relie les **dépenses cumulées** à l’**avancement** par une régression, puis on prévoit le **coût à 100 %** avec un **intervalle de prédiction** (Student). La probabilité de dépasser le budget en découle. Le coefficient de **Spearman** mesure la liaison monotone entre dépenses et avancement.')
        if float(site['budget_fcfa']) <= 0:
            st.info('Définissez un budget pour estimer le risque de dépassement.')
            return
        res = forecast_cost(cost_pairs(progress, expenses), float(site['budget_fcfa']))
        metrics([('Coût final prévu', _money(res['fit100'])), ('Intervalle 80 %', f"{short_number(res['low80'])} à {short_number(res['high80'])}"),
                 ('P(dépasser le budget)', f"{res['p_over']:.1%}"), ('Corrélation de Spearman', f"{res['rho']:.2f}")])
        show_fig(fig_cost_forecast(res))
        st.caption('Hypothèse : dépenses cumulées proportionnelles à l’avancement, résidus indépendants et de variance constante.')
    def _parse_values(text):
        return [float(v.strip().replace(',', '.')) for v in text.replace(';', '\n').splitlines() if v.strip()]
    def lab_materials(db, cid, user):
        st.markdown('Pour un échantillon d’essais : **intervalle de confiance** de la moyenne (Student) et de l’écart-type (khi-deux), **test t unilatéral** contre le seuil requis, **valeur caractéristique** (fractile 5 % avec 95 % de confiance, facteur de tolérance par la loi de Student non centrée) et **bootstrap**.')
        saved = [a for a in db.analyses(cid, user) if a['type'] == 'Matériaux']
        options = ['Saisie manuelle'] + [f"{a['id']} - {a['nom']}" for a in saved]
        source = st.selectbox('Source des essais', options, key='lab_mat_source')
        if source == 'Saisie manuelle':
            base = st.session_state.get('ana_loaded', {}).get('Matériaux', default_analysis('Matériaux'))
            text = st.text_area('Essais (un par ligne ou séparés par ;)', value='\n'.join(map(str, base['values'])), key='lab_mat_text')
            try:
                values = _parse_values(text)
            except ValueError:
                st.error('Valeurs numériques attendues.')
                return
            unit = st.text_input('Unité', value=base['unit'], max_chars=30, key='lab_mat_unit')
            default_limit = float(base['limit'])
        else:
            config = json.loads(next(a for a in saved if source.startswith(str(a['id']) + ' - '))['config'])
            values, unit, default_limit = config['values'], config['unit'], float(config['limit'])
        required = st.number_input('Seuil requis', min_value=.001, value=default_limit, key='lab_mat_required_' + source)
        res = material_inference(values, required)
        metrics([('Essais', str(res['n'])), ('Moyenne', f"{res['mean']:.2f} {unit}"), ('Écart-type', f"{res['sd']:.2f} {unit}"),
                 ('IC 95 % de la moyenne', f"{res['ci_mean'][0]:.2f} à {res['ci_mean'][1]:.2f}"), ('IC 95 % de l’écart-type', f"{res['ci_sd'][0]:.2f} à {res['ci_sd'][1]:.2f}"),
                 ('Valeur caractéristique', f"{res['fk']:.2f} {unit}")])
        show_fig(fig_material_hist(res, unit))
        show_fig(fig_t_test(res))
        st.write(f"Test de H0 « moyenne ≤ seuil » contre H1 « moyenne > seuil » : t = {res['t_stat']:.2f}, p = {res['p_greater']:.4f}. "
                 + ('H0 est rejetée au seuil de 5 %.' if res['p_greater'] < .05 else 'H0 n’est pas rejetée au seuil de 5 %.')
                 + f" Probabilité qu’un essai soit sous le seuil (loi normale ajustée) : {res['p_below']:.2%}.")
        st.write(f"Valeur caractéristique : {res['fk']:.2f} {unit} avec le facteur de tolérance k = {res['k']:.3f} (estimation simple moyenne − 1,645 s : {res['fk_simple']:.2f} {unit}). Elle est {'supérieure' if res['fk'] >= required else 'inférieure'} au seuil requis.")
        show_fig(fig_bootstrap(res, unit))
        if res['n'] < 10:
            st.warning('Moins de 10 essais : les intervalles sont larges et l’hypothèse de normalité est peu vérifiable.')
    def lab_beam(db, cid, user):
        st.markdown('La **fiabilité** s’exprime par l’indice **β = μg / σg** (Cornell) et la probabilité de ruine **Pf = P(g < 0)**. La **courbe de fragilité** montre comment Pf augmente quand on multiplie les charges. Les repères 10⁻³ et 10⁻⁴ sont des ordres de grandeur : la cible dépend de la norme et de la classe de conséquences.')
        saved = [a for a in db.analyses(cid, user) if a['type'] == 'Poutre']
        options = ['Valeurs de la session ou par défaut'] + [f"{a['id']} - {a['nom']}" for a in saved]
        source = st.selectbox('Source des paramètres', options, key='lab_beam_source')
        if source.startswith('Valeurs'):
            base = dict(st.session_state.get('ana_loaded', {}).get('Poutre', default_analysis('Poutre')))
        else:
            base = json.loads(next(a for a in saved if source.startswith(str(a['id']) + ' - '))['config'])
        c1, c2, c3 = st.columns(3)
        base['P'] = c1.number_input('Charge centrale P (kN)', min_value=0.0, value=float(base['P']), key='lab_beam_P_' + source)
        base['q'] = c2.number_input('Charge répartie q (kN/m)', min_value=0.0, value=float(base['q']), key='lab_beam_q_' + source)
        base['fy'] = c3.number_input('Résistance fy (MPa)', min_value=1.0, value=float(base['fy']), key='lab_beam_fy_' + source)
        fmax = st.slider('Facteur de charge maximal de la courbe de fragilité', 1.5, 4.0, 2.6, .1, key='lab_beam_fmax')
        validate_analysis(base)
        with st.spinner('Simulation en cours…'):
            r = compute_analysis(canonical(base))
            curve = fragility_curve(base, np.linspace(.5, fmax, 16))
        v = np.asarray(r['values'], float)
        sd = float(v.std(ddof=1))
        beta = float(v.mean() / sd) if sd > 0 else float('inf')
        metrics([('Indice de fiabilité β', f'{beta:.2f}' if np.isfinite(beta) else '∞'), ('Pf par Monte-Carlo', f"{r['risk']['p']:.3%}"),
                 ('Pf par Cornell Φ(−β)', f'{stats.norm.cdf(-beta):.3%}' if np.isfinite(beta) else '0 %'), ('Marge moyenne g', f'{v.mean():.1f} MPa')])
        show_fig(fig_margin(v, r['risk']))
        show_fig(fig_fragility(curve))
        st.caption('Monte-Carlo : 6 000 tirages par point de la courbe. Cornell suppose une marge g normale ; il peut s’écarter du Monte-Carlo dans les queues de distribution.')
    def lab_laws(db, cid, user):
        st.markdown('Choisissez une loi, réglez ses paramètres, puis lisez les **probabilités**, la **densité** (ou la loi de masse), la **fonction de répartition**, les **moments** et les **quantiles**.')
        name = st.selectbox('Loi de probabilité', list(LAB_LAWS), key='lab_law')
        spec = LAB_LAWS[name]
        st.caption('Usage typique : ' + spec['usage'])
        params = {}
        cols = st.columns(len(spec['params']))
        for col, (key, label, default, low, high) in zip(cols, spec['params']):
            is_int = isinstance(default, int)
            kwargs = dict(value=default, key=f'lab_law_{name}_{key}')
            if low is not None:
                kwargs['min_value'] = int(low) if is_int else float(low)
            if high is not None:
                kwargs['max_value'] = int(high) if is_int else float(high)
            params[key] = col.number_input(label, **kwargs)
        d = build_law(name, params)
        info = describe_law(d)
        a_default, b_default = (float(d.ppf(.25)), float(d.ppf(.75)))
        c1, c2 = st.columns(2)
        a = c1.number_input('Borne a', value=round(a_default, 4), key=f'lab_law_{name}_bound_a')
        b = c2.number_input('Borne b', value=round(b_default, 4), key=f'lab_law_{name}_bound_b')
        if not b >= a:
            st.warning('Il faut b ≥ a.')
            return
        fig, prob = fig_law(d, spec['discrete'], a, b, name)
        show_fig(fig)
        metrics([(f'P({a:g} ≤ X ≤ {b:g})', f'{prob:.4f}'), ('Espérance', f"{info['mean']:.4g}"), ('Écart-type', f"{info['sd']:.4g}"),
                 ('Asymétrie', f"{info['skew']:.3g}"), ('Aplatissement (excès)', f"{info['kurt']:.3g}")])
        st.dataframe([{'Quantile': f'{int(q * 100)} %', 'Valeur': round(v, 4)} for q, v in info['quantiles'].items()], hide_index=True, width='stretch')
    def lab_limits(db, cid, user):
        st.markdown('**Loi des grands nombres** : la moyenne d’un échantillon converge vers l’espérance quand n augmente. **Théorème central limite** : la moyenne de k variables indépendantes tend vers une loi normale, même si la loi d’origine est asymétrique.')
        presets = {'Exponentielle (asymétrique)': ('Exponentielle', {'lam': .5}), 'Lognormale (très asymétrique)': ('Lognormale', {'mu': 0.0, 'sigma': .8}),
                   'Uniforme': ('Uniforme', {'a': 0.0, 'b': 1.0}), 'Gamma': ('Gamma', {'k': 2.0, 'theta': 1.5}),
                   'Binomiale (discrète)': ('Binomiale', {'n': 10, 'p': .3}), 'Poisson (discrète)': ('Poisson', {'lam': 3.0})}
        choice = st.selectbox('Loi de départ', list(presets), key='lab_lim_law')
        name, params = presets[choice]
        d = build_law(name, params)
        n = st.slider('Nombre d’observations n (grands nombres)', 50, 20000, 3000, 50, key='lab_lim_n')
        show_fig(fig_lgn(sim_lgn(d, n, 6), float(d.mean())))
        k = st.slider('Nombre de variables k sommées (théorème central limite)', 1, 200, 30, key='lab_lim_k')
        means, mu, se = sim_tcl(d, k)
        ks, skews = tcl_skew_curve(d)
        show_fig(fig_tcl(means, mu, se, k, name, ks, skews))
        st.write(f'Espérance théorique : {mu:.3f} ; moyenne des moyennes simulées : {means.mean():.3f} ; écart-type théorique de la moyenne σ/√k = {se:.3f}, simulé : {means.std():.3f}.')
    def lab_workspace(db, cid, user):
        db.access(cid, user)
        st.caption('NOTIONS DE PROBABILITÉ · COURBES CALCULÉES À PARTIR DES DONNÉES DU CHANTIER')
        module = st.selectbox('Module', LAB_MODULES, key='lab_module')
        runner = {LAB_MODULES[0]: lab_expenses, LAB_MODULES[1]: lab_incidents, LAB_MODULES[2]: lab_schedule, LAB_MODULES[3]: lab_cost,
                  LAB_MODULES[4]: lab_materials, LAB_MODULES[5]: lab_beam, LAB_MODULES[6]: lab_laws, LAB_MODULES[7]: lab_limits}[module]
        try:
            runner(db, cid, user)
        except ValueError as exc:
            st.warning(str(exc))
        except Exception as exc:  # un module en erreur ne doit pas arrêter l'application
            st.error('Ce module a rencontré une erreur (' + type(exc).__name__ + ') : ' + str(exc)[:160])
    import datetime as dt
    import io
    import sqlite3
    import pandas as pd
    import streamlit as st
    st.set_page_config(page_title='Génie civil pro', page_icon=':material/construction:', layout='wide')
    install_layout()
    st.html('''<header class="app-masthead">
    <p class="eyebrow">PILOTAGE DES TRAVAUX</p><h1>Génie Civil Pro</h1>
    <p>Chantiers &nbsp; / &nbsp; Budget &nbsp; / &nbsp; Qualité &nbsp; / &nbsp; Probabilités</p>
    <div class="masthead-colors" aria-hidden="true"><span></span><span></span><span></span><span></span></div></header>''')
    database_url = _secret('DATABASE_URL')
    gate = access_gate()
    db = Database(url=database_url)
    if 'flash' in st.session_state:
        st.success(st.session_state.pop('flash'))
    if 'seed_error' in st.session_state:
        st.warning(st.session_state.pop('seed_error'))
    def save(table, values, user):
        stamp = (table, json.dumps(values, sort_keys=True, default=str))
        last = st.session_state.get('last_save')
        if last and last[0] == stamp and time.time() - last[1] < 10:
            st.info('Cet enregistrement vient d’être effectué.')
            return
        try:
            db.insert(table, values, user)
        except Exception as exc:
            st.error(str(exc) if isinstance(exc,ValueError) else 'Enregistrement impossible. Vérifiez les valeurs (' + type(exc).__name__ + ').')
            return
        st.session_state.last_save = (stamp, time.time())
        st.session_state.flash = 'Enregistrement effectué.'
        st.session_state.form_nonce = st.session_state.get('form_nonce', 0) + 1
        st.rerun()
    try:
        try:
            maybe_seed_demo(db)
            user = workspace_user(db, gate['role'])
            db.display_name = f"{gate['name']} ({ROLE_LABELS[gate['role']]})"
            if user['role'] != 'admin':
                db.sync_viewer_access(user['id'])
            db.auto_backup()
        except ValueError as exc:
            st.error(str(exc))
            st.stop()
        if st.session_state.get('direct_access_revision') != 1:
            for key in list(st.session_state):
                if key.startswith('ana_') or key in ('analysis_scope', 'report'):
                    del st.session_state[key]
            st.session_state.domain = 'Synthèse'
            st.session_state.section = 'Synthèse'
            st.session_state.direct_access_revision = 1
        st.session_state.user = user
        editable = user['role'] in ('admin', 'editeur')
        db.admin = user['role'] == 'admin'
        with st.sidebar:
            st.subheader('Espace chantier')
            if gate['open']:
                st.badge('Accès direct', icon=':material/computer:', color='blue')
                st.caption('Accès libre : aucun mot de passe configuré.')
            else:
                st.badge(ROLE_LABELS[gate['role']], icon=':material/lock:', color='green' if gate['role'] == 'admin' else 'blue')
                st.caption(gate['name'])
                st.button('Se déconnecter', icon=':material/logout:', on_click=logout, width='stretch', key='logout')
        domains = {
            'Synthèse': ['Synthèse'],
            'Chantiers': ['Chantiers', 'Rapport du jour', 'Journalier', 'Avancement', 'Matériel'],
            'Finances': ['Dépenses', 'Devis'],
            'Qualité': ['Malfaçons'],
            'Analyses probabilistes': ['Analyses probabilistes', 'Laboratoire de probabilités', 'Analyses enregistrées'],
            'Administration': ['Sauvegardes', 'Historique', 'Archives'],
        }
        st.sidebar.button('Tableau de bord',icon=':material/dashboard:',type='primary',width='stretch',on_click=dashboard_route,args=('Synthèse','Synthèse'),key='dashboard_home')
        for nav_domain, nav_icon in [('Chantiers','construction'), ('Finances','payments'), ('Qualité','verified'), ('Analyses probabilistes','query_stats'), ('Administration','settings')]:
            st.sidebar.button(nav_domain, icon=f':material/{nav_icon}:', width='stretch',
                              on_click=dashboard_route, args=(nav_domain,domains[nav_domain][0]), key=f'nav_{nav_icon}')
        domain = st.sidebar.selectbox('Domaine', list(domains), key='domain')
        if st.session_state.get('section') not in domains[domain]:
            st.session_state['section'] = domains[domain][0]
        section = st.sidebar.selectbox('Rubrique', domains[domain], key='section')
        sites = db.sites(user)
        site_map = {row['id']: row for row in sites}
        cid = st.selectbox('Chantier', list(site_map), format_func=lambda key: f"{site_map[key]['code']} - {site_map[key]['nom']}") if sites else None
        st.divider()
        st.subheader('Tableau de bord' if section == 'Synthèse' else section)
        if cid:
            db.access(cid,user)
        if section == 'Historique':
            history(db,cid,user)
        elif section == 'Archives':
            archived=db.sites(user,archived=True)
            records(archived,'archived_sites','Chantiers archivés')
            if archived:
                rid=st.selectbox('Chantier à restaurer',[r['id'] for r in archived])
                if st.button('Restaurer le chantier',icon=':material/restore:'):
                    action(lambda:db.archive('chantiers',rid,user,restore=True))
            if cid:
                table=st.selectbox('Archives du chantier',['depenses','avancement','journalier','malfacons','materiel','devis'])
                archived_rows=db.rows(f'SELECT * FROM {table} WHERE chantier_id=? AND supprime=1',(cid,))
                records(archived_rows,'archives_records','Archives')
                if archived_rows:
                    rid=st.selectbox('Enregistrement à restaurer',[r['id'] for r in archived_rows])
                    if st.button('Restaurer l’enregistrement',icon=':material/restore:'):
                        action(lambda:db.archive(table,rid,user,restore=True))
        elif section == 'Chantiers':
            if editable:
                with st.form(form_key('site')):
                    code = st.text_input('Code')
                    name = st.text_input('Nom du chantier')
                    client = st.text_input('Client')
                    loc = st.text_input('Localisation')
                    budget = st.number_input('Budget (FCFA)', min_value=0.0, step=1000.0)
                    debut = st.date_input('Date de début', value=local_today())
                    fin = st.date_input('Date de fin prévue', value=local_today())
                    if st.form_submit_button('Créer le chantier', icon=':material/add:', width='stretch'):
                        save('chantiers', dict(code=code.strip(), nom=name.strip(), client=client, localisation=loc, budget_fcfa=budget, date_debut=debut.isoformat(), date_fin_prevue=fin.isoformat()), user)
            site_rows=db.sites(user)
            records(filter_rows(site_rows,'sites'), 'sites', 'Chantiers')
            manage(db,'chantiers',site_rows,user)
        elif section == 'Sauvegardes':
            backup_center(db, cid, user, gate)
        elif section == 'Analyses probabilistes' and cid:
            analysis_workspace(db,cid,user)
        elif section == 'Laboratoire de probabilités' and cid:
            lab_workspace(db,cid,user)
        elif section == 'Analyses enregistrées' and cid:
            saved_analyses_workspace(db,cid,user)
        elif not cid:
            for column, tone, label, value in zip(st.columns(4), ['budget','spent','progress','quality'],
                    ['Chantiers actifs','Dépenses enregistrées','Avancement','Malfaçons ouvertes'], ['0','0 FCFA','—','0']):
                with column, st.container(key=f'dash_kpi_{tone}'):
                    st.metric(label, value)
                    st.caption('Aucun chantier sélectionné')
            st.html('<section class="empty-workspace"><h3>Votre espace chantier est prêt</h3><p>Aucun chantier enregistré pour le moment.</p></section>')
            if editable:
                st.button('Créer mon premier chantier',icon=':material/add:',type='primary',on_click=dashboard_route,args=('Chantiers','Chantiers'))
            if user['role'] == 'admin' and demo_available():
                if st.button('Charger les données de démonstration',icon=':material/science:',key='demo_first'):
                    action(lambda: load_demo(db))
        elif section == 'Synthèse':
            dashboard(db,cid,user)
        elif section == 'Rapport du jour':
            if not editable:
                st.info('Votre compte permet la consultation uniquement.')
            else:
                with st.form(form_key('quick_report')):
                    date=st.date_input('Date du rapport', value=local_today())
                    meteo=st.text_input('Météo')
                    effectif=st.number_input('Effectif',min_value=0)
                    travaux=st.text_area('Travaux réalisés')
                    incidents=st.text_area('Incidents')
                    photo=st.file_uploader('Photo du jour',type=['jpg','jpeg','png'],max_upload_size=5)
                    if st.form_submit_button('Enregistrer le rapport du jour',icon=':material/save:',width='stretch'):
                        def quick_save():
                            # A failed photo must not leave a half-saved journal entry.
                            with db.transaction():
                                rid=db.insert('journalier',dict(chantier_id=cid,date_jour=date.isoformat(),meteo=meteo,effectif=effectif,travaux_realises=travaux,incidents=incidents),user)
                                if photo: db.photo('journalier',rid,'Journalier',photo.getvalue(),user)
                        action(quick_save)
        else:
            specs = {
                'Journalier': ('journalier', [('date_jour','Date','date'), ('meteo','Météo','text'), ('effectif','Effectif','int'), ('travaux_realises','Travaux réalisés','area'), ('incidents','Incidents','area')]),
                'Malfaçons': ('malfacons', [('element','Élément','text'), ('type_defaut','Type de défaut','text'), ('criticite','Criticité',['Faible','Moyenne','Élevée','Critique']), ('description','Description','area'), ('action_corrective','Action corrective','area')]),
                'Dépenses': ('depenses', [('categorie','Catégorie',['materiaux','main_oeuvre','materiel','sous_traitance','transport','autre']), ('libelle','Libellé','text'), ('montant_fcfa','Montant (FCFA)','number'), ('date_depense','Date','date'), ('reference_piece','Référence de pièce','text')]),
                'Avancement': ('avancement', [('pourcentage','Avancement (%)','percent'), ('description','Description','area'), ('date_saisie','Date','date')]),
                'Matériel': ('materiel', [('designation','Désignation','text'), ('quantite','Quantité','number'), ('unite','Unité','text'), ('date_reception','Date de réception','date')]),
                'Devis': ('devis', [('numero','Numéro','text'), ('objet','Objet','text'), ('tva_pct','TVA (%)','percent')]),
            }
            table, fields = specs[section]
            if editable:
                with st.form(form_key('record')):
                    values = {'chantier_id': cid}
                    for key, label, kind in fields:
                        if isinstance(kind, list):
                            values[key] = st.selectbox(label, kind)
                        elif kind == 'date':
                            values[key] = st.date_input(label, value=local_today()).isoformat()
                        elif kind in ('int', 'number', 'percent'):
                            values[key] = st.number_input(label, min_value=0 if kind == 'int' else 0.0, max_value=100.0 if kind == 'percent' else None, value=19.25 if key == 'tva_pct' else (0 if kind == 'int' else 0.0))
                        elif kind == 'area':
                            values[key] = st.text_area(label)
                        else:
                            values[key] = st.text_input(label)
                    if table == 'malfacons':
                        values['date_signalement'] = local_today().isoformat()
                    if st.form_submit_button('Enregistrer', icon=':material/save:', width='stretch'):
                        save(table, values, user)
            rows = db.rows(f'SELECT * FROM {table} WHERE chantier_id=? AND supprime=0 ORDER BY id DESC', (cid,))
            records(filter_rows(rows,table), table, f'Liste : {section}')
            manage(db,table,rows,user)
            if table in ('malfacons','journalier'):
                photos(db,table,rows,cid,user)
            if table == 'malfacons' and rows and editable:
                with st.form('resolve'):
                    rid = st.selectbox('Malfaçon', [row['id'] for row in rows])
                    status = st.selectbox('Résolution', ['Ouvert', 'En cours', 'Résolu'])
                    if st.form_submit_button('Modifier le statut', icon=':material/check:', width='stretch'):
                        action(lambda: db.update('malfacons',rid,{'statut_resolution':status},user))
            if table == 'devis' and rows:
                did = st.selectbox('Devis', [row['id'] for row in rows], format_func=lambda key: next(row['numero'] for row in rows if row['id'] == key))
                if editable:
                    with st.form(form_key('quote_line')):
                        des = st.text_input('Désignation de la ligne')
                        unit = st.text_input('Unité de la ligne', value='u')
                        qty = st.number_input('Quantité de la ligne', min_value=0.0)
                        price = st.number_input('Prix unitaire (FCFA)', min_value=0.0)
                        if st.form_submit_button('Ajouter la ligne', icon=':material/add:', width='stretch'):
                            save('lignes_devis', dict(devis_id=did, designation=des, unite=unit, quantite=qty, prix_unitaire_fcfa=price), user)
                lines = db.rows('SELECT * FROM lignes_devis WHERE devis_id=? AND supprime=0', (did,))
                records(lines, 'quote_lines', 'Lignes du devis')
                manage(db,'lignes_devis',lines,user)
                ht = sum(row['quantite'] * row['prix_unitaire_fcfa'] for row in lines)
                vat = next(row['tva_pct'] for row in rows if row['id'] == did)
                st.metric('Total TTC (FCFA)', f'{ht * (1 + vat / 100):,.0f}')
    finally:
        db.conn.close()
