public class Cropper {

  PApplet applet;
  int x, y, width, height;

  int maxEnergy = floor(COLOR_SPACE / 5);
  int maxCrop   = 100;

  int lastBarHeight;
  static final int bufferLength = 30;
  int[] barBuffer = new int[bufferLength];

  Cropper (PApplet tApplet, int tX, int tY, int tWidth, int tHeight) {
    applet = tApplet;
    x = tX;
    y = tY;
    width  = tWidth;
    height = tHeight;
  }

  int barHeight() {
    return lastBarHeight;
  }

  void calculateBarHeight() {
    int row = 0;
    int row_brightness = 0;
    int pixel_index;
    int sample_columns = 30;
    int width_intervals = (width / (2 + sample_columns));

    colorMode(HSB, COLOR_SPACE);
    row_brightness = 0;
    while (true) {
      for (int i=0; i < sample_columns; i ++) {
        row_brightness += int(brightness(pixels[(row * DISPLAY_WIDTH) + (width_intervals * (i + 1))]));  
      }
      row_brightness = row_brightness / (sample_columns * 2);
      if (row_brightness > maxEnergy) break;
      
      row ++;
      if (row > maxCrop) break;
    }

    lastBarHeight = bufferBar(row);
  }

  int bufferBar (int height) {
    int[] tempBuffer = (int[])subset(barBuffer, 1);
           barBuffer = new int[bufferLength];

    // copy the old into the new
    for (int i=0; i < bufferLength - 1; i ++) barBuffer[i] = tempBuffer[i];

    // add the new height in at the end
    barBuffer[bufferLength-1] = height;

    // buff the height (average)
    height = 0;
    for (int i=0; i < bufferLength; i ++) height += barBuffer[i];

    return height / bufferLength;
  }
}