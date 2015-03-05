__author__ = 'jonengelbert'
import tournament

class Player:
    def __init__(self, name, initRating = 0.5):
        self.name = name
        self.rating = initRating
        self.id = None

    def delete_from_db(self):
        """Remove all the player records from the database."""
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
    @classmethod
    def Create(id):
        conn = tournament.connect()
        cursor = conn.cursor()
        statement = "SELECT name, initcount FROM  player WHERE id = %"
        data = (id)
        cursor.execute(statement, data)
        conn.commit()
        params = cursor.fetchone()
        player = self(params[0], params[1])
        player.id = id
        conn.close()
        return player

    @classmethod
    def all(self, tourney_id):
        conn = tournament.connect()
        cursor = conn.cursor()
        statement = "SELECT tournament_player.player_id as id, player.name as name FROM  tournament_player JOIN player ON (tournament_player.player_id = player.id) WHERE tournament_id = %s"
        data = (tourney_id,)
        cursor.execute(statement, data)
        conn.commit()
        players = cursor.fetchall()
        conn.close()
        return [(player[0], player[1]) for player in players]
