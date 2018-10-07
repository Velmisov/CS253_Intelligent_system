//
// Created by vlad on 07.10.18.
//

#include "solver.h"


int Solver::negamax(const Position& pos, int alpha, int beta) {
    ++number_of_explored_nodes;

    if(pos.get_number_of_moves() == BOARD_SIZE)
        return 0;

    for(int x = 0; x < WIDTH; x++) {
        if (pos.is_winning_move(x))
            return (BOARD_SIZE + 1 - pos.get_number_of_moves()) / 2;
    }

    int max = (BOARD_SIZE - 1 - pos.get_number_of_moves()) / 2;	// upper bound of our score as we cannot win immediately
    if(beta > max) {
        beta = max;                     // there is no need to keep beta above our max possible score.
        if(alpha >= beta)
            return beta;  // prune the exploration if the [alpha;beta] window is empty.
    }

    for(int x = 0; x < WIDTH; x++) {// compute the score of all possible next move and keep the best one
        if (pos.can_move(x)) {
            Position P2(pos);
            P2.move(x);               // It's opponent turn in P2 position after current player plays x column.
            int score = -negamax(P2, -beta, -alpha); // explore opponent's score within [-beta;-alpha] windows:
            // no need to have good precision for score better than beta (opponent's score worse than -beta)
            // no need to check for score worse than alpha (opponent's score worse better than -alpha)

            if (score >= beta)
                return score;  // prune the exploration if we find a possible move better than what we were looking for.
            if (score > alpha)
                alpha = score; // reduce the [alpha;beta] window for next exploration, as we only
            // need to search for a position that is better than the best so far.
        }
    }

    return alpha;
}
