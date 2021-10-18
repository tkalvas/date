#ifndef DATE_H_INCLUDED
#define DATE_H_INCLUDED

#include <stdint.h>

struct tk_instant {
  int_fast32_t year;
  int_fast64_t day_number;
  uint_least16_t day_of_year;
  uint_least8_t week;
  uint_least8_t weekday;
  uint_least8_t month;
  uint_least8_t day;
  uint_least8_t hour;
  uint_least8_t minute;
  uint_least8_t second;
  uint_least32_t day_seconds;
  uint_least32_t nanos;
  uint_least8_t tz_hour;
  uint_least8_t tz_minute;
};

int parse_iso8601_instant(
  const char *source, int length,
  struct tk_instant *instant);

int parse_iso8601_instant_asciiz(
  const char *source,
  struct tk_instant *instant);

#endif
