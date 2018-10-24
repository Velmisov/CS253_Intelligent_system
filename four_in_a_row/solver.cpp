//
// Created by vlad on 07.10.18.
//

#include "solver.h"

#include <map>

bool Solver::gameIsOver(const Position& pos) const {
    return checkForStreak(pos, 1, 4) >= 1 || checkForStreak(pos, 2, 4) >= 1;
}

int Solver::checkForStreak(const Position& pos, int player, int streak) const {
    int count = 0;
    for (int row = 0; row < HEIGHT; ++row) {
        for (int col = 0; col < WIDTH; ++col) {
            if (pos.board[row][col] == player) {
                count += horizontalStreak(row, col, pos, streak);
                count += verticalStreak(row, col, pos, streak);
                count += diagonalStreak(row, col, pos, streak);
            }
        }
    }
    return count;
}

bool Solver::horizontalStreak(int row, int col, const Position& pos, int streak) const {
    int count = 0;
    for (int j = col; j < WIDTH; ++j) {
        if (pos.board[row][j] == pos.board[row][col])
            ++count;
        else
            break;
    }
    return count >= streak;
}

bool Solver::verticalStreak(int row, int col, const Position& pos, int streak) const {
    int count = 0;
    for (int j = row; j < HEIGHT; ++j) {
        if (pos.board[j][col] == pos.board[row][col])
            ++count;
        else
            break;
    }
    return count >= streak;
}

int Solver::diagonalStreak(int row, int col, const Position& pos, int streak) const {
    int result = 0;
    int count = 0;

    int j = col;
    for (int i = row; i < HEIGHT; ++i) {
        if (j > HEIGHT)
            break;
        if (pos.board[i][j] == pos.board[row][col])
            ++count;
        else
            break;
        ++j;
    }

    if (count >= streak)
        ++result;

    count = 0;
    j = col;
    for (int i = row; i >= 0; --i) {
        if (j > HEIGHT)
            break;
        if (pos.board[i][j] == pos.board[row][col])
            ++count;
        else
            break;
        ++j;
    }
    if (count >= streak)
        ++result;

    return result;
}

int Solver::heuristic(const Position &pos, int player) const {
    int opponent = (player == 1 ? 2 : 1);

    int my_4 = checkForStreak(pos, player, 4);
    int my_3 = checkForStreak(pos, player, 3);
    int my_2 = checkForStreak(pos, player, 2);
    int opp_4 = checkForStreak(pos, opponent, 4);

    if (opp_4 > 0)
        return -100000;
    return my_4 * 100000 + my_3 * 100 + my_2;
}

int Solver::bestAlpha(int depth, const Position &pos, int player, int barrier) const {
    if (depth == 0 || gameIsOver(pos))
        return heuristic(pos, player);

    int opponent = (player == 1 ? 2 : 1);

    int alpha = INT32_MIN;
    for (int col = 0; col < WIDTH; ++col) {
        if (!pos.can_move(col))
            continue;

        Position child = pos;
        if(pos.is_winning_move(col)){
            alpha = std::max(alpha, 100000);
        }else{
            child.move(col);
            alpha = std::max(alpha, -bestAlpha(depth - 1, child, opponent, alpha));
        }
        if(-alpha <= barrier) // ACHTUNG!!!
            break;
    }
    return alpha;
}

std::pair<int, int> Solver::bestMove(int depth, const Position &pos, int player) const {
    int opponent = (player == 1 ? 2 : 1);

    std::map<int, int> legal;
    for (int col = 0; col < WIDTH; ++col) {
        if (pos.can_move(col)) {
            Position temp = pos;
            temp.move(col);
            legal[col] = -bestAlpha(depth - 1, temp, opponent, INT32_MIN); // ACHTUNG!!!
        }
    }

    int best_alpha = -999999999;
    int best_move = -1;
    for (auto to : legal) {
        int move = to.first;
        int alpha = to.second;
        if (alpha >= best_alpha) {
            best_alpha = alpha;
            best_move = move;
        }
    }
    return {best_move, best_alpha};
}
