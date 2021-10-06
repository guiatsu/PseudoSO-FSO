#ifndef DISK_HPP
#define DISK_HPP
#include <iostream>
#include <vector>
#include "File.hpp"
using namespace std;
class Disk{
    public:
    int max_size;
    vector<string> memory;
    int qtt_occupied;
    Disk(int max_size);
    string CreateFile(string name, int initial_block, int size);
    string DeleteFile(string name);
    int FindValidSegment(int size);
};

#endif