#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *
from Player import *
from Match import *
from Tourney import *
import datetime

def testDeleteAllMatches():
    deleteAllMatches()
    print("1. Old matches can be deleted.")

def testAddPlayers():
    deleteAllPlayers()
    al = Player("Al")
    al.add_to_db()
    c = countPlayers()
    if c != 1:
        raise ValueError("After adding a player, countPlayers should return one.")
    bob = Player("Bob")
    bob.add_to_db()
    c = countPlayers()
    if c != 2:
        raise ValueError("After adding a 2nd player, countPlayers should return two.")
    print("*. Player records can be added.")

def testDeletePlayers():
    deleteAllPlayers()
    al = Player("Al")
    al.add_to_db()
    print("testDeletePlayer, name, id: %s, %d" % (al.name, al.id))
    c = countPlayers()
    if c != 1:
        raise ValueError("After adding a player, countPlayers should return one.")
    bob = Player("Bob")
    bob.add_to_db()
    bob.delete_from_db()
    al.delete_from_db()
    c = countPlayers()
    if c != 0:
        raise ValueError("After removing the only player, countPlayers should return zero.")
    print("*. Player records can be deleted.")

def testAddTourneys():
    deleteAllTournaments()
    mtg1 = Tourney("MTG1", date="2015-02-23")
    mtg1.add_to_db()
    c = countTourneys()
    if c != 1:
        raise ValueError("After adding a tourney, countTourneys should return one.")
    mtg2 = Tourney("MTG2", date="2015-02-24")
    mtg2.add_to_db()
    c = countTourneys()
    if c != 2:
        raise ValueError("After adding a 2nd tournament, countTourneys should return two.")
    print("*. Tourneys records can be added.")

def testDeleteTourneys():
    deleteAllTournaments()
    mtg1 = Tourney("MTG1")
    mtg1.add_to_db()
    c = countTourneys()
    if c != 1:
        raise ValueError("After adding a player, countTourneys should return one.")
    mtg2 = Tourney("MTG2", date="2015-02-24")
    mtg2.add_to_db()
    mtg2.delete_from_db()
    mtg1.delete_from_db()
    c = countTourneys()
    if c != 0:
        raise ValueError("After removing the only countTourneys, countPlayers should return zero.")
    print("*. Tourneys records can be deleted.")

def testAddMatches():
    deleteAllTournaments()
    deleteAllPlayers()
    mtg1 = Tourney("MTG1", date="2015-02-23")
    mtg1.add_to_db()
    al = Player("Al")
    al.add_to_db()
    bob = Player("Bob")
    bob.add_to_db()
    match1 = Match(player1_id=al.id, player2_id=bob.id, tourney_id=mtg1.id, round=1, player1_score=1, player2_score=0, ties=0)
    match1.add_to_db()
    c = countMatches()
    if c != 1:
        raise ValueError("After adding a match, countMatches should return one.")
    cat = Player("Cat")
    cat.add_to_db()
    match2 = Match(player1_id=al.id, player2_id=cat.id, tourney_id=mtg1.id, round=1, player1_score=1, player2_score=0, ties=0)
    match2.add_to_db()
    c = countMatches()
    if c != 2:
        raise ValueError("After adding a 2nd match, countMatches should return two.")
    print("*. Matches records can be added.")

def testDeleteMatches():
    deleteAllMatches()
    deleteAllTournaments()
    deleteAllPlayers()
    mtg1 = Tourney("MTG1", date="2015-02-23")
    mtg1.add_to_db()
    al = Player("Al")
    al.add_to_db()
    bob = Player("Bob")
    bob.add_to_db()
    match1 = Match(player1_id=al.id, player2_id=bob.id, tourney_id=mtg1.id, round=1, player1_score=1, player2_score=0, ties=0)
    match1.add_to_db()
    cat = Player("Cat")
    cat.add_to_db()
    match2 = Match(player1_id=al.id, player2_id=cat.id, tourney_id=mtg1.id, round=1, player1_score=1, player2_score=0, ties=0)
    match2.add_to_db()

    match2.delete_from_db()
    match1.delete_from_db()
    c = countMatches()
    if c != 0:
        raise ValueError("After removing the only countMatches, countPlayers should return zero.")
    print("*. Matches records can be deleted.")

def testDelete():
    deleteAllMatches()
    deleteAllPlayers()
    print("2. Player and match records can be deleted.")


def testCount():
    deleteAllMatches()
    deleteAllPlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print("3. After deleting, countPlayers() returns zero.")


def testRegister():
    deleteAllMatches()
    deleteAllPlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print("4. After registering a player, countPlayers() returns 1.")


def testRegisterCountDelete():
    deleteAllMatches()
    deleteAllPlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deleteAllPlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print("5. Players can be registered and deleted.")


def testStandingsBeforeMatches():
    deleteAllMatches()
    deleteAllPlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    print(countPlayers())
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print("6. Newly registered players appear in the standings with no matches.")


def testReportMatches():
    deleteAllMatches()
    deleteAllPlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print("7. After a match, players have updated standings.")


def testPairings():
    deleteAllMatches()
    deleteAllPlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print("8. After one match, players with one win are paired.")


if __name__ == '__main__':
    testDeleteAllMatches()
    testDelete()
    testAddPlayers()
    testDeletePlayers()
    testAddTourneys()
    testDeleteTourneys()
    testAddMatches()
    testDeleteMatches()

    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print("Success!  All tests pass!")
