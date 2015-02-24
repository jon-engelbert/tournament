__author__ = 'jonengelbert'
import tournament

class Player:
    def __init__(self, name, initcount = 0):
        self.name = name
        self.initcount = initcount
        self.id = None

    def delete_from_db(self):
        """Remove all the player records from the database."""
        print("delete_from_id, name, id: %s %d" % (self.name, self.id))
        conn = tournament.connect()
        cursor = conn.cursor()
        statement = "DELETE FROM player WHERE id = %d" % self.id
        cursor.execute(statement)
        conn.commit()
        conn.close()

    def add_to_db(self):
        """Adds a player to the tournament database.
        The database assigns a unique serial id number for the player.  (This
        should be handled by your SQL database schema, not in your Python code.)
        Args:
          name: the player's full name (need not be unique).
        """
        conn = tournament.connect()
        cursor = conn.cursor()
        statement = "INSERT INTO  player (name) VALUES (%s) RETURNING ID"
        data = (self.name,)
        cursor.execute(statement, data)
        conn.commit()
        self.id = cursor.fetchone()[0]
        conn.close()
        return




