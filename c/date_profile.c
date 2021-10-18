#include "date.h"
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
  const char *text = "2021-10-17T18:35:01";
  int length = strlen(text);
  int repeat = 10000000;
  char *buffer = malloc(repeat * length);
  for (int i = 0; i < repeat; i++) {
    memcpy(buffer + i * length, text, length);
  }
  struct timeval tv_start;
  gettimeofday(&tv_start, NULL);
  struct tk_instant instant;
  for (int i = 0; i < repeat; i++) {
    parse_iso8601_instant(buffer + i * length, length, &instant);
  }
  struct timeval tv_end;
  gettimeofday(&tv_end, NULL);
  if (tv_end.tv_usec < tv_start.tv_usec)
    printf("%ld.%06d\n", tv_end.tv_sec - tv_start.tv_sec - 1, 1000000 + tv_end.tv_usec - tv_start.tv_usec);
  else
    printf("%ld.%06d\n", tv_end.tv_sec - tv_start.tv_sec, tv_end.tv_usec - tv_start.tv_usec);
  return 0;
}
