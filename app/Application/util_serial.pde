static final int SERIAL_HEADERS_COUNT = 6;

byte[] tvData( int[][] led_data ) {
  int pixel_colors_counter = 0;
  byte[] pixel_colors = new byte[SERIAL_HEADERS_COUNT + (led_data.length * 3)];

  pixel_colors[pixel_colors_counter++] = 'L';
  pixel_colors[pixel_colors_counter++] = 'i';
  pixel_colors[pixel_colors_counter++] = 'v';
  pixel_colors[pixel_colors_counter++] = (byte)((led_data.length - 1) >> 8);   // LED count high byte
  pixel_colors[pixel_colors_counter++] = (byte)((led_data.length - 1) & 0xff); // LED count low byte
  pixel_colors[pixel_colors_counter++] = (byte)(pixel_colors[3] ^ pixel_colors[4] ^ 0x55); // Checksum

  for(int i = 0; i < led_data.length; i ++) {
    pixel_colors[pixel_colors_counter++] = byte(led_data[i][0]);
    pixel_colors[pixel_colors_counter++] = byte(led_data[i][1]);
    pixel_colors[pixel_colors_counter++] = byte(led_data[i][2]);
  }

  return pixel_colors;
}

byte[] surroundData( int[][] led_data ) {
  int pixel_colors_counter = 0;
  byte[] pixel_colors = new byte[SERIAL_HEADERS_COUNT + (led_data.length * 4)];

  pixel_colors[pixel_colors_counter++] = 'L';
  pixel_colors[pixel_colors_counter++] = 'i';
  pixel_colors[pixel_colors_counter++] = 'v';
  pixel_colors[pixel_colors_counter++] = (byte)((led_data.length - 1) >> 8);   // LED count high byte
  pixel_colors[pixel_colors_counter++] = (byte)((led_data.length - 1) & 0xff); // LED count low byte
  pixel_colors[pixel_colors_counter++] = (byte)(pixel_colors[3] ^ pixel_colors[4] ^ 0x55); // Checksum

  for(int i = 0; i < led_data.length; i ++) {
    pixel_colors[pixel_colors_counter++] = byte(char(65+i));
    pixel_colors[pixel_colors_counter++] = byte(led_data[i][0]);
    pixel_colors[pixel_colors_counter++] = byte(led_data[i][1]);
    pixel_colors[pixel_colors_counter++] = byte(led_data[i][2]);
  }
  
  return pixel_colors;
}

String serialIndexFor(String name) throws Exception {
  for ( int i = 0; i < Serial.list().length; i ++ ) {
    String[] part = match(Serial.list()[i], name);
    if (part != null) {
      return Serial.list()[i];
    }
  }
  throw new Exception("Serial port named '" + name + "' could not be found");
}
