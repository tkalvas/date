/*
 * The C version of these attempts to be somewhat performant without abandoning
 * readability completely.
 */

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include "date.h"

int tk_error(
  const char *message,
  const char *source,
  int length) {
  fprintf(stderr, "%s\n", message);
  if (source)
    fprintf(stderr, "%.*s\n", length, source);
  else
    fprintf(stderr, "%d\n", length);
  exit(1);
}

int parse_2_digits(
  const char *source, int length) {
  if (length < 2) tk_error("not enough digits", source, length);
  if (!isdigit(source[0]) || !isdigit(source[1]))
    tk_error("not a number", source, 2);
  return 10 * (source[0] - '0') + (source[1] - '0');
}

int parse_3_digits(
  const char *source, int length) {
  if (length < 3) tk_error("not enough digits", source, length);
  if (!isdigit(source[0]) || !isdigit(source[1]) || !isdigit(source[2]))
    tk_error("not a number", source, 3);
  return 100 * (source[0] - '0') + 10 * (source[1] - '0') + (source[2] - '0');
}

int dys[13] = {0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365};

int parse_iso8601_date(
  const char *source, int length,
  struct tk_instant *instant) {
  /* returns number of characters consumed */
  /* yyyy-mm-dd */
  /* +yyyyy-mm-dd */
  /* yyyy-ddd */
  /* yyyy-Www-d */
  int orig_length = length;
  int century;
  int year_in_century;
  int leap;
  if (source[0] == '+') {
    source++;
    length--;
    while (length && isdigit(source[0])) {
      instant->year *= 10;
      instant->year += source[0] - '0';
      source++;
      length--;
    }
  } else {
    century = parse_2_digits(source, length);
    year_in_century = parse_2_digits(source + 2, length - 2);
    if (year_in_century)
      leap = !(year_in_century & 3);
    else
      leap = !(century & 3);
    instant->year = 100 * century + year_in_century;
    instant->flags |= TK_INSTANT_YEAR;
    source += 4;
    length -= 4;
  }
  //instant->day_number = 146097 * (century >> 2) + 36524 * (century & 3) + (year_in_century >> 2) + 365 * year_in_century;
  instant->day_number = (century >> 2) - century + (instant->year >> 2) + 365 * instant->year + 1 - leap;
  if (source[0] != '-') tk_error("bad date separator", source, length);
  if (source[3] == '-') {
    if (length < 6) tk_error("month-day too short", source, length);
    instant->month = parse_2_digits(source + 1, length - 1) - 1;
    instant->day = parse_2_digits(source + 4, length - 4) - 1;
    instant->flags |= TK_INSTANT_MONTH | TK_INSTANT_DAY;
    length -= 6;
    /* 0.49->0.19 (-O3) */
    if (instant->month >= 12)
      tk_error("month number too large", NULL, instant->month);
    int dy = dys[instant->month];
    int maxd = dys[instant->month + 1] - dy;
    if (leap) {
      if (instant->month >= 2) dy++;
      if (instant->month == 2) maxd++;
    }
    if (instant->day >= maxd)
      tk_error("day number too large", NULL, instant->day);
    instant->day_of_year = dy + instant->day;
    instant->day_number += instant->day_of_year;
    /* [0.55] instant->day_number = 365 * instant->year + instant->year / 4 - instant->year / 100 + instant->year / 400 + dy;*/
    instant->flags |= TK_INSTANT_DAY_OF_YEAR | TK_INSTANT_DAY_NUMBER;
  } else if (source[1] == 'W') {
    instant->week_year = instant->year;
    if (length < 6) tk_error("weeknumber-weekday too short", source, length);
    instant->week = parse_2_digits(source + 2, length - 2) - 1;
    if (source[4] != '-') tk_error("bad week separator", source, length);
    if (!isdigit(source[5])) tk_error("weekday not a number", source, length);
    instant->weekday = source[5] - '0' - 1;
    instant->flags &= ~TK_INSTANT_YEAR;
    instant->flags |= TK_INSTANT_WEEK_YEAR | TK_INSTANT_WEEK | TK_INSTANT_WEEKDAY | TK_INSTANT_DAY_NUMBER;
    length -= 6;
    int soywd = (instant->day_number + 5) % 7;
    if (soywd < 4) {
      instant->day_of_year = -soywd;
    } else {
      instant->day_of_year = 7 - soywd;
    }
    int w53 = (soywd == 4) || ((soywd == 3) && leap);
    if (instant->week >= 52 + w53)
      tk_error("week number too large", NULL, instant->week);
    if (instant->weekday >= 7)
      tk_error("weekday too large", NULL, instant->weekday);
    instant->day_of_year += 7 * instant->week + instant->weekday;
    if (instant->day_of_year < 0) {
      int last_leap;
      if (year_in_century != 1)
        last_leap = (year_in_century & 3) == 1;
      else
        last_leap = !(century & 3);
      instant->day_of_year += 365 + last_leap;
      instant->year--;
    } else if (instant->day_of_year > 365 + leap) {
      instant->day_of_year -= 365 + leap;
      instant->year++;
    }
    instant->day_number += instant->day_of_year;
  } else {
    instant->day_of_year = parse_3_digits(source + 1, length - 1) - 1;
    if (instant->day_of_year > leap + 365)
      tk_error("day of year too large", NULL, instant->day_of_year);
    instant->day_number += instant->day_of_year;
    instant->flags |= TK_INSTANT_DAY_OF_YEAR | TK_INSTANT_DAY_NUMBER;
    length -= 4;
  }
  /* 0.49->0.15 (-O3) */
  /* 0.66->0.21 (-O3)
  int m = 12 * instant->year + instant->month - 3;
  div_t ym = div(m, 12);
  int dy = (153*ym.rem + 2) / 5 + instant->day - 1;
  instant->day_number = 365 * instant->year + instant->year / 4 - instant->year / 100 + instant->year / 400 + dy;
  */
  return orig_length - length;
}

int parse_iso8601_time(
  const char *source, int length,
  struct tk_instant *instant) {
  instant->hour = parse_2_digits(source, length);
  if (instant->hour > 23)
    tk_error("hour too large", NULL, instant->hour);
  if (length == 2) return 0;
  if (source[2] != ':')
    tk_error("bad time separator", source, length);
  instant->minute = parse_2_digits(source + 3, length - 3);
  if (length == 5) return 0;
  if (source[5] != ':')
    tk_error("bad time separator", source, length);
  instant->second = parse_2_digits(source + 6, length - 6);
  if (instant->second > (instant->hour == 23 && instant->minute == 59) + 59)
    tk_error("second too large", NULL, instant->second);
  /* +0.01 */
  instant->day_seconds = 60 * (60 * instant->hour + instant->minute) + instant->second;
  instant->flags |= TK_INSTANT_HOUR | TK_INSTANT_MINUTE | TK_INSTANT_SECOND | TK_INSTANT_DAY_SECONDS;
  source += 8;
  length -= 8;
  if (length > 0 && (source[0] == '.' || source[0] == ',')) {
    source++;
    length--;
    int multiplier = 1000000000;
    int sum = 0;
    while (length > 0 && isdigit(source[0])) {
      if (multiplier > 1) {
        multiplier /= 10;
        sum *= 10;
        sum += source[0] - '0';
      }
      source++;
      length--;
    }
    instant->nanos = multiplier * sum;
    instant->flags |= TK_INSTANT_NANOS;
  }
  if (length == 0) return 0;
  if (source[0] == 'Z') {
    instant->tz_minute = 0;
    instant->flags |= TK_INSTANT_TZ_MINUTE;
  } else if (source[0] == '+' || source[0] == '-') {
    int minus = source[0] == '-';
    int tz_hour = parse_2_digits(source + 1, length - 1);
    int tz_minute = 0;
    if (length > 3) {
      if (source[3] == ':')
        tz_minute = parse_2_digits(source + 4, length - 4);
      else if (isdigit(source[3]))
        tz_minute = parse_2_digits(source + 3, length - 3);
    }
    instant->tz_minute = 60 * tz_hour + tz_minute;
    if (minus)
      instant->tz_minute = -instant->tz_minute;
    instant->flags |= TK_INSTANT_TZ_MINUTE;
  }
  return 0;
}

int parse_iso8601_instant(
  const char *source, int length,
  struct tk_instant *instant) {
  /* minimal: yyyy-mm-dd */
  /* maximal: +yyyyy-mm-ddThh:mm:ss.nnnnnnnnn+hhmm */
  instant->flags = 0;
  if (length < 10) tk_error("too short date string", source, length);
  int count = parse_iso8601_date(source, length, instant);
  if (count == length) return 0;
  if (source[count] != 'T') tk_error("bad date/time separator", source, length);
  parse_iso8601_time(source + count + 1, length - count - 1, instant);
  return 0;
}

int parse_iso8601_instant_asciiz(
  const char *source,
  struct tk_instant *instant) {
  return parse_iso8601_instant(source, strlen(source), instant);
}
