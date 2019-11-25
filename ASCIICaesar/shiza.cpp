#include <iostream>
#include <stdio.h>
#include <string.h>
#include <locale.h>
using namespace std;

void decoder(int, string);

int main(int argc, char argv[])
{
	setlocale(LC_ALL, "RUS");
	int end = 1, k = 0;
	string dword = "!4B?42CNC74N?0BCZN2A40C4NC74N5DCDA4";
	while (end != 0)
	{
		decoder(k, dword);
		k++;
		cout << "End rotation? YES(0)/NO(1)" << endl;
		cin >> end;
	}
	return 0;
}

void decoder(int key, string word)
{
	int t = word.size();
	for (int i = 0; i < t; i++)
	{
		word[i] = word[i] - 32;
		if ((word[i] - key) < 32)
		{
			word[i] = (word[i] - key) + 95;
		}
		else if ((word[i] - key) > 126)
		{
			word[i] = (word[i] - key) - 95;
		}
		else
			word[i] = word[i] - key;
	}
	for (int j = 0; j < t; j++)
		cout << word[j];
	cout << endl;
}
