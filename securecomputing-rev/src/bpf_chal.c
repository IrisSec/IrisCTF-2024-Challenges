#include <unistd.h>
#include <linux/seccomp.h>  /* Definition of SECCOMP_* constants */
#include <linux/filter.h>   /* Definition of struct sock_fprog */
#include <sys/ptrace.h>     /* Definition of PTRACE_* constants */
#include <sys/syscall.h>    /* Definition of SYS_* constants */
#include <sys/prctl.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>

#include "bpf_chal_filters.c"

__attribute__((constructor(0))) void seccomp() {
    // Just a bit
    if (ptrace(PTRACE_TRACEME, 0) < 0) { return; }
    
    prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
    for(int i = 0; i < 
#include "bpf_chal_cnt.txt"
    ; i++) {
        struct sock_fprog filter = { filter_len[i], filters[i] };
        syscall(SYS_seccomp, SECCOMP_SET_MODE_FILTER, 0, &filter);
    }
}

// gcc -s -O3 -Wall

int main() {
    printf("Guess: ");
    char flag[49+8+1] = {0};
    if(scanf("%57s", flag) != 1 || strlen(flag) != 57 || strncmp(flag, "irisctf{", 8) != 0 || strncmp(flag + 56, "}", 1)) {
        printf("Guess harder\n");
        return 0;
    }
#define flg(n) *((__uint64_t*)((flag+8))+n)
    syscall(0x1337, flg(0), flg(1), flg(2), flg(3), flg(4), flg(5));
    printf("Maybe? idk bro\n");

    return 0;
}

