# Notion-CLI 🚀
 
 ![PyPI - License](https://img.shields.io/pypi/l/milvus-cli)

 ## Overview

 ![Notion](https://notion.so) Command Line Interface which allows you to:

 - Interact with notion i.e creating,updating  databases and pages
-  Export to various file types
- Generates charts from databases
- syncing with external services and many more utils

notion-cli can be used with any scripts or cron and you can easly add your own commands and tools, ![Adding new commands](https://)

## Installation
```
# Download notion-cli repo from github
$ git clone https://github.com/cebosoul/notion-cli.git


# install || add flag if want to easly modify later
pip install --editable notion-cli
```

## Settings
Before we jump to it, we need to config a few things

### Creating Notion Token
![Notion-creating intergation](https://www.notion.so/help/create-integrations-with-the-notion-api)

```
$ export NotionToken=TOKEN
```

## Usage
  ### 1.Interacting with notion
  1.  create new database
    ```
     $ notion-cli databases --create --name DB_NAME --props PROP_NAME=PROP_TYPE,..,
    
    // example
    $ notion-cli databases --create --name tasks_db --props name=title,done=checkbox
    ```
  2.  updating database attributes
  ```
 $ notion-cli databases --update 
 --db tasks_db --new-name archived_tasks
  ```

  3.  creating new page
  ```
 $ notion-cli pages --add-pg --db DB_NAME --set-props name=title,done=checkbox
  ```
  4.  show page(s) on terminal
  ```
   //display db
   $ notion-cli show --name DB_NAME  --limit int

   //display page
    $ notion-cli show --name DB_NAME  --index pg_index

   $ notion-cli pages --update --name tasks_db --props name=title,done=checkbox
```
  ![More- interacting with notion](https://)

  ### 2. Exporting
  > :warning: **Not Fully Implemented**
1. exporting
```
$ notion-cli export --db DB_NAME --to FILE_TYPE  --dest PATH_SAVE_FILE

// use flag -r to export pages also
```

  ### 3. Generating Charts
> :warning: **Not Fully Implemented**
1. charting, (uses matplotlib)
```
$ notion-cli charts line --db DB_NAME -x PROP_NAME -y PROP_NAME
```


## Contributors
* Cebo Sithole

