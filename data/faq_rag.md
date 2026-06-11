# FAQ — Systèmes RAG

> Document pédagogique de démonstration. Contenu fictif et généraliste.

## Qu'est-ce qu'un RAG ?

RAG signifie *Retrieval-Augmented Generation* (génération augmentée par la
récupération). C'est une architecture qui associe un moteur de recherche
sémantique, qui retrouve des passages pertinents dans une base documentaire, et
un grand modèle de langage (LLM), qui rédige une réponse à partir de ces
passages. Le modèle ne se contente donc pas de ses connaissances internes : il
s'appuie sur des documents fournis au moment de la requête.

## Pourquoi utiliser un RAG ?

- **Réduction des hallucinations** : les réponses sont ancrées dans des documents réels.
- **Connaissances à jour** : il suffit d'ajouter ou de modifier des documents.
- **Traçabilité** : on peut citer les sources et permettre la vérification.
- **Confidentialité** : on interroge un corpus privé sans l'exposer à l'entraînement.
- **Coût maîtrisé** : pas besoin d'entraîner un modèle spécialisé.

## Quelle est la différence entre RAG et fine-tuning ?

Le **fine-tuning** consiste à réentraîner un modèle sur des données spécifiques
pour modifier son comportement ; les connaissances sont alors « gravées » dans
les paramètres et leur mise à jour exige un nouvel entraînement. Le **RAG**, lui,
ne modifie pas le modèle : il lui fournit des documents au moment de la requête.
Le RAG est plus simple à mettre à jour et plus transparent (sources vérifiables),
tandis que le fine-tuning est utile pour adapter le style ou les compétences du
modèle. Les deux approches peuvent être combinées.

## Qu'est-ce que l'ingestion documentaire ?

L'ingestion est l'étape qui prépare les documents pour la recherche : les
fichiers sont chargés, leur texte est extrait, découpé en fragments (chunks),
transformé en embeddings, puis stocké dans une base vectorielle avec ses
métadonnées (source, position).

## Qu'est-ce qu'un chunk ?

Un *chunk* est un fragment de texte de taille maîtrisée obtenu en découpant un
document. On choisit une taille cible (par exemple 1000 caractères). Des chunks
trop grands diluent la pertinence ; trop petits, ils perdent le contexte.

## Pourquoi utilise-t-on un overlap entre les chunks ?

L'**overlap** (recouvrement) consiste à reprendre la fin d'un chunk au début du
suivant. Cela évite de couper une idée ou une phrase en deux à la frontière des
fragments et préserve la continuité du contexte. Un recouvrement de 10 à 20 % de
la taille du chunk est courant.

## Qu'est-ce qu'un embedding ?

Un *embedding* est une représentation vectorielle d'un texte : une liste de
nombres qui capture son sens. Deux textes proches sémantiquement ont des vecteurs
proches dans l'espace, ce qui permet de comparer des textes par le sens et non
par les mots exacts.

## Qu'est-ce qu'une base vectorielle ?

Une base vectorielle stocke les embeddings et permet de retrouver rapidement les
vecteurs les plus proches d'un vecteur de requête. Elle est optimisée pour la
recherche par similarité à grande échelle. Des exemples courants sont Chroma,
FAISS ou pgvector ; un simple index en mémoire (par exemple avec NumPy) suffit
pour de petits corpus.

## Comment fonctionne la similarité cosinus ?

La similarité cosinus mesure l'angle entre deux vecteurs, indépendamment de leur
longueur. Sa valeur va de -1 à 1 : proche de 1, les vecteurs pointent dans la
même direction et les textes sont sémantiquement proches ; proche de 0, ils sont
peu liés. C'est une métrique très utilisée pour comparer des embeddings.

## Pourquoi afficher les sources ?

Afficher les sources renforce la confiance et la vérifiabilité : l'utilisateur
peut remonter au document d'origine, contrôler l'exactitude de la réponse et
détecter d'éventuelles erreurs. C'est essentiel pour les usages professionnels.

## Comment limiter les hallucinations ?

On limite les hallucinations en ancrant strictement les réponses dans le contexte
récupéré, grâce à une consigne système explicite, en fournissant des passages
pertinents, en affichant les sources et en demandant au modèle de signaler
l'absence d'information plutôt que d'inventer.

## Que doit faire le système si l'information n'existe pas dans les documents ?

Il doit l'indiquer clairement, par exemple en répondant que l'information n'est
pas disponible dans les documents, au lieu de produire une réponse inventée.
C'est le comportement attendu d'un système fiable (anti-hallucination).

## Quelles sont les limites d'un prototype RAG simple ?

- Un index en mémoire convient à de petits corpus, pas à des millions de documents.
- Le découpage par caractères est simple ; un découpage par phrases serait plus fin.
- Il n'y a pas de reclassement (re-ranking) avancé des résultats.
- La qualité dépend du modèle d'embeddings et du LLM utilisés.

## Quelles améliorations sont possibles en production ?

- Utiliser une base vectorielle dédiée pour passer à l'échelle.
- Ajouter un re-ranker pour améliorer la pertinence.
- Mettre en place une évaluation automatique (jeux de questions/réponses).
- Gérer l'authentification, les accès et la journalisation.
- Ajouter le multilingue et la recherche hybride (lexicale + sémantique).
