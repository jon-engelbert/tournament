#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from Player import *


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    player = Player(name)
    player.add_to_db()

def registerPlayerForTourney(player, tourney):
    """Adds a player to a tournament.
    Args:
      player: the player object instance,
      tourney: the tournament object instance.
    """
    conn = tournament.connect()
    cursor = conn.cursor()
    statement = "INSERT INTO  tournament_player (player_id, tournament_id) VALUES (%s %s)"
    data = (player.id, tourney.id)
    cursor.execute(statement, data)
    conn.commit()
    conn.close()
    return



def deleteAllMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    statement = "DELETE FROM match"
    cursor.execute(statement)
    conn.commit()
    conn.close()



def deleteAllPlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    statement = "DELETE FROM player"
    cursor.execute(statement)
    conn.commit()
    conn.close()

def deleteAllTournaments():
    """Remove all the tournament records from the database."""
    conn = connect()
    cursor = conn.cursor()
    statement = "DELETE FROM tourney"
    cursor.execute(statement)
    conn.commit()
    conn.close()


def registerPlayerForTourney(player, tournament):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    statement = "INSERT INTO  tournament_players (player_id, tournament_id) VALUES (%s)"
    data = (player.id, tourney.id)
    cursor.execute(statement, data)
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    statement = "SELECT COUNT(*) FROM player"
    cursor.execute(statement)
    result=cursor.fetchone()
    conn.close()
    if result:
        count = result[0]
    else:
        count = 0
    print("count: %d" % count)
    return count

def countTourneys():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    statement = "SELECT COUNT(*) FROM tourney"
    cursor.execute(statement)
    result=cursor.fetchone()
    conn.close()
    if result:
        count = result[0]
    else:
        count = 0
    print("count: %d" % count)
    return count

def countMatches():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    statement = "SELECT COUNT(*) FROM match"
    cursor.execute(statement)
    result=cursor.fetchone()
    conn.close()
    if result:
        count = result[0]
    else:
        count = 0
    print("count: %d" % count)
    return count


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # view for win count
    print("about to calculate playerStandings")
    conn = connect()
    cursor = conn.cursor()
    statementA = "Create View winner As " \
                 "Select player.id as id, player.name as name, count(match.player1_score) as wins " \
                 "from player left join match on (player.id = match.player1_id)  group by player.id order by wins DESC"
    statementB = "Create View loser As " \
                 "select player.id as id, player.name as name, count(match.player2_score) as losses " \
                 "from player left join match on (player.id = match.player2_id)  group by player.id order by losses"
    cursor.execute(statementA)
    cursor.execute(statementB)
    statement = "Select winner.id, winner.name, winner.wins, winner.wins + loser.losses from winner left join loser on (winner.id = loser.id) group by winner.id, winner.name, winner.wins, loser.losses order by winner.wins DESC"
    cursor.execute(statement)
    results = cursor.fetchall()
    for res_id, res_name, res_wins, res_total in results:
        print("winner: %s, wins: %s, total: %s" % (res_name, res_wins, res_total))
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    statement = "INSERT INTO  match (player1_id, player2_id, player1_score, player2_score) VALUES (%s, %s, %s, %s)"
    data = (winner, loser, 1, 0)
    cursor.execute(statement, data)
    conn.commit()
    conn.close()

def swissPairings():
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
    standings = playerStandings()
    i = 0
    pairs = []
    for player_id, name, wins, matches in standings:
        if i % 2 == 0:
            pair = (player_id, name)
        else:
            pair += (player_id, name)
            pairs.append(pair)
        print (pairs)
        i += 1
    return pairs
