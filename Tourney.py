__author__ = 'jonengelbert'
import tournament
import datetime

class Tourney:
    def __init__(self, name, date=datetime.date.today(), location = ""):
        self.name = name
        self.date = date,
        self.location = location
        self.id = None

    def delete_from_db(self):
        """Remove all the tournament records from the database."""
        print("delete_from_id, name, id: %s %d" % (self.name, self.id))
        conn = tournament.connect()
        cursor = conn.cursor()
        statement = "DELETE FROM tourney WHERE id = %d" % self.id
        cursor.execute(statement)
        conn.commit()
        conn.close()

    def add_to_db(self):
        """Adds a tournament to the tournament database.
        The database assigns a unique serial id number for the player.  (This
        should be handled by your SQL database schema, not in your Python code.)
        Args:
          name: the player's full name (need not be unique).
        """
        conn = tournament.connect()
        cursor = conn.cursor()
        statement = "INSERT INTO  tourney (name, tourney_date, location) VALUES (%s, %s, %s) RETURNING ID"
        data = (self.name, self.date, self.location)
        cursor.execute(statement, data)
        conn.commit()
        self.id = cursor.fetchone()[0]
        conn.close()
        return

    def registerPlayer(self, player):
        conn = tournament.connect()
        cursor = conn.cursor()
        statement = "INSERT INTO  tournament_player (player_id, tournament_id) VALUES (%s, %s)"
        data = (player.id, self.id)
        cursor.execute(statement, data)
        conn.commit()
        conn.close()
