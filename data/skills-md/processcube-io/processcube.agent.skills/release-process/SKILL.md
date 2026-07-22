---
name: release-process
description: Erstellt Releases (Stable, Insiders, Development) mit Single-Branch-Workflow (nur main). Nutze diesen Skill wenn der Benutzer eine Version erstellen oder releasen möchte.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
disable-model-invocation: true
---

# Release Process

Du bist ein Release-Manager und erstellst Releases nach Semantic Versioning mit einem Single-Branch-Workflow (nur `main` Branch).

## Release-Typen

Der Benutzer sagt dir welche Version er erstellen will:

| Typ | Format | Beispiel |
|-----|--------|----------|
| **Stable** | `MAJOR.MINOR.PATCH` | `1.0.0`, `1.1.0`, `2.0.0` |
| **Insiders** | `X.Y+1.0-insiders.N` | Stable `1.0.0` → `1.1.0-insiders.1`, `1.1.0-insiders.2` |
| **Development** | `X.Y+1.0-develop.N` | Stable `1.0.0` → `1.1.0-develop.1`, `1.1.0-develop.2` |

**Wichtig**: Insiders und Development basieren immer auf der letzten Stable-Version mit erhöhtem Minor!

## Allgemeiner Ablauf

### 1. Vorbereitung (IMMER zuerst)

```bash
# Prüfe aktuellen Branch
git branch --show-current

# Prüfe auf uncommitted changes
git status --porcelain
```

- Falls nicht auf `main`: Frage ob gewechselt werden soll
- **Falls uncommitted changes vorhanden**: Führe `git stash` aus und merke dir dies
- Aktualisiere: `git pull origin main`

### 2. Version ermitteln

- Lies aktuelle Version aus `package.json` oder anderen Versionsdateien
- Suche nach existierenden Tags: `git tag -l "v*"`

### 3. Neue Version bestimmen

**Für Stable Release:**
- Analysiere Commits seit letztem stabilen Tag: `git log v{LAST_VERSION}..HEAD --oneline`
- Analysiere Code-Änderungen: `git diff v{LAST_VERSION}..HEAD`
- Bestimme Release-Typ:
  - **MAJOR**: Breaking Changes (entfernte APIs, geänderte Signaturen, `BREAKING CHANGE` in Commits, `feat!:` oder `fix!:`)
  - **MINOR**: Neue Features (`feat:` Commits, neue exportierte Funktionen)
  - **PATCH**: Bug Fixes, interne Änderungen

**Für Insiders Release:**
- Finde letzte Stable-Version: `git tag -l "v[0-9]*.[0-9]*.[0-9]*" | grep -v "-" | sort -V | tail -1`
- Berechne Basisversion: Letzte Stable + Minor erhöht, Patch auf 0
  - Beispiel: Stable `1.0.0` → Basis `1.1.0`
  - Beispiel: Stable `2.3.5` → Basis `2.4.0`
- Suche existierende Insiders-Tags für diese Basis: `git tag -l "v{BASIS}-insiders.*" | sort -V | tail -1`
- Wenn Tags existieren: Nummer hochzählen (z.B. `1.1.0-insiders.3` → `1.1.0-insiders.4`)
- Wenn keine existieren: Starte mit `.1` (z.B. `1.1.0-insiders.1`)

**Für Development Release:**
- Finde letzte Stable-Version: `git tag -l "v[0-9]*.[0-9]*.[0-9]*" | grep -v "-" | sort -V | tail -1`
- Berechne Basisversion: Letzte Stable + Minor erhöht, Patch auf 0
  - Beispiel: Stable `1.0.0` → Basis `1.1.0`
  - Beispiel: Stable `2.3.5` → Basis `2.4.0`
- Suche existierende Develop-Tags für diese Basis: `git tag -l "v{BASIS}-develop.*" | sort -V | tail -1`
- Wenn Tags existieren: Nummer hochzählen (z.B. `1.1.0-develop.5` → `1.1.0-develop.6`)
- Wenn keine existieren: Starte mit `.1` (z.B. `1.1.0-develop.1`)

### 4. Changelog generieren (PFLICHT)

**Führe vor dem Release den Changelog-Skill aus.** Lies dazu die Datei `skills/changelog/SKILL.md` und befolge die darin beschriebenen Anweisungen vollständig.

- Zielgruppe: **Anwender** (Changelog aus Nutzersicht)
- Modus: **Aktualisieren** (nur neue Änderungen seit letztem Eintrag)
- Stelle sicher, dass alle Commits seit dem letzten Tag im Changelog dokumentiert sind
- **Erst wenn der Changelog erfolgreich aktualisiert wurde, fahre mit Schritt 5 fort**

### 5. Version aktualisieren

- Aktualisiere `package.json` und andere Versionsdateien
- Commite: `git commit -am "chore: release v{VERSION}"`

### 6. Tag erstellen und pushen

```bash
git tag v{VERSION}
git push origin main
git push origin v{VERSION}
```

### 7. Änderungen wiederherstellen

- **Falls in Schritt 1 gestasht wurde**: `git stash pop`
- Informiere den Nutzer

### 8. Zusammenfassung

Zeige:
- Alte Version → Neue Version
- Release-Typ
- Wichtigste Änderungen
- Git Tag Name
