#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2
import random
from Player import *
from Tourney import Tourney


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


def selectPlayerIdsInTourney(tourney):
    conn = connect()
    cursor = conn.cursor()
    statement = "SELECT * FROM  tournament_player WHERE tournament_id = %s"
    data = (tourney.id,)
    cursor.execute(statement, data)
    player_ids = [playerID[1] for playerID in cursor.fetchall()]
    conn.commit()
    conn.close()
    return player_ids



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

def InitialPairingsWithByes(players):
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
    use_bye = len(players) % 2 != 0
    random.shuffle(players)
    #max_standing = max(standings, key= numPlayed)
    player_bye_id = None
    if use_bye:
        bye_number = random.randint(0,len(players)-1)
        byePlayer = Player(players[bye_number][1])
        byePlayer.id = players[bye_number][0]
    i = 0
    pairs = []
    for player in players:
        if (not use_bye or (player[0] != byePlayer.id)):
            if i % 2 == 0:
                prevPlayer = player
            else:
                pair = (player[0], player[1], prevPlayer[0], prevPlayer[1])
                pairs.append(pair)
            i += 1
    return pairs, byePlayer

def playerStandingsII(tourney, initial_bye_player = None):
    """Returns a list of the players and their win records, sorted by win percentage

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, losses, ties, matches played, points,  win percentage, game wins, game losses):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()

    statement_playerrecords = "Create View playerrecords AS " \
                 "(Select player.id as player_id, player.name as name, match.player1_score as wins, match.player2_score as losses, match.ties as ties from player FULL OUTER JOIN match on (player.id = match.player1_id) " \
                 "where (match.tourney_id = %s) order by name)" \
                 " UNION " \
                 "(Select player.id as player_id, player.name as name, match.player2_score as wins, match.player1_score as losses, match.ties as ties from player FULL OUTER JOIN match on (player.id = match.player2_id) " \
                 "where (match.tourney_id = %s) order by name)"
    data = (tourney.id, tourney.id)
    cursor.execute(statement_playerrecords, data)
    statement_playerstandings =  "Create View playerstandings AS " \
                 "Select player_id as id, name, count(case when wins > losses then 1 end) as match_wins, count(case when wins < losses then 1 end) as match_losses, count(case when wins = losses then 1 end) as match_ties, " \
                 "sum(wins) as game_wins, sum(losses) as game_losses, sum(ties) as game_ties " \
                 "from playerrecords group by player_id, name order by match_wins DESC"
    cursor.execute(statement_playerstandings)
    statement =  "Select  id, name, match_wins, match_losses, match_ties, (match_wins+ match_losses + match_ties) as gp, (match_wins * 2 + match_ties) as points, (match_wins + match_ties/2.0)/(match_wins+ match_losses + match_ties) as win_pct, game_wins, game_losses " \
                 "from playerstandings group by id, name, match_wins, match_losses, match_ties, game_wins, game_losses order by win_pct DESC"
    cursor.execute(statement)
    playerstandings = cursor.fetchall()

    if len(playerstandings) == 0:
            playerstandings = [(p[0], p[1], 0, 0, 0, 0, 0, 0., 0, 0) for p in Player.all(tourney.id)]
    if initial_bye_player:
        playerstandings.insert(int(len(playerstandings)/2), (initial_bye_player.id, initial_bye_player.name, 0,0,0,0,0,0.5,0,0))

    return playerstandings






def reportMatchNew(tourneyid, round, player1id, player2id, gameWins1, gameWins2, ties):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    statement = "INSERT INTO  match (tourney_id, round, player1_id, player2_id, player1_score, player2_score, ties) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    data = (tourneyid, round, player1id, player2id, gameWins1, gameWins2, ties)
    cursor.execute(statement, data)
    conn.commit()
    conn.close()


def numPlayed(record):
    """
    number of games played for a player
    :param record: A tuple comprised of 0-id, 1-name, 2-wins, 3-losses, 4-ties
    :return: one per win, one per loss, one per tie, sum of all of these
    """
    return record[2] + record[3] + record[4]


def swissPairingsWithByes(players, standings):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  If odd, one player, who hasn't had a bye yet, gets the bye.
    Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    players are already sorted by win percentage.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    use_bye = len(players) % 2 != 0
    max_played = max(standings, key=lambda item:item[5])[5]
    players_nobye = [(player[0], player[1]) for player in standings if player[5] >= max_played]
    if use_bye:
        bye_number = random.randint(0, len(players_nobye)-1)
        player_bye_id = players_nobye[bye_number][0]
    i = 0
    pairs = []
    for player in standings:
        if (not use_bye or (player[0] != player_bye_id)):
            if i % 2 == 0:
                prevPlayer = player
            else:
                pair = (player[0], player[1], prevPlayer[0], prevPlayer[1])
                pairs.append(pair)
            i += 1
    return pairs

