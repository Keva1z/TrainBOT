# Training BOT

## Bot that helps people get motivation to train

## STEP 1: Setup

### Clone repository from GitHub

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
```

## Create .env file in 'misc' folder

### Write this to .env file

```env
TOKEN_API="##########:###################################"
KEYS_FOLDER = "misc/keys"
DB_PATH = "misc/database.db"
```

## pass your bot api key to TOKEN_API variable

```env
TOKEN_API="##########:###################################"
           ^^^^^^^^^^ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KEYS_FOLDER = "misc/keys"
DB_PATH = "misc/database.db"
```

## Step 2: Create venv

### Open terminal and write

```bash
python -m venv .venv
```

### Then activate environment

```bash
cd .venv/scripts
activate
```

### Then install dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Create RSA keys

### Run file 'create_keys.py'

```bash
python create_keys.py
```

## Step 4: Create database

### Bot using sqlite3 so

### Create 'database.db' file in misc folder

## Step 5: Start bot

```bash
python main.py
```

## Step 6: Profit
