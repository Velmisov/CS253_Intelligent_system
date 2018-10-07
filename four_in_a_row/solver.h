//
// Created by vlad on 07.10.18.
//

#ifndef FOUR_IN_A_ROW_SOLVER_H
#define FOUR_IN_A_ROW_SOLVER_H


#include "position.h"

class Solver {
    unsigned long long number_of_explored_nodes;

public:
    int negamax(const Position& pos, int alpha=-1, int beta=1);
};


#endif //FOUR_IN_A_ROW_SOLVER_H
