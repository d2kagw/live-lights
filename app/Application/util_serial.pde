static final int SERIAL_HEADERS_COUNT = 11;

byte[] pixelData( int[][] led_data ) {
  int pixel_colors_counter = 0;
  byte[] pixel_colors = new byte[SERIAL_HEADERS_COUNT]; //+ (led_data.length * 3)];

  pixel_colors[pixel_colors_counter++] = 'L';
  pixel_colors[pixel_colors_counter++] = 'i';
  pixel_colors[pixel_colors_counter++] = 'v';
  pixel_colors[pixel_colors_counter++] = 'e';
  pixel_colors[pixel_colors_counter++] = 'L';
  pixel_colors[pixel_colors_counter++] = 'i';
  pixel_colors[pixel_colors_counter++] = byte((led_data.length - 1) >> 8);
  pixel_colors[pixel_colors_counter++] = byte((led_data.length - 1) & 0xff);
  pixel_colors[pixel_colors_counter++] = byte(LED_SURROUND_COUNT & 0xff);
  pixel_colors[pixel_colors_counter++] = byte(pixel_colors[7] ^ pixel_colors[8] ^ 0x55);

  // for(int i = 0; i < led_data.length; i ++) {
  //   pixel_colors[pixel_colors_counter++] = byte(led_data[i][0]);
  //   pixel_colors[pixel_colors_counter++] = byte(led_data[i][1]);
  //   pixel_colors[pixel_colors_counter++] = byte(led_data[i][2]);
  // }

  return pixel_colors;
}