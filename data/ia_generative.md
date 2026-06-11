# L'IA générative

> Document pédagogique de démonstration. Contenu fictif et généraliste.

## 1. Qu'est-ce que l'IA générative ?

L'IA générative désigne les systèmes capables de **produire** de nouveaux
contenus — texte, images, audio, code — plutôt que de seulement classer ou
prédire. Les grands modèles de langage (LLM) en sont l'exemple le plus connu :
ils génèrent du texte cohérent en réponse à une consigne. Ces modèles sont
entraînés sur de très grandes quantités de textes et apprennent les régularités
statistiques du langage.

## 2. Fonctionnement général d'un modèle de langage

Un modèle de langage prédit le prochain élément de texte le plus probable, compte
tenu de ce qui précède. En répétant cette prédiction, il génère des phrases
entières. Il ne « comprend » pas au sens humain : il modélise des probabilités
apprises sur ses données d'entraînement. La qualité du résultat dépend du modèle,
de la consigne fournie et du contexte disponible.

## 3. Notion de token

Un **token** est l'unité de base manipulée par le modèle. Il peut s'agir d'un
mot, d'une partie de mot ou d'un signe de ponctuation. Le texte est découpé en
tokens avant d'être traité. Le coût et la vitesse d'un modèle, ainsi que la
quantité de texte qu'il peut traiter, se mesurent souvent en nombre de tokens.

## 4. Notion de contexte

Le **contexte** est l'ensemble des informations fournies au modèle au moment de
la génération : la consigne, l'historique de la conversation et, le cas échéant,
des documents ajoutés. La **fenêtre de contexte** désigne la quantité maximale de
tokens que le modèle peut prendre en compte simultanément. Un contexte pertinent
et bien organisé améliore nettement la qualité des réponses.

## 5. Moteur de recherche classique ou modèle génératif ?

Un moteur de recherche classique renvoie une liste de documents ou de liens
correspondant à des mots-clés ; c'est à l'utilisateur de lire et de synthétiser.
Un modèle génératif, lui, produit directement une réponse rédigée. L'inconvénient
est qu'un modèle seul peut inventer des informations. C'est pourquoi on le couple
souvent à une recherche documentaire (RAG) pour ancrer ses réponses dans des
sources réelles.

## 6. Usages courants

- **Résumé automatique** : condenser un long document en quelques points clés.
- **Génération de texte** : rédiger des brouillons, des e-mails, des descriptions.
- **Assistant de code** : proposer, expliquer ou corriger du code.
- **Chatbot** : dialoguer et répondre à des questions en langage naturel.
- **Extraction d'informations** : repérer des entités, des dates, des montants
  dans un texte non structuré.

## 7. Risques et points de vigilance

- **Hallucinations** : le modèle peut produire des informations fausses mais
  formulées avec assurance.
- **Biais** : il peut reproduire des biais présents dans ses données
  d'entraînement.
- **Réponses non vérifiées** : sans sources, il est difficile de contrôler
  l'exactitude.
- **Données sensibles** : il ne faut pas transmettre de secrets ou de données
  personnelles à un service non maîtrisé.

## 8. Bonnes pratiques d'utilisation

- Formuler des consignes claires et précises.
- Fournir le contexte nécessaire et, si possible, des documents de référence.
- Demander au modèle de citer ses sources lorsqu'il s'appuie sur des documents.
- Vérifier les informations importantes plutôt que de les accepter telles quelles.
- Éviter de transmettre des données confidentielles.

## 9. Lien entre IA générative et RAG

Le RAG (génération augmentée par la récupération) combine un modèle génératif
avec une recherche documentaire. Avant de répondre, le système retrouve les
passages pertinents dans une base de connaissances et les fournit au modèle comme
contexte. Le modèle s'appuie alors sur ces passages pour produire une réponse
factuelle et sourcée. Le RAG réduit ainsi les hallucinations et permet de mettre
à jour les connaissances sans réentraîner le modèle.
