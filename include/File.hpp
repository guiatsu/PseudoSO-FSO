#ifndef FILE_HPP
#define FILE_HPP
#define INCLUDE_SDL
#define INCLUDE_SDL_MIXER
#include <iostream>
#include <fstream>
#include <vector>
#include <regex>
using namespace std;
vector<string> split_string(string line, string delimiter);
vector<vector<string>> read_file(string path);

#endif