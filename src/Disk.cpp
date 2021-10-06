#include "../include/Disk.hpp"
Disk::Disk(int max_size){
    this -> max_size = max_size;
    qtt_occupied = 0;
    for(int i = 0; i < max_size;i++)
        memory.push_back("");
}
int Disk::FindValidSegment(int size){
    int cont = 0;
    for(unsigned int i = 0; i < memory.size();i++){
        if(i+size < memory.size()){
            if(memory[i] == "")
                for(unsigned int j = i; j < i+size;j++){
                    if(memory[j] == "")
                        cont++;
                    if(cont == size)
                        return i;
                }
        }
        else{
            break;
        }
        cont = 0;
    }
    return -1;
}
string Disk::CreateFile(string name, int initial_block, int size){
    if(max_size-qtt_occupied < size)
        return "Não pode criar o arquivo "+name+" (falta de espaço) .";
    else{
        if(initial_block > max_size-1 || initial_block < 0)
            return "Não pode criar o arquivo "+name+" (bloco inicial ocupado) .";
        else if(initial_block + size > max_size)
            return "Não pode criar o arquivo "+name+" (quantidade de blocos insuficientes no disco) .";
        else if(size < 0)
            return "Não pode criar o arquivo "+name+" (quantidade de blocos invalida, numero negativo) .";
        else if(initial_block < 0)
            return "Não pode criar o arquivo "+name+" (falta de espaço) .";
        else{
            vector<string> invalid;
            vector<string> valid;
            for(int i = initial_block;i < initial_block+size;i++){
                if(memory[i] != "")
                    invalid.push_back(to_string(i));
                else
                    valid.push_back(to_string(i));   
            }
            if(!invalid.empty()){
                if(invalid.size() == 1){
                    return "Não pode criar o arquivo "+name+" (bloco "+invalid[0]+" ocupado) .";
                }
                else{
                    string ret = "";
                    ret+= invalid[0];
                    for(unsigned i = 1; i<invalid.size()-1;i++){
                        ret+= ", "+invalid[i];
                    }
                    ret +=  " e " + invalid[invalid.size()-1];
                    return "Não pode criar o arquivo "+name+" (blocos "+ret+" ocupados) .";
                }
            }
            else{
                for(auto i : valid)
                    memory[stoi(i)] = name;
                if(valid.size() == 1)
                    return "Criou o arquivo "+name+" (bloco "+valid[0]+") .";
                else{
                    string ret = "";
                    ret+= valid[0];
                    for(unsigned i = 1; i<valid.size()-1;i++)
                        ret+= ", "+valid[i];
                    ret +=  " e " + valid[valid.size()-1];
                    return "Criou o arquivo "+name+" (blocos "+ret+") .";
                }
            }
        }
    }
}
string Disk::DeleteFile(string name){
    bool nameFound = false;
    for (unsigned int i = 0; i < memory.size();i++){
        if(memory[i] == name){
            memory[i] = "";
            nameFound = true;
        }
    }
    if(!nameFound)
        return "Não pode deletar o arquivo "+name+" porque ele não existe.";
    return "Deletou o arquivo X";
}