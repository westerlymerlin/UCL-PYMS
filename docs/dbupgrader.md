# None

<a id="dbupgrader"></a>

# dbupgrader

Database backup and upgrade tools.

This module provides functions for performing database backups and upgrading
databases to newer versions. It includes functionalities to back up specified
databases into a compressed zip file, as well as to modify database schemas
and update data based on new version changes or requirements.

Functions:
- backup_database(): Creates a zip file backup of the main and results database.
- pyms_database_update(): Upgrades the primary database to the latest version.
- results_database_update(): Upgrades the results database to the latest version.
- check_db_version(): Determines the current version of a database or initializes
  it if it is missing required structures.

Author: Gary Twinn

<a id="dbupgrader.zipfile"></a>

## zipfile

<a id="dbupgrader.path"></a>

## path

<a id="dbupgrader.os"></a>

## os

<a id="dbupgrader.time"></a>

## time

<a id="dbupgrader.sqlite3"></a>

## sqlite3

<a id="dbupgrader.settings"></a>

## settings

<a id="dbupgrader.backup_database"></a>

#### backup\_database

```python
def backup_database()
```

Creates a backup of the specified database and its results database in a zip file.

Summary:
This function generates a backup of the main database file and the results database
file specified in the provided settings. The two database files are archived together
in a zip file for safekeeping. The backup process involves locating the database files,
creating a zip archive, compressing the files, and saving the archive in the same
directory as the primary database file with a default naming convention. After completing
the backup, the function prints out the total processing time and a completion message.

<a id="dbupgrader.pyms_database_update"></a>

#### pyms\_database\_update

```python
def pyms_database_update()
```

Updates the PyMS database schema and data to the latest version.

This function handles the migration of the PyMS database from an earlier
version to the latest supported version. It updates the schema, modifies
data to align with the new schema, and performs data integrity adjustments.
The process involves adding new columns, updating records, and modifying
database views as necessary to support the updated functionality and logic
of the PyMS application.

<a id="dbupgrader.check_db_version"></a>

#### check\_db\_version

```python
def check_db_version(database)
```

Checks the database version and initializes the settings table if it does not exist.

This function queries the `settings` table in the provided database to determine
the current version. If the `settings` table is missing, it assumes the database
is version 0, creates the `settings` table, and sets its version to 1. Afterward,
it retrieves the version from the `settings` table.

<a id="dbupgrader.results_database_update"></a>

#### results\_database\_update

```python
def results_database_update()
```

Updates the Results Database by checking its version and applying necessary upgrades.

This function ensures that the Results Database is up-to-date by verifying the current version
and performing structural or data upgrades if needed. The current implementation upgrades
the database from version 1 to version 2, modifying specific records in the HeliumRuns table
and updating the database schema version.

