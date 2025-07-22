import tkinter.ttk
from tkinter import *
import user_mgr  # Importer le module de gestion des utilisateurs 
import job_mgr  # Importer le module de gestion des poste
import topic_mgr  # Importer le module de gestion des thèmes 


# Définir une classe de composant d'interface personnalisée 
class CWidget:
    def __init__(self, widget: Widget, pos: tuple, size: tuple, font: tuple, fg: str, bg: str) -> None:
#:paramètre widget: objet de classe standard de tkinter
#:paramètre pos: coordonnées absolues par rapport au coin supérieur gauche de la fenêtre, par exemple : (100, 100)
#:paramètre size: taille du composant (en pixels), par exemple : (100, 100)
#:paramètre font: police du texte, par exemple : ('Times New Roman', 15)
#:paramètre fg: couleur du premier plan, par exemple : "black"
#:paramètre bg: couleur de fond, par exemple : "white"
        self.widget = widget
        # Définir la largeur et la hauteur du composant 
        if size:
            if size[0] > 0: self.widget.place(width=size[0])
            if size[1] > 0: self.widget.place(height=size[1])
        # Définir la police du composant :
        if font:
            if type(widget) != Canvas and type(widget) != tkinter.ttk.Treeview: self.widget['font'] = font
            if type(widget) == OptionMenu: self.widget['menu'].config(font=font)
        # Définir la couleur du premier plan du composant 
        if fg and type(widget) != Canvas:
            self.widget['fg'] = fg
        # Définir la couleur de fond du composant 
        if bg:
            self.widget['bg'] = bg
        # Définir la position du composant :
        self.widget.place(x=pos[0], y=pos[1])

    #Créer une variable de chaîne de caractères 
    def gen_text_var(self) -> StringVar:
        self.text_var = StringVar()
        return self.text_var

    # Obtenir le contenu textuel du composant 
    def get_text(self) -> str:
        if type(self.widget) in [Entry]:
            return self.widget.get()
        elif type(self.widget) in [OptionMenu, Checkbutton, Radiobutton, Listbox]:
            return self.text_var.get()
        else:
            return self.widget['text']

    # Définir le contenu textuel du composant 
    def set_text(self, text: str) -> None:
        if type(self.widget) in [Entry]:
            self.widget.delete(0, 'end')
            self.widget.insert(0, text)
        elif type(self.widget) in [OptionMenu, Checkbutton, Radiobutton, Listbox]:
            self.text_var.set(text)
        else:
            self.widget['text'] = text

    # Définir si le composant est activé ou non
    def enabled(self, is_enable: bool) -> None:
        self.widget['state'] = NORMAL if is_enable else DISABLED

    # Définir la fonction de rappel pour l'événement de clic
    def click_call_back(self, call_back) -> None:
        self.widget['command'] = call_back

    # Ajouter un écouteur d'événement
    def add_listener(self, call_back, event_type='<ButtonPress-1>') -> None:
        self.widget.bind(event_type, call_back)


# Classe de cadre personnalisé
class CFrame(CWidget):
    #Le Cadre

    def __init__(self, master, pos=(0, 0), size=None, font=None, fg=None, bg=None, is_show=True):
        widget = Frame(master)
        super().__init__(widget, pos, size, font, fg, bg)
        self.pos = pos
        self.size = size
        if not is_show: self.hide_frame()

    # Obtenir l'objet du cadre
    def get(self):
        return self.widget

    # Afficher le cadre
    def show_frame(self):
        self.widget.place(x=self.pos[0], y=self.pos[1], width=self.size[0], height=self.size[1])

    # Masquer le cadre
    def hide_frame(self):
        self.widget.place_forget()


# Classe de balise de texte personnalisée
class CLabel(CWidget):
   #Étiquette de texte

    def __init__(self, master, pos, text, size=None, font=None, fg=None, bg=None):
        widget = Label(master, text=text)
        super().__init__(widget, pos, size, font, fg, bg)


# Classe de champ de saisie de texte personnalisée
class CEntry(CWidget):
    #Champ de saisie de texte

    def __init__(self, master, pos, size=None, font=None, fg=None, bg=None):
        widget = Entry(master, textvariable=self.gen_text_var())
        super().__init__(widget, pos, size, font, fg, bg)

    # Définir comme champ de saisie de mot de passe
    def set_as_password_entry(self):
       
       #Définir comme champ de saisie de mot de passe, où tous les caractères sont affichés comme des astérisques (*).
       #:return: Aucun
    
        # Afficher tous les textes du champ de saisie comme des étoiles
        self.widget['show'] = '*'


# Classe de bouton personnalisée
class CButton(CWidget):
       #les Boutons

    def __init__(self, master, pos, text, call_back=None, size=None, font=None, fg=None, bg=None):
        widget = Button(master, text=text)
        super().__init__(widget, pos, size, font, fg, bg)
        if call_back: self.click_call_back(call_back)


class CText(CWidget):
    #Boîte de texte enrichi à plusieurs lignes

    def __init__(self, master, pos, size=None, font=None, fg=None, bg=None):
        widget = Text(master)
        super().__init__(widget, pos, size, font, fg, bg)
        # 1.0 représente le premier caractère de la première ligne, c'est-à-dire le début de la zone de texte, 4.5 représente la position du cinquième caractère de la quatrième ligne. Note : les lignes commencent à 1 et les colonnes à 0.
        self.begin = '1.0'
        # END représente la fin de la zone de texte, c'est-à-dire la position finale
        self.end = END

    def delete_all_texts(self):
 
        
        #Effacer le contenu du champ de texte.
        #:return: Aucun

        self.widget.delete(self.begin, self.end)

    def get_text(self):

        #Obtenir le contenu du champ de texte.
        #:return: Chaîne de caractères

        res = self.widget.get(self.begin, self.end)
        if res == '\n': res = ''
        return res

    def set_text(self, txt):
       
        #Définir le contenu du champ de texte.
        #:paramètre txt: Chaîne de caractères cible.
        #:return: Aucun
     
        # delete
        self.delete_all_texts()
        # paramètre
        self.widget.insert(self.end, txt)


class CTreeView(CWidget):
    #【Le TreeView peut afficher une structure arborescente ou une structure de tableau par défaut, mais dans ce cas, nous l'avons encapsulé en une classe de tableau bidimensionnel.】

    def __init__(self, master, pos, size=None, font=None, fg=None, bg=None):
        widget = tkinter.ttk.Treeview(master, show='headings')  # show='headings' indique que le TreeView est configuré en mode tableau (plutôt qu'en structure arborescente)
        super().__init__(widget, pos, size, font, fg, bg)
        # Ajouter une barre de défilement
        self.xscroll = tkinter.ttk.Scrollbar(master, orient=HORIZONTAL, command=widget.xview)  # Barre de défilement horizontale
        self.yscroll = tkinter.ttk.Scrollbar(master, orient=VERTICAL, command=widget.yview)  # Barre de défilement verticale
        self.xscroll.place(x=pos[0], y=pos[1] + size[1], width=size[0])
        self.yscroll.place(x=pos[0] + size[0], y=pos[1], height=size[1])
        widget['xscrollcommand'] = self.xscroll.set
        widget['yscrollcommand'] = self.yscroll.set
        if font:
            style = tkinter.ttk.Style()
            style.configure("Treeview.Heading", font=font)  # Définir la police de l'en-tête du tableau
            style.configure("Treeview", font=font, rowheight=font[1] * 2)  # Définir la police du contenu du tableau, la hauteur de ligne est le double de la taille de la police

    def refresh(self, lst_header, lst_data, lst_col_width=None, anchor='w'):
     
      
        #Actualiser les données du tableau (en vidant d'abord le contenu du tableau, puis en affichant à nouveau le nouveau contenu).
        #Remarque : Les données sont affichées par défaut alignées à gauche. Vous pouvez modifier le paramètre "anchor" pour changer l'alignement.
        #:paramètre lst_header: Colonnes de titre (vous pouvez modifier le nombre de colonnes à tout moment).
        #:paramètre lst_data: Contenu des données du tableau. La longueur de chaque sous-liste doit correspondre au nombre de colonnes du titre.
        #:paramètre lst_col_width: Largeur de chaque colonne, par exemple : [100, 50, 60, 70]. Remarque : si la somme des largeurs de toutes les colonnes dépasse la largeur totale du tableau, les largeurs de chaque colonne seront automatiquement agrandies proportionnellement pour remplir le tableau.
        #:paramètre anchor: 'w' pour aligner à gauche, 'e' pour aligner à droite, 'center' pour aligner au centre.
     
        self.widget['columns'] = lst_header
        for idx, col in enumerate(self.widget['columns']):
            self.widget.heading(col, text=col, anchor=anchor)  # Afficher le texte à l'intérieur de l'en-tête du tableau en alignement à gauche
            if lst_col_width:
                self.widget.column(col, anchor=anchor, minwidth=lst_col_width[idx], width=lst_col_width[idx])
            else:
                self.widget.column(col, anchor=anchor)
        # Effacer le contenu du tableau
        for item in self.widget.get_children():
            self.widget.delete(item)
        # Ajouter une nouvelle ligne
        for row in lst_data:
            self.widget.insert('', END, values=row)

    def add_select_item_callback(self, call_back):
        
    
        #Ajouter une fonction de rappel lorsque certains éléments sont sélectionnés dans le tableau.
        #:paramètre call_back: La fonction de rappel, qui doit accepter un paramètre d'événement représentant l'objet d'événement.
        #:return: Aucun
        
        self.add_listener(call_back, '<<TreeviewSelect>>')

    def get_selected_items(self) -> list:
    
        #Obtenir la liste des index de tous les éléments sélectionnés (à partir de 0).
        #:return: Une liste. Si aucun élément n'est sélectionné, renvoie une liste vide.

        lst_idxs = []
        for idx, item in enumerate(self.widget.get_children()):
            if item in self.widget.selection():
                lst_idxs.append(idx)
        return lst_idxs

    def get_item(self, idx: int) -> list:
      
        #Obtenir la liste des données de l'élément spécifié à l'index donné.
        #:paramètre idx: index, à partir de 0
        #:return: liste des données de toutes les colonnes de l'élément spécifié

        return list(self.widget.item(self.widget.get_children()[idx], 'values'))


class CDlg:
    #【Boîte de dialogue】, comprenant 8 types de boîtes de dialogue + sélecteur de couleur + sélecteur de fichier + boîte de dialogue de saisie simple.

    @staticmethod
    def show(dlg_title='Indication', content='Contenu du texte'):
        from tkinter import messagebox
        # Renvoyer un type str : 'ok'
        return messagebox.showinfo(dlg_title, content)


class CInputPanel:

    #Fenêtre contextuelle pour l'ajout/modification d'informations, disposant d'un agencement automatique de tous les champs.






    def __init__(self, master, call_back, columns, default_values=None, title='', size=(350, 0), font=('Times New Roman', 12)):
        
        #:paramètre maître : objet de fenêtre parent
        #:paramètre call_back : fonction de rappel à exécuter lorsque l'utilisateur clique sur le bouton "OK" sur cette interface (toutes les valeurs seront renvoyées à cette fonction sous forme de liste)
        #:paramètre colonnes : liste des valeurs de champs nécessitant une saisie utilisateur
        #:paramètre valeurs_par_défaut : liste des valeurs par défaut (pour la fonctionnalité de remplissage automatique des informations lors de la modification)
        #:paramètre titre : titre de la fenêtre
        #:paramètre taille : taille de l'interface (si la hauteur est définie sur 0, elle sera automatiquement ajustée en fonction du nombre de champs)
        #:paramètre police : police de caractères
      
        self.root = Toplevel(master)
        if title:
            self.root.title(title)
        else:
            self.root.title('Modifier les informations' if default_values else 'Ajouter des informations')
        size = (size[0], size[1] if size[1] else 50 * len(columns))
        ox = int((self.root.winfo_screenwidth() - size[0]) / 2)
        oy = int((self.root.winfo_screenheight() - size[1]) / 2)
        self.root.geometry('{}x{}-{}+{}'.format(size[0], size[1], ox, oy))
        self.root.grab_set()
        # La touche ESC ferme l'interface (détruit)
        self.root.bind('<Escape>', lambda x: self.root.destroy())
        self.root.bind('<Return>', lambda x: self.on_click_ok_btn())
        self.call_back = call_back
        self.width, self.height = size[0], size[1]
        self.font = font
        self.columns = columns
        self.default_values = default_values
        self.create_widgets()

    def disable_entry(self, entry_idx):
        self.entrys[entry_idx]['state'] = DISABLED

    def show_tips(self, tips):
        from tkinter import messagebox
        tkinter.messagebox.showinfo('Indication', tips)
        self.root.lift()

    def destroy(self):
        #Casser la fenêtre
        self.root.destroy()

    def on_click_ok_btn(self):
        
        #Si l'utilisateur clique sur le bouton "OK" sur cette interface.
     
        #Cette interface détecte automatiquement si une valeur de champ est manquante. Si c'est le cas, une boîte de dialogue s'affiche pour informer l'utilisateur
        for col_name, entry in zip(self.columns, self.entrys):
            if not entry.get().strip():
                self.show_tips(f' Veuillez entrez:{col_name}')
                return
        # Appeler la fonction de rappel et retourner toutes les valeurs de champ entrées par l'utilisateur sous forme de liste 
        self.call_back([x.get() for x in self.entrys])

    def create_widgets(self, ox=20, rate=1.2, height=30, gap_of_btns=25):
    
       
        #Créer tous les contrôles de libellé, de zone de texte et de bouton.
        #:param ox: Valeur en pixels entre le contrôle et les bords latéraux de la fenêtre
        #:param rate: Ratio de largeur entre la zone de texte et le libellé. Plus ce nombre est grand, plus la zone de texte est large et le libellé est étroit
        #:param height: Hauteur du contrôle
        #:param gap_of_btns: Valeur d'espace entre deux boutons
        # Calculer la largeur et la hauteur du Label
        w_label, h_label = (self.width - ox * 2) // (1 + rate), height
        # Calculer la largeur et la hauteur du Entry
        w_entry, h_entry = w_label * rate, h_label - 4
        # Calculer la largeur et la hauteur du Button
        w_btn, h_btn = (self.width - ox * 2 - gap_of_btns) // 2, height
        # Calculer l'espace entre chaque contrôle sur la ligne
        gap = (self.height - ox * 2 - h_label * len(self.columns) - h_btn) / len(self.columns)
        self.entrys = []
        for idx, col_name in enumerate(self.columns):
            lbl = Label(self.root, text=f'{col_name}：', font=self.font, anchor='w')
            lbl.place(x=ox, y=ox + idx * (h_label + gap), width=w_label, height=h_label)
            entry = Entry(self.root, font=self.font)
            entry.place(x=ox + w_label, y=ox + idx * (h_label + gap), width=w_entry, height=h_entry)
            entry.delete(0, 'end')
            entry.insert(0, self.default_values[idx] if self.default_values else "")
            self.entrys.append(entry)
        btn_back = Button(self.root, text='Retour', font=self.font, command=self.destroy)
        btn_back.place(x=ox, y=ox + len(self.columns) * (h_label + gap), width=w_btn, height=h_btn)
        btn_ok = Button(self.root, text='Confirmer', font=self.font, command=self.on_click_ok_btn)
        btn_ok.place(x=ox + w_btn + gap_of_btns, y=ox + len(self.columns) * (h_label + gap), width=w_btn, height=h_btn)


# Définir une classe d'application
class App:
    def __init__(self, title, width, height):
        # Créer une fenêtre
        self.root = Tk()
        # Définir le titre
        self.root.title(title)
        # Calculer la marge à gauche de la fenêtre pour qu'elle s'affiche centrée par rapport à l'écran
        offset_x = int((self.root.winfo_screenwidth() - width) / 2)
        # Calculer la marge en haut de la fenêtre pour qu'elle s'affiche centrée par rapport à l'écran
        offset_y = int((self.root.winfo_screenheight() - height) / 2)
        # Définir la taille et la position de la fenêtre
        self.root.geometry('{}x{}-{}+{}'.format(width, height, offset_x, offset_y))
        # Créer un cadre d'interface de démarrage
        self.frame_start = CFrame(self.root, size=(1280, 800), is_show=True)
        # Créer un cadre d'interface de connexion
        self.frame_login = CFrame(self.root, size=(1280, 800), is_show=False)
        # Créer un cadre d'interface d'entreprise
        self.frame_company = CFrame(self.root, size=(1280, 800), is_show=False)
        # Créer un cadre d'interface étudiant
        self.frame_student = CFrame(self.root, size=(1280, 800), is_show=False)
        # Ajouter un composant personnalisé
        self.run()
        # Démarrer la boucle principale
        self.root.mainloop()

    # Sélectionner la connexion en tant qu'utilisateur d'entreprise 
    def choose_user_company(self):
        self.user_type = 'company'
        self.btn_login.set_text('Connexion en tant que utilisateur de entreprise')
        self.btn_register.set_text('Inscription en tant que utilisateur de entreprise')
        self.frame_login.show_frame()

    # Sélectionner la connexion en tant qu'utilisateur étudiant
    def choose_user_student(self):
        self.user_type = 'student'
        self.btn_login.set_text('Connexion en tant que utilisateur de élève')
        self.btn_register.set_text('Inscription en tant que utilisateur de élève')
        self.frame_login.show_frame()

    # Quitter l'application
    def exit_app(self):
        self.root.destroy()

    # Créer un cadre d'interface de démarrage
    def create_frame_start(self):
        # Dans le cadre de l'interface de démarrage, ajouter un titre
        CLabel(self.frame_start.get(), (0, 50), "Système de gestion des stages à l'ESIGELEC", (1280, 120), self.font_title)
        #Dans le cadre de l'interface de démarrage, ajouter un bouton : "Connexion utilisateur d'entreprise"
        CButton(self.frame_start.get(), (490, 300), "Connectez-vous en tant qu'utilisateur d'entreprise", self.choose_user_company, (320, 55), self.font1)
        # Dans le cadre de l'interface de démarrage, ajouter un bouton : "Connexion utilisateur étudiant"
        CButton(self.frame_start.get(), (490, 400), "Connectez-vous en tant qu'utilisateur d'étudiant", self.choose_user_student, (320, 55), self.font1)
        # Dans le cadre de l'interface de démarrage, ajouter un bouton : "Quitter le système"
        CButton(self.frame_start.get(), (490, 500), "Déconnectez-vous du système", self.exit_app, (320, 55), self.font1)

    # La logique de connexion de l'utilisateur
    def user_login(self):
        # Créer un objet gestionnaire d'utilisateurs
        mgr = user_mgr.UserMgr()
        # Charger les données des utilisateurs
        dct = mgr.load_users(self.user_type)
        #Obtenir le nom d'utilisateur et le mot de passe saisis par l'utilisateur
        act = self.entry_act.get_text()
        pwd = self.entry_pwd.get_text()
        # Si le compte existe
        if act in dct:
            # Si le mot de passe est correcte
            if dct[act][1] == pwd:
                # Enregistrer les données de l'utilisateur
                self.user_data = dct[act]
                print("Les données de connexion de l'utilisateur：")
                print(self.user_data)
                #Afficher l'interface correspondante en fonction du type d'utilisateur.entre ou etudiant
                if self.user_type == 'company':
                    self.frame_company.show_frame()
                    self.refresh_grid_company_job()
                    self.refresh_grid_company_apply()
                else:
                    self.frame_student.show_frame()
                    self.refresh_grid_student_job()
                    self.refresh_grid_student_apply()
                    self.check_refused_jobs()
                    self.refresh_grid_student_apply()
            else:
                #Afficher une boîte de dialogue pour signaler une erreur de mot de passe.
                CDlg.show(content='Mot de passe incorrect. Veuillez réessayer')
        else:
            # Afficher une boîte de dialogue pour signaler que le compte n'existe pas
            CDlg.show(content="Le compte n'existe pas. Veuillez vous inscrire d abord")

    # La logique d'inscription des utilisateurs
    def _user_register(self, values):
        # Créer un objet gestionnaire d'utilisateurs.
        mgr = user_mgr.UserMgr()
        # Charger les données des utilisateurs
        dct = mgr.load_users(self.user_type)
        # Si l'utilisateur est un utilisateur d'entreprise et que le nom de l'entreprise existe déjà
        if self.user_type == 'company' and mgr.is_company_exists(values[2]):
            # Afficher une notification indiquant que le nom de l'entreprise est déjà utilisé
            self.panel_register.show_tips("Le nom de l'entreprise ne peut pas être répété. Veuillez saisir un nouveau nom.")
        else:
            # Si le compte existe déjà
            if values[0] in dct:
                # Afficher une notification indiquant que le compte a déjà été enregistré
                self.panel_register.show_tips("Ce compte a déjà été enregistré par un autre utilisateur")
            else:
                # Ajouter les informations de l'utilisateur aux données des utilisateurs
                dct[values[0]] = values
                #Enregistrer les données de l'utilisateur
                mgr.save_users(self.user_type, dct)
                # Fermer le panneau d'inscription
                self.panel_register.destroy()
                # Afficher une boîte de dialogue pour indiquer que l'inscription a réussi
                CDlg.show(content="Inscription réussie")

    #  l'inscription de l'utilisateur
    def user_register(self):
        # Créer des panneaux d'inscription différents en fonction du type d'utilisateur (etudiant ou entreprise)
        if self.user_type == 'company':
            self.panel_register = CInputPanel(self.frame_login.get(), self._user_register,
                                              ["Nom d'utilisateur", 'Mot de passe', "Nom de l'entreprise", "Adresse du l'entreprise", "Domaine d'activité"],
                                              title="Inscription en tant que utilisateur d'entreprise", font=self.font1)
        else:
            self.panel_register = CInputPanel(self.frame_login.get(), self._user_register,
                                              ["Nom d'utilisateur", "Mot de passe", "Nom de l'élève", 'Sexe', 'Age', "Nom de l'école ou l'université", 'Specialité'],
                                              title="Inscription en tant qu'utilisateur de élève", font=self.font1)

    #Retour à l'interface de départ
    def back_to_start(self):
        self.entry_act.set_text('')
        self.entry_pwd.set_text('')
        self.frame_login.hide_frame()

    # créer un cadre de page de connexion
    def create_frame_login(self):
        #  ajouter un titre dans un cadre de la page de connexion 
        CLabel(self.frame_login.get(), (0, 50), "Système de gestion des stages à l'ESIGELEC", (1280, 120), self.font_title)
        # Ajoutez des étiquettes pour le nom d'utilisateur et le mot de passe dans le cadre de l'interface de connexion
        CLabel(self.frame_login.get(), (400, 260), "Nom d'utilisateur：", (150, 40), self.font1)
        CLabel(self.frame_login.get(), (400, 330), "Mot de passe：", (150, 40), self.font1)
        # Ajoutez des champs de saisie pour le nom d'utilisateur et le mot de passe dans le cadre de l'interface de connexion.
        self.entry_act = CEntry(self.frame_login.get(), (530, 260), (280, 30), self.font1)
        self.entry_pwd = CEntry(self.frame_login.get(), (530, 330), (280, 30), self.font1)
        self.entry_pwd.set_as_password_entry()
        # Ajoutez des boutons de connexion et d'inscription dans le cadre de l'interface de connexion.
        self.btn_login = CButton(self.frame_login.get(), (470, 420), "", self.user_login, (320, 47), self.font1)
        self.btn_register = CButton(self.frame_login.get(), (470, 500), "", self.user_register, (320, 47), self.font1)
        # Ajoutez un bouton de retour dans le cadre de l'interface de connexion.
        CButton(self.frame_login.get(), (470, 580), "Retour", self.back_to_start, (320, 47), self.font1)

    #La logique de publication des offres d'emploi 
    def _add_job(self, values):
        mgr = job_mgr.JobMgr()
        # Si l'entreprise a déjà publié un poste similaire.
        if mgr.is_company_job_exists(self.user_data[2], values[0]):
            # Afficher un message d'erreur indiquant que le nom du poste est en double
            self.panel_job.show_tips('Le nom du poste ne peut pas être répété. Veuillez saisir à nouveau.')
        else:
            # Créer de nouvelles informations sur le poste.
            job = [self.user_data[2], values[0], values[1], values[2], 0, '', []]  # here
            # Ajouter des informations sur le poste.
            mgr.add_job(job)
            # Fermez le panneau de publication des offres d'emploi.
            self.panel_job.destroy()
            #Actualisez la liste des postes de l'entreprise.
            self.refresh_grid_company_job()
            # Afficher un message indiquant que la publication a réussi
            CDlg.show(content='La publication du poste a été réussie !')

    # Publier une offre d'emploi
    def add_job(self):
        # Afficher le panneau de publication d'offres d'emploi
        self.panel_job = CInputPanel(self.frame_company.get(), self._add_job, [' Le nom du poste', 'Salaire', 'Compétences requises'],
                                     title='Publier une offre d emploi', size=(350, 250), font=self.font1)

    # supprimer une offre d'emploi
    def del_job(self):
        idxs = self.grid_company_job.get_selected_items()
        if idxs:
            item = self.grid_company_job.get_item(idxs[0])
            company_name, job_name = item[0], item[1]
            # supprimer l'offre d'emploi sélectionnée
            job_mgr.JobMgr().del_company_job(company_name, job_name)
            # Actualiser la liste des postes de l'entreprise
            self.refresh_grid_company_job()
        else:
            # Rappeler à l'utilisateur de choisir un poste
            CDlg.show(content='Veuillez sélectionner le poste à supprimer dans la liste.')

    # modifier l'offre d'emploi
    def _mod_job(self, values):
        job_mgr.JobMgr().mod_company_job(self.cur_sel_company_name, self.cur_sel_job_name, values)
        self.refresh_grid_company_job()
        self.panel_job.destroy()

    # modifier l'offre d'emploi
    def mod_job(self):
        idxs = self.grid_company_job.get_selected_items()
        if idxs:
            item = self.grid_company_job.get_item(idxs[0])
            values = [item[1], item[2], item[3]]
            # Afficher le panneau de modification de l'offre d'emploi
            self.panel_job = CInputPanel(self.frame_company.get(), self._mod_job,
                                         ['Nom du poste', 'Salarié', 'Compétences requises'], values, title="Modifier l'offre d'emploi",
                                         size=(350, 250), font=self.font1)
        else:
            # Rappeler à l'utilisateur de choisir un poste
            CDlg.show(content='Veuillez sélectionner le poste à supprimer dans la liste')

    # publier un sujet de stage
    def post_topic(self):
        topic = self.entry_topic.get_text()
        content = self.entry_content.get_text()
        dct_topics = topic_mgr.TopicMgr().load_topics()
        k = self.user_data[2]
        v = (topic, content)
        dct_topics[k] = v
        topic_mgr.TopicMgr().save_topics(dct_topics)
        CDlg.show(content='Publication réussie !')
        self.entry_topic.set_text('')
        self.entry_content.set_text('')

    # Retour à la page de connexion
    def back_to_login(self):
        self.entry_act.set_text('')
        self.entry_pwd.set_text('')
        self.cur_sel_company_name = None
        self.cur_sel_job_name = None
        self.frame_company.hide_frame()
        self.frame_student.hide_frame()

    # Actualiser la liste des postes de l'entreprise
    def refresh_grid_company_job(self, is_reset=False):
        if is_reset:
            self.grid_company_job.refresh(self.lst_header_job, [])
        else:
            lst_jobs = job_mgr.JobMgr().get_company_jobs(self.user_data[2])
            lst_data = []
            for l in lst_jobs:
                lst_data.append([l[0], l[1], l[2], l[3], len(l[-1])])
            self.grid_company_job.refresh(self.lst_header_job, lst_data)

    # Actualiser la liste des candidatures pour les postes de l'entreprise
    def refresh_grid_company_apply(self, is_reset=False):
        if is_reset:
            self.grid_company_apply.refresh(self.lst_header_company_apply, [],
                                            [130] * len(self.lst_header_company_apply))
        else:
            lst = job_mgr.JobMgr().get_job_apply_students(self.cur_sel_company_name, self.cur_sel_job_name)
            lst_data = []
            for l in lst:
                lst_data.append([self.cur_sel_company_name, self.cur_sel_job_name, *l[2:]])
            self.grid_company_apply.refresh(self.lst_header_company_apply, lst_data,
                                            [130] * len(self.lst_header_company_apply))
            self.btn_company_disagree.enabled(
                job_mgr.JobMgr().get_job_state(self.cur_sel_company_name, self.cur_sel_job_name) == 0)
            self.btn_company_agree.enabled(
                job_mgr.JobMgr().get_job_state(self.cur_sel_company_name, self.cur_sel_job_name) == 0)

    # Logique de modification des informations utilisateur
    def _user_mod_info(self, values):
        mgr = user_mgr.UserMgr()
        dct = mgr.load_users(self.user_type)
        if self.user_type == 'company' and mgr.is_company_exists(values[2], values[0]):
            self.panel_register.show_tips("Le nom de l'entreprise ne peut pas être répété, veuillez saisir à nouveau.")
        else:
            dct[values[0]] = values
            mgr.save_users(self.user_type, dct)
            self.panel_register.destroy()
            self.user_data = values
            CDlg.show(content="Modification réussie")

    # modifier les informations de l'utilisateur
    def user_mod_info(self):
        values = self.user_data
        self.panel_register = CInputPanel(self.frame_company.get(), self._user_mod_info,
                                          ['Nom de utilisateur', 'Mot de passe', "Nom de L'entreprise", "Adresse du l'entreprise", "Domaine d'activité"], values,
                                          title="Modifier les informations de l'entreprise", font=self.font1)
        self.panel_register.disable_entry(0)
        self.panel_register.disable_entry(1)

    # Retour d'appel après sélection d'un poste d'entreprise
    def on_click_grid_company_job_item(self, event):
        idxs = self.grid_company_job.get_selected_items()
        if idxs:
            item = self.grid_company_job.get_item(idxs[0])
            self.cur_sel_company_name = item[0]
            self.cur_sel_job_name = item[1]
            self.refresh_grid_company_apply()

    # Logique de refus de candidature
    def disagree_apply(self):
        idxs = self.grid_company_apply.get_selected_items()
        if idxs:
            item = self.grid_company_apply.get_item(idxs[0])
            job_mgr.JobMgr().disagree_student_apply(item[0], item[1], idxs[0])
            self.refresh_grid_company_job()
            self.refresh_grid_company_apply()
        else:
            CDlg.show(content="Veuillez sélectionner l'élément de candidature à refuser dans la liste")

    # Logique d'approbation de candidature
    def agree_apply(self):
        idxs = self.grid_company_apply.get_selected_items()
        if idxs:
            item = self.grid_company_apply.get_item(idxs[0])
            job_mgr.JobMgr().agree_student_apply(item[0], item[1], idxs[0])
            self.refresh_grid_company_apply()
            CDlg.show(content='Envoyé avec succès')
        else:
            CDlg.show(content="Veuillez sélectionner l'élément de candidature à approuver dans la liste.")

    #Créer une interface d'entreprise
    def create_frame_company(self):
        # Créer une liste de postes d'entreprise
        self.grid_company_job = CTreeView(self.frame_company.get(), (20, 20), (930, 420))
        self.grid_company_job.add_select_item_callback(self.on_click_grid_company_job_item)
        # Ajouter des éléments à l'interface de l'entreprise
        CLabel(self.frame_company.get(), (20, 465), 'Liste des candidats pour le poste：', (200, 30), self.font1)
        self.grid_company_apply = CTreeView(self.frame_company.get(), (20, 500), (930, 220))
        self.btn_company_disagree = CButton(self.frame_company.get(), (130, 740), 'Refuser cette candidature', self.disagree_apply,
                                            (250, 40), self.font1)
        self.btn_company_agree = CButton(self.frame_company.get(), (530, 740), 'Accepter et envoyer une invitation de stage', self.agree_apply,
                                         (250, 40), self.font1)
        # Ajouter des boutons et des étiquettes
        CButton(self.frame_company.get(), (990, 40), "Publier une offre d'emploi", self.add_job, (250, 40), self.font1)
        CButton(self.frame_company.get(), (990, 110), "Supprimer une offre d'emploi", self.del_job, (250, 40), self.font1)
        CButton(self.frame_company.get(), (990, 180), "Modifier une offre d'emploi", self.mod_job, (250, 40), self.font1)
        CButton(self.frame_company.get(), (990, 250), "Modifier les informations de l'entreprise", self.user_mod_info, (250, 40), self.font1)
        CButton(self.frame_company.get(), (990, 320), 'Déconnexion', self.back_to_login, (250, 40), self.font1)
        CLabel(self.frame_company.get(), (970, 400), 'Publier le sujet de stage：', (180, 40), self.font1)
        CLabel(self.frame_company.get(), (985, 460), 'Le sujet:', (60, 30), self.font1)
        # Ajouter des champs de saisie et des boutons
        self.entry_topic = CEntry(self.frame_company.get(), (1050, 460), (190, 28), self.font1)
        CLabel(self.frame_company.get(), (990, 510), 'Le contenu：', (80, 30), self.font1)
        self.entry_content = CText(self.frame_company.get(), (1000, 560), (240, 150), self.font1)
        CButton(self.frame_company.get(), (995, 725), 'Publier maintenant', self.post_topic, (245, 40), self.font1)

    # Actualiser la liste des postes pour les étudiants
    def refresh_grid_student_job(self, is_reset=False):
        if is_reset:
            self.grid_student_job.refresh(self.lst_header_job, [])
        else:
            lst_jobs = job_mgr.JobMgr().load_jobs()
            lst_data = []
            for l in lst_jobs:
                lst_data.append([l[0], l[1], l[2], l[3], len(l[-1])])
            self.grid_student_job.refresh(self.lst_header_job, lst_data)

    # Actualiser la liste des candidatures des étudiants
    def refresh_grid_student_apply(self, is_reset=False):
        if is_reset:
            self.grid_student_apply.refresh(self.lst_header_company_apply, [],
                                            [130] * len(self.lst_header_company_apply))
        else:
            lst = job_mgr.JobMgr().get_student_apply_jobs(self.user_data[0])
            self.grid_student_apply.refresh(self.lst_header_company_apply, lst,
                                            [130] * len(self.lst_header_company_apply))

    # Méthode pour postuler à un poste
    def apply_job(self):
        # "Obtenir les informations sur les postes où les étudiants ont déjà été embauchés
        my_job = job_mgr.JobMgr().get_my_job(self.user_data[0])
        # Si l'étudiant a déjà été embauché pour un poste, indiquer qu'il ne peut pas postuler à d'autres postes
        if my_job:
            CDlg.show(content="Vous avez été embauché chez {} pour le poste de {} ， Vous ne pouvez pas postuler à d'autres postes pour le moment".format(my_job[0], my_job[1]))
            return

        # Obtenir les informations du poste sélectionné
        idxs = self.grid_student_job.get_selected_items()
        if idxs:
            item = self.grid_student_job.get_item(idxs[0])
            # Soumettre une candidature au gestionnaire de poste
            res = job_mgr.JobMgr().apply_job(item[0], item[1], self.user_data)
            if res == 2:
                # Actualiser la liste des postes pour les étudiants et la liste des candidatures
                self.refresh_grid_student_job()
                self.refresh_grid_student_apply()
                CDlg.show(content='Vous avez réussi à postuler chez{} pour le poste de{}'.format(item[0], item[1]))
            elif res == 1:
                CDlg.show(content="La candidature a échoué, on ne peut postuler qu'une seule fois pour un même poste")
            elif res == 0:
                CDlg.show(content='La candidature a échoué, le poste est déjà expiré')
        else:
            CDlg.show(content='Veuillez sélectionner le poste que vous souhaitez postuler dans la liste')

    # Méthode pour consulter les informations de l'entreprise
    def view_company_info(self):
        # Obtenir les informations sur le poste où l'étudiant a déjà été embauché
        my_job = job_mgr.JobMgr().get_my_job(self.user_data[0])
        if my_job:
            # Si embauché, afficher les informations de l'entreprise
            content = "Nom de l'entreprise :{}\nNom du poste :{}\nSalaire : {}\nCompétences requises : {}".format(*my_job[:4])
        else:
            content = 'Pas encore embauché dans une entreprise！'
        # Afficher la boîte de dialogue
        CDlg.show(dlg_title="Informations sur l'entreprise", content=content)

    # Consulter le sujet de stage
    def view_topic(self):
        # Obtenir les informations sur le poste où l'étudiant a déjà été embauché
        my_job = job_mgr.JobMgr().get_my_job(self.user_data[0])
        if my_job:
            k = my_job[0]
            # Obtenir le dictionnaire des sujets de stage
            dct = topic_mgr.TopicMgr().load_topics()
            if k in dct:
                # Si l'entreprise a publié un sujet de stage, afficher les informations sur le sujet de stage
                CDlg.show(dlg_title='Sujet de stage', content='Sujet de stage： {}\nContenu du stage：\n{}'.format(*dct[k]))
            else:
                CDlg.show(content="L'entreprise n'a pas encore publié de sujet de stage")
        else:
            CDlg.show(content="Vous n'avez pas encore été embauché dans une entreprise ！")

    # Méthode pour annuler une candidature
    def undo_apply(self):
        if self.grid_student_apply.get_selected_items():
            # Obtenez les informations de demande sélectionnées, révoquez la demande et actualisez la liste
            job_mgr.JobMgr().undo_apply(self.user_data[0], self.cur_sel_company_name, self.cur_sel_job_name)
            self.refresh_grid_student_job()
            self.refresh_grid_student_apply()
        else:
            CDlg.show(content='Veuillez sélectionner la demande à révoquer dans la liste')

    # Approche pour accepter un stage
    def agree_job(self):
        #Accepter le stage, supprimer toutes les demandes, rafraîchir la liste des demandes et désactiver le bouton
        job_mgr.JobMgr().agree_job(self.cur_sel_company_name, self.cur_sel_job_name)
        job_mgr.JobMgr().del_all_apply(self.user_data[0])
        self.refresh_grid_student_apply()
        self.btn_student_disagree.enabled(False)
        self.btn_student_agree.enabled(False)
        CDlg.show(content='Félicitations pour avoir réussi chez {} à décrocher le poste de {}！'.format(self.cur_sel_company_name, self.cur_sel_job_name))

    # Approche pour refuser un stage
    def disagree_job(self):
        # Refuser le stage, actualiser la liste des demandes et désactiver le bouton
        job_mgr.JobMgr().disagree_job(self.cur_sel_company_name, self.cur_sel_job_name, self.user_data[0])
        self.refresh_grid_student_apply()
        self.btn_student_disagree.enabled(False)
        self.btn_student_agree.enabled(False)
        CDlg.show(content='Vous avez refuser la demande du poste de {} chez {}'.format(self.cur_sel_company_name, self.cur_sel_job_name))

    # La méthode de rappel pour cliquer sur un élément de la liste des demandes des étudiants
    def on_click_grid_student_apply_item(self, event):
        idxs = self.grid_student_apply.get_selected_items()
        if idxs:
            item = self.grid_student_apply.get_item(idxs[0])
            # Obtenez le nom de l'entreprise et du poste actuellement sélectionnés, puis déterminez si vous pouvez accepter le stage
            self.cur_sel_company_name = item[0]
            self.cur_sel_job_name = item[1]
            is_enable = job_mgr.JobMgr().is_company_agree_my_apply(item[0], item[1], self.user_data[0])
            self.btn_student_disagree.enabled(is_enable)
            self.btn_student_agree.enabled(is_enable)

    def check_refused_jobs(self):
        lst = job_mgr.JobMgr().get_my_refused_apply(self.user_data[0])
        for job in lst:
            CDlg.show(content="Désolé，Votre demande de stage pour le poste de {} chez {} a été refusée！".format(job[0], job[1]))

    #Créer l'interface étudiante
    def create_frame_student(self):
        # Créez une liste de postes pour les étudiants, définissez sa position et sa taille.
        self.grid_student_job = CTreeView(self.frame_student.get(), (20, 20), (930, 470))
        # Ajoutez un bouton "Postuler pour un poste", définissez sa position, son texte, son événement de clic et sa taille.
        CButton(self.frame_student.get(), (990, 40), 'Postuler pour un poste', self.apply_job, (250, 40), self.font1)
        # Ajoutez un bouton "Voir les informations de l'entreprise", définissez sa position, son texte, son événement de clic et sa taille.
        CButton(self.frame_student.get(), (990, 120), "Voir les informations de l'entreprise", self.view_company_info, (250, 40), self.font1)
        # Ajoutez un bouton "Voir les sujets de stage de l'entreprise", définissez sa position, son texte, son événement de clic et sa taille.
        CButton(self.frame_student.get(), (990, 200), "Voir les sujets de stage de l'entreprise", self.view_topic, (250, 40), self.font1)
        # Ajoutez un bouton "Déconnexion", définissez sa position, son texte, son événement de clic et sa taille.
        CButton(self.frame_student.get(), (990, 280), 'Déconnection', self.back_to_login, (250, 40), self.font1)
        # Ajoutez une étiquette "Postes auxquels j'ai postulé", définissez sa position, son texte et sa taille.
        CLabel(self.frame_student.get(), (10, 510), "Postes auxquels j'ai postulé:", (190, 25), self.font1)
        # Créez une liste des demandes d'étudiants, puis définissez sa position et sa taille.
        self.grid_student_apply = CTreeView(self.frame_student.get(), (20, 540), (930, 230))
        # Ajoutez une fonction de rappel pour sélectionner un élément de la liste des demandes.
        self.grid_student_apply.add_select_item_callback(self.on_click_grid_student_apply_item)
        #Ajoutez un bouton "Révoquer la demande", définissez sa position, son texte, son événement de clic et sa taille.
        CButton(self.frame_student.get(), (990, 560), 'Révoquer la demande', self.undo_apply, (250, 40), self.font1)
        # Créez un bouton "Accepter le stage", définissez sa position, son texte, son événement de clic et sa taille.
        self.btn_student_agree = CButton(self.frame_student.get(), (990, 625), 'Accepter le stage', self.agree_job, (250, 40),
                                         self.font1)
        # Créez un bouton "Refuser le stage", définissez sa position, son texte, son événement de clic et sa taille.
        self.btn_student_disagree = CButton(self.frame_student.get(), (990, 690), 'Refuser le stage', self.disagree_job,
                                            (250, 40), self.font1)

    # initialement
    def init(self):
        #Définir le style de police des titres
        self.font_title = ('Times New Roman', 40, 'bold')
        # Définir le style de police général.
        self.font1 = ('Times New Roman', 10)
        # Initialiser le type d'utilisateur à None.
        self.user_type = None
        # Initialiser les données utilisateur à None.
        self.user_data = None
        # Initialiser les noms de l entreprise à None.
        self.cur_sel_company_name = None
        #Initialiser le nom du poste actuellement sélectionné à None.
        self.cur_sel_job_name = None
        # Définir les noms de colonnes pour la liste des postes d'étudiants.
        self.lst_header_job = ["Nom de l'entreprise", 'Nom du poste', 'Salarié', 'Compétences requises', 'Nombre de candidatures']
        # Méthode de définir les noms des colonnes de la liste des candidatures des étudiants
        self.lst_header_company_apply = ["Nom de l'entreprise", 'Nom du poste', 'Nom du candidat', 'Sexe', 'Age', "Nom de l'école ou université", 'Spécialité']
        # Initialiser la liste des postes avec une liste vide
        self.lst_jobs = []

    # Exécuter la méthode
    def run(self):
        # initialement
        self.init()
        # Créer l'interface de démarrage
        self.create_frame_start()
        # Créer l'interface de connexion
        self.create_frame_login()
        # Créer l'interface de l'entreprise
        self.create_frame_company()
        # Créer l'interface de l'étudiant
        self.create_frame_student()


if __name__ == '__main__':
    app = App("Système de gestion des stages à l'ESIGELEC", 1280, 800)
