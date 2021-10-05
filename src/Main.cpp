#include "../include/File.hpp"
#include <iostream>
int main(int argc, char** argv)
{
    vector<vector<string>> file = read_file("assets/processes.txt");
    for (auto i : file){
        for(auto j : i){
            cout << j << " ";
        }
        cout << endl;
    }
    return 0;
}
