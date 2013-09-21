int[] columnAndRowForLED(int led_index) {
  int col_max = LED_TV_COLUMNS - 1;
  int row_max = LED_TV_ROWS    - 1;
  int tCol, tRow, tLed_index;
  
  if (led_index < LED_TV_TOTAL/2) {
    tCol = min(col_max, led_index);
    tRow = led_index - col_max;
    if (led_index < col_max) {
      tRow = 0;
    }
  } else {
    tLed_index = LED_TV_TOTAL - led_index;
    tCol = tLed_index - row_max;
    tRow = min(row_max, tLed_index);
    if (tCol < 0) {
      tCol = 0;
    }
  }
  int[] response = {tCol, tRow};
  return response;
}