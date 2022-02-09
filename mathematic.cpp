#include <iostream>
#include <vector>
#include <string>
#include <cmath>
using namespace std;
 

bool operation(char c){
    return c=='+' || c=='-' || c=='*' ||  c=='/' || c=='^';
}
 

int prioritet(char op){ 
    if(op<0) return 3;
    else{
        if(op == '+' || op == '-')return 1;
        else if(op == '*' || op == '/' )return 2;
        else if(op == '^')return 4;
        else return -1;
    }
}
 
void action(vector<long> &value, char op){
    if(op<0){
        long unitar=value.back();
        value.pop_back();
        if(-op=='-')value.push_back(-unitar);
    }
    else{
        long right = value.back();
        value.pop_back();
        long left = value.back();
        value.pop_back();
        if(op=='+')value.push_back(left+right);
        else if(op=='-')value.push_back(left-right);
        else if(op=='*')value.push_back(left*right);
        else if(op=='/')value.push_back(left/right);
        else if(op=='^')value.push_back(pow(left,right));
    }
}
 
long main_calculator(string &formula){
    bool unary=true;
    vector<long>value;
    vector<char>op;
    for(int i=0; i<formula.size(); i++){
            if(formula[i]=='('){
                op.push_back('(');  
                unary=true;
            }
            else if(formula[i]==')'){
                while(op.back()!='('){
                    action(value, op.back());
                    op.pop_back();
                }
                op.pop_back();
                unary=false;
            }
            else if(operation(formula[i])){
                char zn=formula[i];
                if(unary==true)zn=-zn;
                while(!op.empty() && prioritet(op.back())>=prioritet(zn)){
                    action(value, op.back()); 
                    op.pop_back();
                }
                op.push_back(zn);
                unary=true;
            }
            else{
                string number;
                while(i<formula.size() && isdigit(formula[i]))number+=formula[i++];
                i--;
                value.push_back(atol(number.c_str()));
                unary=false;
            }
        }
    while(!op.empty()){   
        action(value, op.back());
        op.pop_back();
    }
    return value.back();
}


int start_calculate(string formula, string x){
    string old_form = formula;
    if(x[0]=='-'){
        x.insert(x.begin(),'(');
        x.insert(x.end(),')');
    }
    int size=2*formula.size();
    for(int i=0; i<size; i++){
        if(formula[i]=='x'){
            int b = i -1;
            if(formula[0]=='x'){
                formula.erase(i,1);
                formula.insert(i,x);
            }else if(formula[0]!='x' && formula[b]=='-' || formula[b]=='+'|| formula[b]=='/'|| formula[b]=='*'|| formula[b]=='^'){
                formula.erase(i,1);
                formula.insert(i,x);
            }else{
                formula.erase(i,1);
                formula.insert(i,"*"+x);
            }
        }else if(formula[i]=='e'){
            const string e = "2,72";
            formula.erase(i,1);
            formula.insert(i,"*"+e);
        }
    }
    // cout << formula;
    cout << "Выражение: " << old_form << "=" << main_calculator(formula) << endl;
    return 0;
        
}

string remove_spaces(string formula)
{
    int length = formula.length();
    for (int i = 0; i < length; i++) {
        if(formula[i] == ' '){
            formula.erase(i, 1);
            length--;
            i--;
        }
    }
    return formula;
}

int main() {
    string formula,x;
    int q = 0;
    getline(cin, formula);
    if(formula.length()>200){
        cout << "Выражение должно содаржать 200 символов или менее. У вас " << formula.length() << endl;
    }else{
        int length = formula.length();
        for (int i = 0; i < length; i++) {
            if(formula[i] == 'x'){
                q+=1;
            }
        }
        if(q>0){
            cin >> x;
            string formula_wno_spaces = remove_spaces(formula);
            start_calculate(formula_wno_spaces, x);
        }else{
            string x = "1";
            string formula_wno_spaces = remove_spaces(formula);
            start_calculate(formula_wno_spaces, x);
        }
        
    }
   return 0; 
}