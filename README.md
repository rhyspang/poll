## install project
```
cd annotator_audio
source ./install.sh
```

## requirements
```
pip install -r requirements.txt
```

## configuration
using mysql for storage
1. modify annotator/config.py `SQLALCHEMY_DATABASE_URI` to fit your mysql database
2. run `flask db init` to init migration
3. run `flask db migrate` to make a migration
4. run `flask db upgrade` to apply a migration

## run
```
flask run -h 0.0.0.0 -p 2256 --no-debugger --without-threads
```

# file2db
run `python file_info2db.py` to add audio info to db