# Atualiza o pip para a versão mais recente
python3 -m pip install --upgrade pip

# Instala as dependências do projeto
python3 -m pip install --no-cache-dir -r requirements.txt

# Migrando banco de dados
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

# Coletando arquivos estáticos
python3 manage.py collectstatic --noinput
