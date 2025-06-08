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
2) Das gefundene Datenbankdatum hat zunächst eine große Menge an Daten.
3) Die Zeit und die Ressourcen reichen nicht aus, um eine neue Datenbank von Grund auf zu erstellen.

Die Entscheidung wurde gemeinsam von Tatiana K. und Julia K. getroffen.

Quelle der DB: https://www.kaggle.com/datasets/filipkin/cocktails-and-ingredients-dataset

### Regarded options

Wir erstellen und befüllen die Datenbank manuell.

Vorteile:
1) Wir haben die Kontrolle über den Inhalt der Datenbank.

Dagegen:
1) Zeitaufwendig.
2) Risiko von inkonsistenten Daten.
