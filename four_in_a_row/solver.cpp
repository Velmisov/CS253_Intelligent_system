//
// Created by vlad on 07.10.18.
//

#include "solver.h"


std::pair<int, int> Solver::negamax(const Position& pos, int alpha, int beta) {
    ++number_of_explored_nodes;

    if(pos.get_number_of_moves() == BOARD_SIZE)
        return { 0, 0 };

    for(int x = 0; x < WIDTH; x++) {
        if (pos.is_winning_move(x))
            return { x, 1 };
    }

    int max = (BOARD_SIZE - 1 - pos.get_number_of_moves()) / 2;	// upper bound of our score as we cannot win immediately
    if(beta > max) {
        beta = max;                     // there is no need to keep beta above our max possible score.
        if(alpha >= beta)
            return { -1, beta };  // prune the exploration if the [alpha;beta] window is empty.
    }

    for(int x = 0; x < WIDTH; x++) {// compute the score of all possible next move and keep the best one
        if (pos.can_move(x)) {
            Position P2(pos);
            P2.move(x);               // It's opponent turn in P2 position after current player plays x column.
            auto result = negamax(P2, -beta, -alpha);
            int score = -result.second; // explore opponent's score within [-beta;-alpha] windows:
            // no need to have good precision for score better than beta (opponent's score worse than -beta)
            // no need to check for score worse than alpha (opponent's score worse better than -alpha)

            if (score >= beta)
                return { x, score };  // prune the exploration if we find a possible move better than what we were looking for.
            if (score > alpha)
                alpha = score; // reduce the [alpha;beta] window for next exploration, as we only
            // need to search for a position that is better than the best so far.
        }
    }

    return { -1, alpha };
}

int Solver::calc() {
    for (int row = 0; row < HEIGHT; ++row) {
        for (int col = 0; col < WIDTH - 3; ++col) {
            for (int i = 0; i < 4; ++i) {
                heur[row][col]++;
            }
        }
    }

    for (int row = 0; row < HEIGHT - 3; ++row) {
        for (int col = 0; col < WIDTH; ++col) {
            for (int i = 0; i < 4; ++i) {
                heur[row][col]++;
            }
        }
    }

    for (int row = 0; row < HEIGHT; ++row) {
        for (int col = 0; col < WIDTH; ++col) {
            if (row + 3 < HEIGHT && col + 3 < WIDTH) {
                for (int i = 0; i < 4; ++i) {
                    ++heur[row + i][col + i];
                }
            }
            if (row + 3 < HEIGHT && col - 3 >= 0) {
                for (int i = 0; i < 4; ++i) {
                    ++heur[row + i][col - i];
                }
            }
        }
    }
}

int Solver::heuristic() const {

}
