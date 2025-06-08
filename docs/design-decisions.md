---
title: Design Decisions
nav_order: 3
---

{: .label }
[Tatjana K.]

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>



## 01: Cocktail DB

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 17-Apr-2025

### Problem statement

Wir benötigen eine Datenbank mit Cocktailrezepten und den dazugehörigen Zutaten, um einen Webservice für Cocktails zu erstellen.

### Decision

Wir verwenden ein Schema und Daten aus einer öffentlich zugänglichen Quelle. Die Hauptmerkmale der Datenbank sind, dass Cocktails und ihre Zutaten bereits miteinander verknüpft sind und dass sie bereits über genügend vorerfasste Daten verfügt.
Die Gründe:
1) Das Datenbankschema ist als korrekt erachtet.
2) Die gefundene Datenbank hat zunächst eine große Menge an Daten.
3) Die Zeit und die Ressourcen reichen nicht aus, um eine neue Datenbank von Grund auf zu erstellen.

Die Entscheidung wurde gemeinsam von Tatiana K. und Julia K. getroffen.

Quelle der DB: https://www.kaggle.com/datasets/filipkin/cocktails-and-ingredients-dataset

### Regarded options

Wir erstellen und befüllen die Datenbank manuell.

Vorteile:
1) Wir haben die Kontrolle über den Inhalt der Datenbank.

Nachteile:
1) Zeitaufwendig.
2) Risiko von inkonsistenten Daten.


## 02: Snack DB

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 20-Apr-2025

### Problem statement

Wir benötigen eine Datenbank mit Snacks, um einen Webservice für die Suche von Cocktails und dazu gehörenden Snack zu erstellen.

### Decision

Wir erstellen eine Snack-Datenbank manuell.

Die Entscheidung wurde gemeinsam von Tatiana K. und Julia K. getroffen.
Julia K. erstellt und befüllt eine Tabelle mit Snacks manuell.

### Regarded options

Wir nutzen eine öffentlich zugängliche Datenbank von Snacks.

Vorteile:
1) Zeitsparend.
2) Diese Datenbank wird bereits eine große Menge an Daten haben.
3) Das Datenbankschema wird wahrscheinlich richtig erstellt.

Nachteile:
1) Wir haben keine Kontrolle über den Inhalt der Datenbank.
2) Es besteht die Wahrscheinlichkeit, dass der Inhalt der Snack-Datenbank nicht mit unserer Cocktail-Datenbank übereinstimmt.



## 03: Die Beziehung Cocktails mit Snacks

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 01-Mai-2025

### Problem statement

Wir möchten ein relationales Modell für die Beziehungen zwischen Snacks und Cocktails definieren, das der Funktionalität unseres Webservices für die Suche nach Cocktails und passenden Snacks entspricht.

### Decision

Jeder Cocktail besteht aus einer oder mehreren Zutaten. Jede der Zutaten hat eine feste Position (Postion 1, Position 2, usw.) im Cocktail. Für jede Grundzutat, die Alkohol ist, wird ein einziger Snack angeboten. Um den Snack für den Cocktail zu bestimmen, wählen wir den Snack für die alkoholische Zutat des Cocktails mit der kleinsten Positionszahl.

In der Datenbank kann dieses Schema durch das folgende Diagramm dargestellt werden:

![snack_cocktail_relation_diagram.png](snack_cocktail_relation_diagram.png)


**Erklärung anhand zwei Beispiele:**

1) Cocktail-Id: 11002

| Zutaten   | Position im Cocktail |
|-----------|----------------------|
| Vodka     | 1                    |
| Light rum | 2                    |
| Gin       | 3                    |
| Tequila   | 4                    |
| Lemon     | 5                    |
| Coca-Cola | 6                    |

In diesem Beispiel sind 4 Zutaten alkoholisch. Nach der Logik unserer Datenbank wählen wir den Snack nach Alkohol mit der kleinsten Positionsnummer aus. Das bedeutet, dass für diesen Cocktail der Alkohol an Position 1 für die Snackauswahl ausschlaggebend ist.

2) Cocktail-Id: 14564

| Zutaten              | Position im Cocktail |
|----------------------|----------------------|
| Cranberry juice      | 1                    |
| Soda water           | 2                    |
| Midori melon liqueur | 3                    |
| Creme de Banane      | 4                    |

In diesem Beispiel haben wir zwar vier Zutaten, aber nur eine davon ist alkoholisch. Diese befindet sich auf Position 3 und ist somit ausschlaggebend für die Snackauswahl.

Die Entscheidung wurde von Tatiana K. getroffen.
Tatjana K. übernimmt die SQL-Anfragen und die Erstellung der Relationen Cocktail-Snack-Tabellen.

### Regarded options

**1) Wir weisen jedem Cocktail einen eigenen Snack zu.**

Pro:
- Einfacheres relationales Datenbankmodell

Contra:
- Duplizierung der Daten (z.B. mehrere Cocktails werden die gleichen Snacks haben) -> Gegenteil von Normalisierung einer DB
- Logische Inkonsistenz, z.B. Cocktails mit ähnlichen Zutaten unterschiedliche Snacks zuzuordnen.


**2) Wir ordnen jedem Cocktail mit mehreren alkoholischen Grundzutaten eine Reihe von entsprechenden Snacks zu.**

Pro:
- die Möglichkeit, ein flexibles Modell für die Snackauswahl zu erstellen

Contra:
- komplexeres Datenbankschema
- Logische Inkonsistenz, z.B. Zuordnung von zueinander unpassenden Snacks
