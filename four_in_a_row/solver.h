//
// Created by vlad on 07.10.18.
//

#ifndef FOUR_IN_A_ROW_SOLVER_H
#define FOUR_IN_A_ROW_SOLVER_H


#include "position.h"

class Solver {
    unsigned long long number_of_explored_nodes;

public:

    Solver(): number_of_explored_nodes(0) {}

    bool gameIsOver(const Position& pos) const;

    int checkForStreak(const Position& pos, int player, int streak) const;

    bool horizontalStreak(int row, int col, const Position& pos, int streak) const;

    bool verticalStreak(int row, int col, const Position& pos, int streak) const;

    int diagonalStreak(int row, int col, const Position& pos, int streak) const;

    int heuristic(const Position &pos, int player) const;

    int bestAlpha(int depth, const Position &pos, int player, int barrier) const;

    std::pair<int, int> bestMove(int depth, const Position &pos, int player) const;
};


#endif //FOUR_IN_A_ROW_SOLVER_H
