#include "cheat.h"
#include "cheats.h"
#include "date.h"

CHEAT_TEST(
  parser_test,
  struct tk_instant instant;
  parse_iso8601_instant_asciiz("2021-10-17T18:35:01", &instant);
  cheat_assert(1);
  cheat_assert_int(instant.year, 2021);
  cheat_assert_int(instant.month, 10 - 1);
  cheat_assert_int(instant.day, 17 - 1);
  cheat_assert_int(instant.hour, 18);
  cheat_assert_int(instant.minute, 35);
  cheat_assert_int(instant.second, 1);

  parse_iso8601_instant_asciiz("2021-290T18:35:01", &instant);
  cheat_assert_int(instant.year, 2021);
  cheat_assert_int(instant.day_of_year, 290 - 1);
  cheat_assert_int(instant.hour, 18);
  cheat_assert_int(instant.minute, 35);
  cheat_assert_int(instant.second, 1);

  parse_iso8601_instant_asciiz("2021-W41-7T18:35:01", &instant);
  cheat_assert_int(instant.year, 2021);
  cheat_assert_int(instant.week, 41 - 1);
  cheat_assert_int(instant.weekday, 7 - 1);
  cheat_assert_int(instant.hour, 18);
  cheat_assert_int(instant.minute, 35);
  cheat_assert_int(instant.second, 1);
  
)
