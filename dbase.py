
import MySQLdb


class DBase(object):
    dsn = ("localhost","root","nbuser","mydic")

    def __init__(self):
        self.conn = MySQLdb.connect(*self.dsn, charset='utf8')
        self.cur = self.conn.cursor()

    # The __enter__ and __exit__ "magic methods" let a class use the with statement.
    # It's basically saying return an instantiated version of this class when it's used
    # in a with DBase() as db: context.
    def __enter__(self):
        return DBase()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def queryDbase(self, sql):
        with DBase() as db:
            self.cur.execute(sql)
            return self.cur.fetchall()

    def updateDbase(self, sql):
        with DBase() as db:
            try:
                self.cur.execute(sql)
                # Commit your changes in the database
                self.conn.commit()
            #except MySQLdb.Error as e:
            except Exception as e:
                print(e)

            except :
                print('error', sys.exc_info()[0])

            return
