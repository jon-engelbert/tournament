#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")
    statementA = "Create View winner As " \
                 "Select player.id as id, player.name as name, count(match.player1_score) as wins " \
                 "from player left join match on (player.id = match.player1_id)  group by player.id order by wins DESC"
    statementB = "Create View loser As " \
                 "select player.id as id, player.name as name, count(match.player2_score) as losses " \
                 "from player left join match on (player.id = match.player2_id)  group by player.id order by losses"
    cursor.execute(statementA)
    cursor.execute(statementB)


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    statement = "DELETE FROM match"
    cursor.execute(statement)
    conn.commit()
    conn.close()



def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    statement = "DELETE FROM player"
    cursor.execute(statement)
    conn.commit()
    conn.close()

def deleteTourneys():
    """Remove all the tournament records from the database."""
    conn = connect()
    cursor = conn.cursor()
    statement = "DELETE FROM tournament"
    cursor.execute(statement)
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


def registerPlayer(_name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    statement = "INSERT INTO  player (name) VALUES (%s)"
    data = (_name,)
    cursor.execute(statement, data)
    conn.commit()
    conn.close()

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
    #statement = "select player.id, player.name, wins, count(match.player2_id) as losses from player left join (select player.id, count(match.player1_id) as wins from player left join match on (player.id = match.player1_id)  group by player.id order by wins) on player.id = match.player2_id  group by player.id"
    #statement1 = "select player.id, player.name, count(match.player1_id) as wins, count(player.id) as matches from player left join match on (player.id = match.player1_id or player.id = match.player2_id) group by player.id"
    statement2 = "select player.id, player.name, count(match.player1_score) as wins, 0 " \
                 "from player left join match on (player.id = match.player1_id)  group by player.id order by wins DESC"
    statement3 = "select player.id, player.name, count(match.player2_score) as losses, 0 " \
                 "from player left join match on (player.id = match.player2_id)  group by player.id order by losses"
    statement = "Select winner.id, winner.name, winner.wins, winner.wins + loser.losses from winner left join loser on (winner.id = loser.id) group by winner.id, winner.name, winner.wins, loser.losses order by winner.wins DESC"
    #statement = "Select winner.id, winner.wins + loser.losses from winner left join loser on (winner.id = loser.id) group by winner.id, winner.wins, loser.losses"
    statement_big = "Select winner.id, winner.wins + loser.losses from winner left join loser on (winner.id = loser.id) group by winner.id, winner.wins, loser.losses"
    cursor.execute(statement)
    results = cursor.fetchall()
    for res_id, res_name, res_wins, res_total in results:
        print("winner: %s, wins: %s, total: %s" % (res_name, res_wins, res_total))
    return results

    # cursor.execute(statement2)
    # results2 = cursor.fetchall()
    # cursor.execute(statement3)
    # results3 = cursor.fetchall()
    #
    # for res_id, res_name, res_wins, res_none in results2:
    #     print("winner: %s, wins: %s" % (res_name, res_wins))
    # win_maps = {res_id : [res_id, res_name, res_wins, 0] for res_id, res_name, res_wins, res_none in results2}
    # loss_maps = {res_id : res_losses for res_id, res_name, res_losses, res_none in results3}
    # print("win_maps, then loss_maps")
    # print(win_maps)
    # print(loss_maps)
    # for key, value in win_maps.iteritems():
    #     losses = loss_maps[key]
    #     if losses == None:
    #         losses = 0
    #
    #     name = value[1]
    #     wins = value[2]
    #     if wins == None:
    #         wins = 0
    #     win_maps[key][2] = wins
    #     print("name losses: %s %s" % (name, losses))
    #     print("name wins: %s %s" % (name, wins))
    #     win_maps[key][3] = wins + losses
    #     print("name matches: %s %s" % (name, win_maps[key][3]))
    #
    # conn.commit()
    # conn.close()
    # print("player standings wins")
    # print(sorted(win_maps.values(), key= lambda win: win[2]))
    # print("player standings losses")
    # print(results3)
    # return sorted(win_maps.values(), key= lambda win: win[2])



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