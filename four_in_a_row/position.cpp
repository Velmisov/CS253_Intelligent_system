//
// Created by vlad on 07.10.18.
//

#include "position.h"


Position::Position(): board{0}, filled{0}, number_of_moves(0) {}


int Position::get_number_of_moves() const {
    return number_of_moves;
}

bool Position::can_move(int column) const {
    return filled[column] < HEIGHT;
}

void Position::move(int column) {
    board[column][filled[column]] = 1 + (number_of_moves % 2);
    ++filled[column];
    ++number_of_moves;
}

bool Position::in_border(int column) const {
    return column >= 0 && column < WIDTH;
}

bool Position::is_winning_move(int column) const {
    if (!can_move(column))
        return false;

    int current_player = 1 + (number_of_moves % 2);

    if (filled[column] >= 3 && board[column][filled[column] - 1] == current_player &&
        board[column][filled[column] - 2] == current_player &&
        board[column][filled[column] - 3] == current_player)
        return true;


    for(int dy = -1; dy <=1; dy++) {
        int surroundings = 0;
        for(int dx = -1; dx <=1; dx += 2) {
            for (int x = column + dx, y = filled[column] + dx * dy; in_border(x) && in_border(y) && board[x][y] == current_player;) {
                x += dx;
                y += dx * dy;
                ++surroundings;
            }
        }
        if(surroundings >= 3)
            return true;
    }
    return false;
}
