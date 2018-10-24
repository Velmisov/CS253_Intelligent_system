//
// Created by vlad on 07.10.18.
//

#include "position.h"

#include <iostream>
using namespace std;


Position::Position(): board{0}, filled{0}, number_of_moves(0), last_move(-1) {}

Position::Position(string field): board{0}, filled{0}, number_of_moves(0), last_move(-1) {
    for (auto step : field) {
        move(step - '1');
    }
}

bool Position::can_move(int column) const {
    return filled[column] < HEIGHT;
}

void Position::move(int column) {
    board[filled[column]][column] = 1 + (number_of_moves % 2);
    ++filled[column];
    ++number_of_moves;
    last_move = column;
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
    int last_col = last_move;
    int last_row = last_move >= 0 ? filled[last_move]-1 : -1;

    cout << endl;
    for (int row = HEIGHT-1; row >= 0; --row) {
        if(row == last_row && 0 == last_col){
            cout << "|-";
        }else{
            cout << "| ";
        }
        for (int col = 0; col < WIDTH; ++col) {
            if (board[row][col])
                cout << board[row][col];
            else
                cout << " ";
            if(row == last_row){
                if(col == last_col)
                    cout << "-| ";
                else if(col == last_col-1)
                    cout << " |-";
                else
                    cout << " | ";
            }else
                cout << " | ";
        }
        cout << endl;
    }
    cout << "--1---2---3---4---5---6---7--" << endl;
}

int Position::who_play_now() const {
    return (number_of_moves % 2 ? 2 : 1);
}
