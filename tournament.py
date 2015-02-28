#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random
from Player import *
import Tourney


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


def selectPlayersInTourney(tourney):
    conn = connect()
    cursor = conn.cursor()
    statement = "SELECT * FROM  tournament_player WHERE tournament_id = %s"
    data = (tourney.id,)
    cursor.execute(statement, data)
    player_ids = cursor.fetchall()
    conn.commit()
    conn.close()
    return [Player(player_id) for player_id in player_ids]



def deleteAllMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    statement = "DELETE FROM match"
    cursor.execute(statement)
    conn.commit()
    conn.close()



def deleteAllTournamentPlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    statement = "DELETE FROM tournament_player"
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


def registerPlayerForTourney(player, tourney):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    statement = "INSERT INTO  tournament_player (player_id, tournament_id) VALUES (%s, %s)"
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
    return count

def playerStandingsWithTies(tourney):
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
    conn = connect()
    cursor = conn.cursor()
    statementA = "Create View winner As " \
                 "Select player.id as id, player.name as name, count(match.player1_score) as match_wins, sum(match.player1_score) as game_wins " \
                 "from player FULL OUTER JOIN match on (player.id = match.player1_id) where (match.tourney_id = %s AND match.player1_score > match.player2_score) group by player.id order by name"
    statementB = "Create View loser As " \
                 "select player.id as id, player.name as name, count(match.player1_score) as match_losses, sum(match.player2_score) as game_losses " \
                 "from player FULL OUTER JOIN match on (player.id = match.player2_id) where (match.tourney_id = %s AND match.player1_score > match.player2_score)  group by player.id order by name"
    statementC = "Create View ties1 As " \
                 "select player.id as id, player.name as name, count(match.player1_score) as ties, sum(match.ties) as game_ties " \
                 "from player FULL OUTER JOIN match on (player.id = match.player1_id) where (match.tourney_id = %s AND match.player1_score = match.player2_score)  group by player.id order by name"
    statementD = "Create View ties2 As " \
                 "select player.id as id, player.name as name, count(match.player2_score) as ties, sum(match.ties) as game_ties " \
                 "from player FULL OUTER JOIN match on (player.id = match.player2_id) where (match.tourney_id = %s AND match.player1_score = match.player2_score)  group by player.id order by name"
    data = (tourney.id,)
    cursor.execute(statementA, data)
    cursor.execute(statementB, data)
    cursor.execute(statementC, data)
    cursor.execute(statementD, data)
    statement = "Select COALESCE(winner.id, loser.id), COALESCE(winner.name,  loser.name), COALESCE(winner.match_wins, 0), COALESCE(loser.match_losses,0) from winner FULL OUTER JOIN loser on (winner.id = loser.id) " \
                "group by winner.id, winner.name, loser.id, loser.name, winner.match_wins, loser.match_losses order by winner.name"
    cursor.execute(statement)
    win_loss = cursor.fetchall()
    statement = "Select COALESCE(ties1.id, ties2.id), COALESCE(ties1.name, ties2.name), COALESCE(ties1.ties, 0) + COALESCE(ties2.ties, 0) from ties1 FULL OUTER JOIN ties2  ON (ties1.id = ties2.id)" \
                "group by ties1.id, ties2.id, ties1.name, ties2.name, ties1.ties, ties2.ties order by ties1.name"
    cursor.execute(statement)
    ties = cursor.fetchall()
    statement = "Create View ties As " \
                "Select COALESCE(ties1.id, ties2.id) as id, COALESCE(ties1.name, ties2.name) as name, COALESCE(ties1.ties, 0) + COALESCE(ties2.ties, 0) as ties from ties1 FULL OUTER JOIN ties2  ON (ties1.id = ties2.id)" \
                "group by ties1.id, ties2.id, ties1.name, ties2.name, ties1.ties, ties2.ties order by ties1.name"
    cursor.execute(statement)
    statement = "Create View winloss As " \
                "Select COALESCE(winner.id, loser.id) as id, COALESCE(winner.name,  loser.name)as name, COALESCE(winner.match_wins, 0) as match_wins, COALESCE(loser.match_losses,0) as match_losses from winner FULL OUTER JOIN loser on (winner.id = loser.id) " \
                "group by winner.id, winner.name, loser.id, loser.name, winner.match_wins, loser.match_losses order by winner.name"
    cursor.execute(statement)
    statement =  "Select COALESCE(winloss.id, ties.id) as id, COALESCE(winloss.name, ties.name) as name, COALESCE(winloss.match_wins, 0), COALESCE(winloss.match_losses, 0), COALESCE(ties.ties, 0) from winloss FULL OUTER JOIN ties on (winloss.id = ties.id)"
    cursor.execute(statement, data)
    results = cursor.fetchall()


    # statement =  "Select player.id as id, player.name as name, count(match.player1_score) as match_wins, sum(match.player1_score) as game_wins " \
    #              "from player FULL OUTER JOIN match on (player.id = match.player1_id) where (match.tourney_id = %s AND match.player1_score > match.player2_score) group by player.id order by name"
    # cursor.execute(statement, data)
    # matches = cursor.fetchall()
    # print("wins %s" % matches)
    # statement =  "select player.id as id, player.name as name, count(match.player2_score) as match_losses, sum(match.player2_score) as game_losses " \
    #              "from player FULL OUTER JOIN match on (player.id = match.player2_id) where (match.tourney_id = %s AND match.player1_score > match.player2_score)  group by player.id order by name"
    # cursor.execute(statement, data)
    # matches = cursor.fetchall()
    # print("Losses %s" % matches)
    # statement =  "select player.id as id, player.name as name, count(match.player1_score) as ties, sum(match.ties) as game_ties " \
    #              "from player FULL OUTER JOIN match on (player.id = match.player1_id) where (match.tourney_id = %s AND match.player1_score = match.player2_score)  group by player.id order by name"
    # cursor.execute(statement, data)
    # matches = cursor.fetchall()
    # print("Ties1 %s" % matches)
    # statement = "select player.id as id, player.name as name, count(match.player2_score) as ties, sum(match.ties) as game_ties " \
    #              "from player FULL OUTER JOIN match on (player.id = match.player2_id) where (match.tourney_id = %s AND match.player1_score = match.player2_score)  group by player.id order by name"
    # cursor.execute(statement, data)
    # matches = cursor.fetchall()
    # print("Ties2 %s" % matches)

    return results

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

def reportMatchNew(tourney, round, player1, player2, gameWins1, gameWins2, ties):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    statement = "INSERT INTO  match (tourney_id, round, player1_id, player2_id, player1_score, player2_score, ties) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    data = (tourney.id, round, player1.id, player2.id, gameWins1, gameWins2, ties)
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
        i += 1
    return pairs

def numPlayed(record):
    """
    number of games played for a player
    :param record: A tuple comprised of 0-id, 1-name, 2-wins, 3-losses, 4-ties
    :return: one per win, one per loss, one per tie, sum of all of these
    """
    return record[2] + record[3] + record[4]

def totalPoints(record):
    """
    total points for this player
    :param record: A tuple comprised of 0-id, 1-name, 2-wins, 3-losses, 4-ties
    :return: 2 points per win, one point per tie.
    """
    return 2 * record[2] + record[4]
def winPercentage(record):
    """
    total points for this player divided by totl possible points
    :param record: A tuple comprised of 0-id, 1-name, 2-wins, 3-losses, 4-ties
    :return: 2 points per win, one point per tie, for total points, divide by 2* total games.
    """
    return (2 * record[2] + record[4]) / ( 2* (record[2] + record[3] + record[4]))


def swissPairingsWithByes(tourney):
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
    standings = playerStandingsWithTies(tourney)
    use_bye = len(standings) % 2 != 0
    max_standing = max(standings, key= numPlayed)
    max_played = numPlayed(max_standing)
    players_nobye = [player for player in standings if numPlayed(player) < max_played]
    if use_bye:
        bye_number = random.rand(len(players_nobye))
        player_bye_id = players_nobye[bye_number]
    i = 0
    pairs = []
    if max_played == 0:
        random.shuffle(standings)
        print("first round %s" % standings)
    else:
        standings = sorted(standings, key = totalPoints)
        print("late round %s" % standings)
    for player in standings:
        if (not use_bye or (player[0] != player_bye_id)):
            if i % 2 == 0:
                pair = (player[0], player[1])
            else:
                pair += (player[0], player[1])
                pairs.append(pair)
            print (pairs)
        i += 1
    return pairs
