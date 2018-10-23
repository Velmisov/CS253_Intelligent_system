#include <iostream>
#include "position.h"
#include "solver.h"
using namespace std;


const int DEPTH = 8;

int main() {

    //auto pos = new Position("333333444444");
    auto pos = new Position("");
    pos->show();

    auto solver = new Solver();

    int player;
    do {
        cout << "Choose number of player (1 or 2): ";
        cin >> player;
        if (player == 1 || player == 2)
            break;
        cout << "Retry" << endl;
    } while (true);

    while (pos->number_of_moves != BOARD_SIZE) {
        int col;
        if (pos->who_play_now() != player) {
            clock_t FOR_CLOCK = clock();
            auto res = solver->bestMove(DEPTH, *pos, pos->who_play_now());

            cout << "Time spent: " << double(clock() - FOR_CLOCK) / CLOCKS_PER_SEC << " seconds" << endl;
            cout << res.first + 1 << " " << res.second << endl;
            col = res.first;

            if (pos->is_winning_move(col)) {
                pos->move(col);
                pos->show();
                cout << "Computer won ¯\\_(ツ)_/¯" << endl;
                break;
            }
        }
        else {
            do {
                cout << "Choose your column: ";
                cin >> col;
                --col;
                if (pos->can_move(col)) {
                    break;
                } else {
                    cout << "Invalid column! Try again!" << endl;
                }
            } while (true);
            if (pos->is_winning_move(col)) {
                pos->move(col);
                pos->show();
                cout << "You won!" << endl;
                break;
            }
        }
        pos->move(col);
        pos->show();
    }

    return 0;
}
