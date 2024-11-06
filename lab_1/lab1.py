# -*- coding: utf-8 -*-

class TennisGameDefactored1:
    """
    A class representing a tennis game, tracking players' scores and providing the current score.
    """

    def __init__(self, player1Name, player2Name):
        """
        Initializes the game with player names and sets initial scores to zero.

        Args:
            player1Name (str): Name of the first player.
            player2Name (str): Name of the second player.
        """
        self.player1Name = player1Name
        self.player2Name = player2Name
        self.p1points = 0
        self.p2points = 0

    def won_point(self, playerName):
        """
        Increases the score of the player who won the point.

        Args:
            playerName (str): Name of the player who won the point.
        """
        if playerName == self.player1Name:
            self.p1points += 1
        else:
            self.p2points += 1

    def score(self):
        """
        Calculates and returns the current score of the game in tennis scoring format.

        Returns:
            str: The current score in terms of "Love", "Fifteen", "Thirty", "Forty", "Deuce", "Advantage", or "Win".
        """
        result = ""
        tempScore = 0
        if self.p1points == self.p2points:
            result = {
                0: "Love-All",
                1: "Fifteen-All",
                2: "Thirty-All",
                3: "Forty-All",
            }.get(self.p1points, "Deuce")
        elif self.p1points >= 4 or self.p2points >= 4:
            minusResult = self.p1points - self.p2points
            if minusResult == 1:
                result = "Advantage " + self.player1Name
            elif minusResult == -1:
                result = "Advantage " + self.player2Name
            elif minusResult >= 2:
                result = "Win for " + self.player1Name
            else:
                result = "Win for " + self.player2Name
        else:
            for i in range(1, 3):
                if i == 1:
                    tempScore = self.p1points
                else:
                    result += "-"
                    tempScore = self.p2points
                result += {
                    0: "Love",
                    1: "Fifteen",
                    2: "Thirty",
                    3: "Forty",
                }[tempScore]
        return result


class TennisGameDefactored2:
    """
    A class to track points in a tennis game with additional methods for handling score setting and calculation.
    """

    def __init__(self, player1Name, player2Name):
        """
        Initializes the game with player names and sets initial scores to zero.

        Args:
            player1Name (str): Name of the first player.
            player2Name (str): Name of the second player.
        """
        self.player1Name = player1Name
        self.player2Name = player2Name
        self.p1points = 0
        self.p2points = 0

    def won_point(self, playerName):
        """
        Increases the score of the player who won the point.

        Args:
            playerName (str): Name of the player who won the point.
        """
        if playerName == self.player1Name:
            self.P1Score()
        else:
            self.P2Score()

    def score(self):
        """
        Returns the current score of the game using tennis score terminology.

        Returns:
            str: The current score of the game, including special cases for "Deuce", "Advantage", and "Win".
        """
        result = ""
        if self.p1points == self.p2points and self.p1points < 4:
            result = ["Love", "Fifteen", "Thirty", "Forty"][self.p1points] + "-All"
        elif self.p1points == self.p2points and self.p1points >= 3:
            result = "Deuce"
        else:
            P1res = ["Love", "Fifteen", "Thirty", "Forty"][self.p1points] if self.p1points < 4 else ""
            P2res = ["Love", "Fifteen", "Thirty", "Forty"][self.p2points] if self.p2points < 4 else ""
            if self.p1points > self.p2points and self.p1points >= 4:
                result = "Advantage " + self.player1Name
            elif self.p2points > self.p1points and self.p2points >= 4:
                result = "Advantage " + self.player2Name
            elif self.p1points >= 4 and self.p1points - self.p2points >= 2:
                result = "Win for " + self.player1Name
            elif self.p2points >= 4 and self.p2points - self.p1points >= 2:
                result = "Win for " + self.player2Name
            else:
                result = P1res + "-" + P2res
        return result

    def SetP1Score(self, number):
        """
        Sets the score for player 1.

        Args:
            number (int): The number of points to add to player 1's score.
        """
        for i in range(number):
            self.P1Score()

    def SetP2Score(self, number):
        """
        Sets the score for player 2.

        Args:
            number (int): The number of points to add to player 2's score.
        """
        for i in range(number):
            self.P2Score()

    def P1Score(self):
        """Increases player 1's score by one point."""
        self.p1points += 1

    def P2Score(self):
        """Increases player 2's score by one point."""
        self.p2points += 1


class TennisGameDefactored3:
    """
    A class representing a tennis game with an optimized scoring system.
    """

    def __init__(self, player1Name, player2Name):
        """
        Initializes the game with player names and sets initial scores to zero.

        Args:
            player1Name (str): Name of the first player.
            player2Name (str): Name of the second player.
        """
        self.p1N = player1Name
        self.p2N = player2Name
        self.p1 = 0
        self.p2 = 0

    def won_point(self, n):
        """
        Increases the score of the player who won the point.

        Args:
            n (str): Name of the player who won the point.
        """
        if n == self.p1N:
            self.p1 += 1
        else:
            self.p2 += 1

    def score(self):
        """
        Returns the current score of the game using tennis terminology.

        Returns:
            str: The current score, including special cases for "Deuce", "Advantage", and "Win".
        """
        # Define a list of tennis scores
        points = ["Love", "Fifteen", "Thirty", "Forty"]

        # If neither player has won a game, or the score is still close
        if self.p1 < 4 and self.p2 < 4 and self.p1 + self.p2 < 6:
            if self.p1 == self.p2:
                return f"{points[self.p1]}-All"
            else:
                return f"{points[self.p1]}-{points[self.p2]}"

        # Handle Deuce condition (both players have 3 or more points and the score is tied)
        if self.p1 == self.p2:
            return "Deuce"

        # Handle Advantage or Win condition
        if abs(self.p1 - self.p2) == 1:
            return f"Advantage {self.p1N if self.p1 > self.p2 else self.p2N}"

        # If the difference in score is 2 or more, the game is won
        return f"Win for {self.p1N if self.p1 > self.p2 else self.p2N}"
