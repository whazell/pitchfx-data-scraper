import logging
import pymysql.cursors
from scrapers import config

CACHE_LIMIT = 1000

def init_db():
    '''
        Initialize the globals for this module.

        Returns False on error, True otherwise
    '''
    global logger
    global db 
    global cur
    global insert_list
    global cached_count
    global db_name

    insert_list = []
    cached_count = 0
    logger = logging.getLogger(__name__)
    
    db_info = config.get_db_config()
    
    try:
        db  = pymysql.connect(host=db_info['host'], user=db_info['user'], \
               passwd=db_info['passwd'], db=db_info['db_name'])
        cur = db.cursor()
    except:
        logger.error("Could not connect to database.")
        return False
    
    db_name = db_info['db_name']
    return True


def insert_db (query, data, need_result):
    '''
        Insert data into the database using the connection established in 
        init_db(). If an error is encountered, rollback the database. If need_result 
        is true, then the data is inserted immediately. If it is false the data will
        be grouped before the insert for efficiency.

        Return False on Error, otherwise return True.
    '''
    global cached_count
    global insert_list
    
    ins = (query, data)
    cached_count += 1
    insert_list.append((query, data))

    if need_result == True or cached_count > CACHE_LIMIT:
        result = _insert(insert_list)
        del insert_list[:]
        insert_list = []
        cached_count = 0
        return result

def flush_db ():
    '''
        This function will bulk insert all cached items. This should be called 
        before the program is finished to ensure all items are added to the database
        and not just cached
    '''
    global cached_count
    global insert_list

    result = _insert(insert_list)
    cached_count = 0
    insert_list = []
    return result

def _insert (insert_list):
    '''
        Bulk inserts all cached items into the database.
    '''
    
    for i in insert_list:
        try:
            cur.execute(i[0], i[1])
        except pymysql.Error as e:
            logger.warning('Got error {!r}, errno is {}'.format(e, e.args[0]) + 
                            "Data that caused the issue: " + str(i[0]) + str(i[1]))
            continue
    
    # Commit changes to db
    try:
        db.commit()
    except pymysql.Error as e:
        logger.warning('Got error {!r}, errno is {}'.format(e, e.args[0]))
        db.rollback
        return False

    return True


def build_query (db_map, db_table, gid, date):
    '''
        Build the query based on the database map given. Since gid and
        date are excluded from the maps, they must be manually added at 
        the start.

        Returns the query that will look like:

        insert into db_table (x, y, z) values (%s, %s, %s)
    '''
    query = "insert into " + db_table + "("
    val_query = " values ("

    if date:
        query     += "game_date, "
        val_query += "%s," 

    if gid:
        query += "gid, " 
        val_query += "%s,"

    # Build the query
    i = len(db_map)
    for key in db_map:
        query     += key[0]
        val_query += "%s"
        i -= 1
        if i > 0:
             query +=  ","
             val_query += ","
    
    query += ")" + val_query + ")"
    return query


def check_tables():
    '''
        This function checks if all the tables defined in the config file 
        are available in the database. If they are, then return true, and 
        if they are not then return false.
    '''
    ret = True
    cur.execute("SHOW tables")
    tables = cur.fetchall()
    
    # fetchall() returns list of tuples, so need to flatten
    tables = [i[0] for i in tables]
    
    for i in config.table_list:
        if i not in tables:    
            print("Could not find table: " + i)
            ret = False

    return ret


def get_newest_schema():
    '''
        Check the db/schema/ folder for the most recent database schema file based on 
        the numerical ordering. The names are in the form:

        xxxx_schema.sql

    '''
    prefix = "db/schema/"
    return prefix + "0001_schema.sql"

def get_last_id():
    '''
        Return the ID from the last item inserted. 
    '''
    return cur.lastrowid
    

def get_name():
    ''' 
        Return name of currently used database
    '''
    global db_name
    return db_name


def get_latest_date():
    '''
        Get the latest date of data that is currently in the database
    '''
    cur.execute("SELECT MAX(game_date) FROM games")
    date = cur.fetchone()
    return date[0]
