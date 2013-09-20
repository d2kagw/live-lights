public class Cropper {

  PApplet applet;
  int x, y, width, height;

  int maxEnergy = 15;
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
    int width_intervals = (width / 5);

    colorMode(HSB, 100);

    while (true) {
      row_brightness  = int(brightness(pixels[(row * DISPLAY_WIDTH) + (width_intervals * 1)]));
      row_brightness += int(brightness(pixels[(row * DISPLAY_WIDTH) + (width_intervals * 2)]));
      row_brightness += int(brightness(pixels[(row * DISPLAY_WIDTH) + (width_intervals * 3)]));
      row_brightness  = row_brightness / 3;

      
      if (row_brightness > maxEnergy) {
        break;
      }
      
      row ++;
      if (row > maxCrop) {
        println("Giving up at row " + row + " because we're still below our max level");
        break;
      }
    }

    lastBarHeight = bufferBar(row);
  }

  int bufferBar (int height) {
    int[] tempBuffer = (int[])subset(barBuffer, 1);
    barBuffer = new int[bufferLength];

    // copy the old into the new
    for (int i=0; i < bufferLength - 1; i ++) {
      barBuffer[i] = tempBuffer[i];
    }

    // add the new height in at the end
    barBuffer[bufferLength-1] = height;

    // buff the height (average)
    height = 0;
    for (int i=0; i < bufferLength; i ++) {
      height += barBuffer[i];
    }

    return height / bufferLength;
  }
}