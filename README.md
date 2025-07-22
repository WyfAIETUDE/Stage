
# Projet Informatique - Gestion des Offres de Stage à l'Esigelec

## Auteurs
- Wu Yufan
- Zhang Shixu  
29/04/2024

## Table des Matières
1. [Introduction](#introduction)
2. [Spécifications et Conception](#spécifications-et-conception)
3. [Méthode de Résolution](#méthode-de-résolution)
4. [Conclusion](#conclusion)

## Introduction
Ce programme Python permet de gérer les offres de stages à l'Esigelec. Il offre deux interfaces principales :
- Pour les **entreprises** : création de comptes et publication d'offres
- Pour les **étudiants** : inscription et candidature aux offres

L'objectif est de faciliter la mise en relation entre entreprises et étudiants, et de simplifier le processus de candidature.

## Spécifications et Conception
Le système repose sur plusieurs fonctionnalités clés :

1. **Gestion des comptes**  
   - Stockage des informations via des dictionnaires/classes
   - Profils distincts pour entreprises et étudiants

2. **Gestion des offres**  
   - Liste/dictionnaire des offres associées aux entreprises
   - Système de candidatures pour chaque offre

3. **Notifications**  
   - Envoi d'acceptations/refus aux étudiants
   - Interface de gestion pour les entreprises

4. **Modifications**  
   - Mise à jour des informations profil
   - Gestion des offres et candidatures

5. **Persistance**  
   - Sauvegarde des données entre sessions

## Méthode de Résolution
L'application est structurée en 7 modules principaux :

### 1. Compte Entreprise
```python
def choose_user_company(self):
    self.user_type = 'company'
    self.btn_login.set_text('Connexion entreprise')
    self.btn_register.set_text('Inscription entreprise')
    self.frame_login.show_frame()
```

### 2. Gestion des Offres
```python
def view_topic(self):
    # Affiche les sujets de stage disponibles
```

### 3. Compte Étudiant
```python
def choose_user_student(self):
    self.user_type = 'student'
    self.btn_login.set_text('Connexion étudiant')
    self.btn_register.set_text('Inscription étudiant')
    self.frame_login.show_frame()
```

### 4. Modifications Entreprise
```python
def add_job(self):
    # Interface pour publier une nouvelle offre
    self.panel_job = CInputPanel(...)

def mod_job(self):
    # Modification d'une offre existante
    job_mgr.JobMgr().mod_company_job(...)
```

### 5. Fonctionnalités Étudiant
```python
def create_frame_student(self):
    # Interface complète avec :
    - Liste des offres
    - Boutons de candidature
    - Gestion des candidatures
    - Acceptation/refus de stages
```

### 6. Notifications
```python
def agree_apply(self):
    # Acceptation d'une candidature
    job_mgr.JobMgr().agree_student_apply(...)
    CDlg.show(content='Bien envoyé')

def disagree_apply(self):
    # Refus d'une candidature
    job_mgr.JobMgr().disagree_student_apply(...)
```

### 7. Candidatures Multiples
```python
def apply_job(self):
    # Gestion des restrictions :
    - 1 poste à la fois
    - Pas de doublons
    if res == 2:
        CDlg.show(content='Candidature réussie')
```

## Conclusion
Ce projet nous a permis de :
- Mettre en pratique les concepts Python avancés
- Gérer des structures de données complexes
- Concevoir une interface utilisateur complète

Bien que fonctionnel, le système pourrait être amélioré par :
- Une meilleure gestion des erreurs
- Des performances accrues
- Une interface plus intuitive

Ce projet représente une première étape vers le développement d'applications professionnelles.
