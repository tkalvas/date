#ifndef DATE_H_INCLUDED
#define DATE_H_INCLUDED

#include <stdint.h>

#define TK_INSTANT_YEAR 1
#define TK_INSTANT_MONTH 2
#define TK_INSTANT_DAY 4
#define TK_INSTANT_HOUR 8
#define TK_INSTANT_MINUTE 16
#define TK_INSTANT_SECOND 32
#define TK_INSTANT_NANOS 64
#define TK_INSTANT_WEEK_YEAR 128
#define TK_INSTANT_WEEK 256
#define TK_INSTANT_WEEKDAY 512
#define TK_INSTANT_DAY_OF_YEAR 1024
#define TK_INSTANT_DAY_NUMBER 2048
#define TK_INSTANT_DAY_SECONDS 4096
#define TK_INSTANT_TZ_MINUTE 8192

struct tk_instant {
  int_fast32_t year;
  int_fast64_t day_number;
  int_least16_t day_of_year;
  int_fast32_t week_year;
  uint_least8_t week;
  uint_least8_t weekday;
  uint_least8_t month;
  uint_least8_t day;
  uint_least8_t hour;
  uint_least8_t minute;
  uint_least8_t second;
  uint_least32_t day_seconds;
  uint_least32_t nanos;
  int_least16_t tz_minute;
  int_fast16_t flags;
};

int parse_iso8601_instant(
  const char *source, int length,
  struct tk_instant *instant);

int parse_iso8601_instant_asciiz(
  const char *source,
  struct tk_instant *instant);

#endif
