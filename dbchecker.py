from settings import settings
import sqlite3




def checkdb():
    pymsdbver = checkversion(databasepath)
    print('dbchecker.py : PyMS Database version = %s' % pymsdbver)
    if pymsdbver ==1:
        version_1_to_2(databasepath)
    resultsdbver= checkversion(resultsdatabase)
    print('dbchecker.py : Results Database version = %s' % resultsdbver)
    if resultsdbver ==1:
        version_1_to_2(resultsdatabase)


def checkversion(filepath):
    database = sqlite3.connect(filepath)
    cursorObj = database.cursor()
    sqlquery = "Select version from version"
    try:
        cursorObj.execute(sqlquery)
        return cursorObj.fetchone()[0]
    except sqlite3.OperationalError:
        return 1
    finally:
        database.close()

def version_1_to_2(filepath):
    database = sqlite3.connect(filepath)
    database.execute('CREATE TABLE Version (version INTEGER DEFAULT (1));')
    database.commit()
    cursorObj = database.cursor()
    sqlinsert = "INSERT INTO version (version) VALUES (2)"
    cursorObj.execute(sqlinsert)
    database.commit()
    database.close()



databasepath = settings['database']['databasepath']
resultsdatabase =  settings['database']['resultsdatabasepath']
checkdb()