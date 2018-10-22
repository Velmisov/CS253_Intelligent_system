//
// Created by vlad on 07.10.18.
//

#include "position.h"

#include <iostream>
using namespace std;


Position::Position(): board{0}, filled{0}, number_of_moves(0) {}

Position::Position(string field): board{0}, filled{0}, number_of_moves(0) {
    for (auto step : field) {
        move(step - '1');
    }
}

int Position::get_number_of_moves() const {
    return number_of_moves;
}

bool Position::can_move(int column) const {
    return filled[column] < HEIGHT;
}

void Position::move(int column) {
    board[filled[column]][column] = 1 + (number_of_moves % 2);
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

    if (filled[column] >= 3 && board[filled[column] - 1][column] == current_player &&
        board[filled[column] - 2][column] == current_player &&
        board[filled[column] - 3][column] == current_player)
        return true;


    for(int dy = -1; dy <=1; dy++) {
        int surroundings = 0;
        for(int dx = -1; dx <=1; dx += 2) {
            for (int x = column + dx, y = filled[column] + dx * dy; in_border(x) && in_border(y) && board[y][x] == current_player;) {
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

void Position::show() const {
    cout << endl;
    for (int row = 0; row < HEIGHT; ++row) {
        for (int col = 0; col < WIDTH; ++col) {
            cout << board[HEIGHT - row - 1][col] << " ";
        }
        cout << endl;
    }
}

int Position::who_play_now() const {
    return (number_of_moves % 2 ? 2 : 1);
}
