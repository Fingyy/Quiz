# Quiz
Quiz je webová aplikace vyvinutá pomocí Django frameworku. Uživatel si vybere kolik otázek má kvíz obsahovat, určí úroveň obtížnosti a vybere kategorii. Na tomto základě program vygeneruje pro hráče sadu otázek. Každá z nich je zobrazena na obrazovce prohlížeče. Po jejich zodpovězení hra končí a hráč získá své skóre.

## Požadavky
- python~= 3.7
- django~=3.2.25
- requests~=2.31.0

## Použité technologie
- Django, Python
- HTML, CSS

## Setup
### 1. Klonování repozitáře:
```
git clone https://github.com/Fingyy/Quiz.git
```
### 2. Vytvoření a nastavení virtual env:
Windows
```
pip install virtualenv
python -m virtualenv venv
.\venv\Scripts\activate
```
Mac
```
pip install virtualenv
python -m virtualenv venv
source venv/bin/activate
```
### 3. Instalace závislostí:
```
pip install -r requirements.txt
```
### 4. Nastavení databáze:
```
python manage.py migrate
```
### 5. Spuštění serveru:
```
python manage.py runserver
```
### 6. Přístup k aplikaci:
- Otevřete webový prohlížeč a přejděte na http://localhost:8000/
- Pro administrativní rozhraní přejděte na http://localhost:8000/admin/
