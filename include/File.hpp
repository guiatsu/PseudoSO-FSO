#ifndef FILE_HPP
#define FILE_HPP
#include <iostream>
#include <fstream>
#include <vector>
#include <regex>
using namespace std;
enum op{CREATE,DELETE};
vector<string> split_string(string line, string delimiter);
vector<vector<string>> read_file(string path);

#endif