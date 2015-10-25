#include<stdio.h>
#include<string.h>
#include<stdlib.h>

int main(int argc, char* argv[]){
	int total_files=0;
	int i=0;

	if(argc < 2){
		printf("Filename not specified. Retry.\n");
		return 0;	
	}
	int total_files = argc-1;
	for(i=1;i<=total_files;i++){
		
	}	
	return 0;
}
