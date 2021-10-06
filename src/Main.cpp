#include "../include/Disk.hpp"
#include <iostream>
int main(int argc, char** argv){
    vector<vector<string>> file = read_file("assets/files.txt");
    Disk *disk = new Disk(stoi(file[0][0]));
    for( int i = 2 ; i < 2+stoi(file[1][0]);i++){
        cout << disk -> CreateFile(file[i][0],stoi(file[i][1]),stoi(file[i][2])) << endl;
    }
    for(unsigned int i = 2+stoi(file[1][0]);i < file.size();i++){
        if(stoi(file[i][1]) == DELETE)
            cout << disk -> DeleteFile(file[i][2]) << endl;
        else
            cout << disk -> CreateFile(file[i][2],disk -> FindValidSegment(stoi(file[i][3])),stoi(file[i][3])) << endl;
    }
    
    return 0;
}
