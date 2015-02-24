__author__ = 'jonengelbert'
import tournament
import datetime

class Match:
    def __init__(self, player1_id, player2_id, tourney_id, round = 0, player1_score = 0, player2_score = 0, ties = 0):
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.tourney_id = tourney_id
        self.round = round,
        self.player1_score = player1_score
        self.player2_score = player2_score
        self.ties = ties

    def delete_from_db(self):
        """Remove all the tournament records from the database."""
        conn = tournament.connect()
        cursor = conn.cursor()
        statement = "DELETE FROM match WHERE player1_id = %d AND player2_id = %d AND tourney_id = %d" % (self.player1_id, self.player2_id, self.tourney_id)
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
        statement = "INSERT INTO  match (player1_id, player2_id, tourney_id, round, player1_score, player2_score, ties) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = (self.player1_id, self.player2_id, self.tourney_id, self.round, self.player1_score, self.player2_score, self.ties)
        cursor.execute(statement, data)
        conn.commit()
        conn.close()
        return