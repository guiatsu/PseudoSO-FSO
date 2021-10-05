#include "../include/File.hpp"
vector<string> split_string(string line, string delimiter){
	regex space("[^"+delimiter+"]+");
	vector<string> splitted_line;
	auto line_begin = sregex_iterator(line.begin(),line.end(),space);
	auto line_end = sregex_iterator();
	for(sregex_iterator j = line_begin; j != line_end; j++){
		smatch match = *j;
		splitted_line.push_back(match.str());
	}
	return splitted_line;
}
vector<vector<string>> read_file(string path){
    fstream File;
    File.open(path,ios::in);
    string line;
    vector<string> splitted_line;
    vector<vector<string>> file;
    while(getline(File,line)){
        if(line != ""){
            splitted_line = split_string(line,", ");
            file.push_back(splitted_line);
            
        }
    }
    File.close();
    return file;
}
