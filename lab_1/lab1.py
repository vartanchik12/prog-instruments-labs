class TennisGameDefactored1:
    """
    A class representing a tennis game, tracking players' scores and providing the current score.
    """

    def __init__(self, player1_name: str, player2_name: str) -> None:
        """
        Initializes the game with player names and sets initial scores to zero.

        Args:
            player1_name (str): Name of the first player.
            player2_name (str): Name of the second player.
        """
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.p1_points = 0
        self.p2_points = 0

    def won_point(self, player_name: str) -> None:
        """
        Increases the score of the player who won the point.

        Args:
            player_name (str): Name of the player who won the point.
        """
        if player_name == self.player1_name:
            self.p1_points += 1
        else:
            self.p2_points += 1

    def score(self) -> str:
        """
        Calculates and returns the current score of the game in tennis scoring format.

        Returns:
            str: The current score in terms of "Love", "Fifteen", "Thirty", "Forty",
                 "Deuce", "Advantage", or "Win".
        """
        result = ""
        temp_score = 0

        if self.p1_points == self.p2_points:
            result = {
                0: "Love-All",
                1: "Fifteen-All",
                2: "Thirty-All",
                3: "Forty-All",
            }.get(self.p1_points, "Deuce")
        elif self.p1_points >= 4 or self.p2_points >= 4:
            minus_result = self.p1_points - self.p2_points
            if minus_result == 1:
                result = "Advantage " + self.player1_name
            elif minus_result == -1:
                result = "Advantage " + self.player2_name
            elif minus_result >= 2:
                result = "Win for " + self.player1_name
            else:
                result = "Win for " + self.player2_name
        else:
            for i in range(1, 3):
                if i == 1:
                    temp_score = self.p1_points
                else:
                    result += "-"
                    temp_score = self.p2_points
                result += {
                    0: "Love",
                    1: "Fifteen",
                    2: "Thirty",
                    3: "Forty",
                }[temp_score]

        return result


class TennisGameDefactored2:
    """
    A class to track points in a tennis game with additional methods for handling
    score setting and calculation.
    """

    def __init__(self, player1_name: str, player2_name: str) -> None:
        """
        Initializes the game with player names and sets initial scores to zero.

        Args:
            player1_name (str): Name of the first player.
            player2_name (str): Name of the second player.
        """
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.p1_points = 0
        self.p2_points = 0

    def won_point(self, player_name: str) -> None:
        """
        Increases the score of the player who won the point.

        Args:
            player_name (str): Name of the player who won the point.
        """
        if player_name == self.player1_name:
            self.p1_score()
        else:
            self.p2_score()

    def score(self) -> str:
        """
        Returns the current score of the game using tennis score terminology.

        Returns:
            str: The current score of the game, including special cases for "Deuce",
                 "Advantage", and "Win".
        """
        result = ""

        if self.p1_points == self.p2_points and self.p1_points < 4:
            result = ["Love", "Fifteen", "Thirty", "Forty"][self.p1_points] + "-All"
        elif self.p1_points == self.p2_points and self.p1_points >= 3:
            result = "Deuce"
        else:
            p1_res = ["Love", "Fifteen", "Thirty", "Forty"][self.p1_points] if self.p1_points < 4 else ""
            p2_res = ["Love", "Fifteen", "Thirty", "Forty"][self.p2_points] if self.p2_points < 4 else ""
            if self.p1_points > self.p2_points and self.p1_points >= 4:
                result = "Advantage " + self.player1_name
            elif self.p2_points > self.p1_points and self.p2_points >= 4:
                result = "Advantage " + self.player2_name
            elif self.p1_points >= 4 and self.p1_points - self.p2_points >= 2:
                result = "Win for " + self.player1_name
            elif self.p2_points >= 4 and self.p2_points - self.p1_points >= 2:
                result = "Win for " + self.player2_name
            else:
                result = p1_res + "-" + p2_res

        return result

    def set_p1_score(self, number: int) -> None:
        """
        Sets the score for player 1.

        Args:
            number (int): The number of points to add to player 1's score.
        """
        for _ in range(number):
            self.p1_score()

    def set_p2_score(self, number: int) -> None:
        """
        Sets the score for player 2.

        Args:
            number (int): The number of points to add to player 2's score.
        """
        for _ in range(number):
            self.p2_score()

    def p1_score(self) -> None:
        """Increases player 1's score by one point."""
        self.p1_points += 1

    def p2_score(self) -> None:
        """Increases player 2's score by one point."""
        self.p2_points += 1


class TennisGameDefactored3:
    """
    A class representing a tennis game with an optimized scoring system.
    """

    def __init__(self, player1_name: str, player2_name: str) -> None:
        """
        Initializes the game with player names and sets initial scores to zero.

        Args:
            player1_name (str): Name of the first player.
            player2_name (str): Name of the second player.
        """
        self.p1_name = player1_name
        self.p2_name = player2_name
        self.p1 = 0
        self.p2 = 0

    def won_point(self, n: str) -> None:
        """
        Increases the score of the player who won the point.

        Args:
            n (str): Name of the player who won the point.
        """
        if n == self.p1_name:
            self.p1 += 1
        else:
            self.p2 += 1

    def score(self) -> str:
        """
        Returns the current score of the game using tennis terminology.

        Returns:
            str: The current score, including special cases for "Deuce", "Advantage", and "Win".
        """
        points = ["Love", "Fifteen", "Thirty", "Forty"]

        if self.p1 < 4 and self.p2 < 4 and self.p1 + self.p2 < 6:
            if self.p1 == self.p2:
                return f"{points[self.p1]}-All"
            else:
                return f"{points[self.p1]}-{points[self.p2]}"

        if self.p1 == self.p2:
            return "Deuce"

        if abs(self.p1 - self.p2) == 1:
            return f"Advantage {self.p1_name if self.p1 > self.p2 else self.p2_name}"

        return f"Win for {self.p1_name if self.p1 > self.p2 else self.p2_name}"
