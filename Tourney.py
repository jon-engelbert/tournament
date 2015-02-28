__author__ = 'jonengelbert'
import tournament
import datetime
import random

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

    def getPlayers(self):
        conn = tournament.connect()
        cursor = conn.cursor()
        statement = "SELECT player_id FROM  tournament_player WHERE tournament_id = %s"
        data = (self.id,)
        cursor.execute(statement, data)
        conn.commit()
        playerIDs = cursor.fetchall()
        conn.close()
        return playerIDs

    def initialPairingsWithByes(self):
        """Returns a list of pairs of players for the next round of a match.

        Assuming that there are an even number of players registered, each player
        appears exactly once in the pairings.  Each player is paired with another
        player with an equal or nearly-equal win record, that is, a player adjacent
        to him or her in the standings.

        Returns:
          A list of tuples, each of which contains (id1, name1, id2, name2)
            id1: the first player's unique id
            name1: the first player's name
            id2: the second player's unique id
            name2: the second player's name
        """
        playerIDs = self.getPlayers()
        use_bye = len(playerIDs) % 2 != 0
        #max_standing = max(standings, key= numPlayed)
        if use_bye:
            bye_number = random.randint(0,len(playerIDs)-1)
            print("bye number: %d" % bye_number)
            player_bye_id = playerIDs[bye_number]
        i = 0
        pairs = []
        random.shuffle(playerIDs)
        print("first round %s" % playerIDs)
        for playerID in playerIDs:
            if (not use_bye or (playerID != player_bye_id)):
                if i % 2 == 0:
                    prevPlayerID = playerID
                else:
                    pair = (playerID, prevPlayerID)
                    pairs.append(pair)
                i += 1
        print (pairs)
        return pairs
