# Introduction à l'intelligence artificielle

> Document pédagogique de démonstration. Contenu fictif et généraliste, sans
> données personnelles ni informations confidentielles.

## 1. Qu'est-ce que l'intelligence artificielle ?

L'intelligence artificielle (IA) désigne l'ensemble des techniques permettant à
une machine d'effectuer des tâches qui requièrent habituellement l'intelligence
humaine : comprendre du langage, reconnaître des images, prendre des décisions
ou faire des prédictions. Plutôt qu'une définition unique, l'IA regroupe un
ensemble de méthodes et de modèles capables d'apprendre à partir de données ou
de raisonner à partir de règles.

## 2. IA, machine learning et deep learning

Ces trois notions sont souvent confondues mais s'emboîtent :

- **Intelligence artificielle** : le domaine le plus large, qui inclut toutes
  les approches visant à reproduire des capacités intelligentes, y compris les
  systèmes à base de règles.
- **Machine learning (apprentissage automatique)** : un sous-ensemble de l'IA où
  le système apprend des régularités à partir de données, sans être programmé
  explicitement pour chaque cas.
- **Deep learning (apprentissage profond)** : un sous-ensemble du machine
  learning fondé sur des réseaux de neurones à plusieurs couches, particulièrement
  efficace pour les images, le son et le langage.

En résumé : tout deep learning est du machine learning, et tout machine learning
est de l'IA, mais l'inverse n'est pas vrai.

## 3. Les grands types d'apprentissage

### 3.1 Apprentissage supervisé
Le modèle apprend à partir d'exemples étiquetés : à chaque entrée correspond une
sortie connue. Il généralise ensuite à de nouveaux cas. Exemples : classer un
e-mail en « spam » ou « non-spam », prédire un prix.

### 3.2 Apprentissage non supervisé
Le modèle reçoit des données sans étiquettes et cherche des structures cachées :
regrouper des éléments similaires (clustering) ou réduire la dimension des
données. Exemple : segmenter automatiquement des clients en groupes.

### 3.3 Apprentissage par renforcement
Un agent apprend par essais et erreurs en interagissant avec un environnement.
Il reçoit des récompenses ou des pénalités et ajuste sa stratégie pour maximiser
la récompense cumulée. Exemple : un programme qui apprend à jouer à un jeu.

## 4. Données d'entraînement

Les données d'entraînement sont les exemples à partir desquels un modèle
apprend. Leur quantité, leur diversité et leur qualité déterminent largement la
performance du modèle. Des données biaisées ou erronées produisent un modèle
biaisé ou peu fiable : c'est le principe « garbage in, garbage out ».

## 5. Notion de modèle

Un modèle est le résultat de l'apprentissage : une fonction paramétrée qui, à
partir d'une entrée, produit une sortie (une prédiction, une classe, un texte).
L'apprentissage consiste à ajuster les paramètres du modèle pour réduire l'écart
entre ses prédictions et les résultats attendus.

## 6. Entraînement, validation, test et inférence

- **Entraînement** : ajustement des paramètres du modèle sur les données
  d'entraînement.
- **Validation** : réglage des hyperparamètres et suivi de la performance sur un
  jeu de validation distinct, afin d'éviter le surapprentissage.
- **Test** : évaluation finale sur des données jamais vues, pour estimer la
  performance réelle.
- **Inférence** : utilisation du modèle entraîné en production pour produire des
  prédictions sur de nouvelles entrées.

## 7. Exemples d'applications

- **Systèmes de recommandation** : suggérer des produits, des films ou des
  articles adaptés aux préférences.
- **Détection d'anomalies** : repérer des transactions ou des comportements
  inhabituels.
- **Analyse de texte** : classer des documents, analyser des sentiments,
  extraire des informations.
- **Chatbots et assistants** : dialoguer en langage naturel.
- **Vision par ordinateur** : reconnaître des objets, lire du texte, analyser des
  images.

## 8. Avantages de l'IA

L'IA permet d'automatiser des tâches répétitives, de traiter de grands volumes
de données, de détecter des régularités difficiles à percevoir pour un humain et
d'assister la prise de décision. Elle peut améliorer la rapidité, la cohérence
et l'accessibilité de nombreux services.

## 9. Limites de l'IA

L'IA présente aussi des limites : dépendance à la qualité des données, risque de
biais, manque de transparence de certains modèles, difficulté à généraliser hors
du périmètre d'apprentissage, et absence de véritable compréhension du sens. Un
contrôle humain reste nécessaire, en particulier pour les décisions sensibles.

## 10. Importance de la qualité des données

La qualité des données est déterminante : des données représentatives, propres,
bien annotées et à jour conduisent à des modèles plus fiables. À l'inverse, des
données incomplètes, déséquilibrées ou obsolètes dégradent la performance et
peuvent introduire des biais. Investir dans la préparation et la gouvernance des
données est souvent plus rentable que de complexifier le modèle.
