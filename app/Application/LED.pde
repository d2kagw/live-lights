class LED {
  int x, y, width, height, coverage;
  LED(PApplet applet, int tX, int tY, int tWidth, int tHeight, int tCoverage) {
    x        = tX;
    y        = tY;
    width    = tWidth;
    height   = tHeight;
    coverage = tCoverage;

    println("Adding LED at: " + x + "x" + y);
  }

  int[] rgbValue() {
    // new variable
    int[] rgb = new int[3];

    // get the data
    int total_pixels   = width * height;
    int pixel_coverage = floor(100 / coverage);
    
    int average_r = 0;
    int average_g = 0;
    int average_b = 0;
    
    int pixel_index;
    for(int index=0; index < total_pixels; index += pixel_coverage) {
      pixel_index = x + (floor(index/width) * DISPLAY_WIDTH) + (y * DISPLAY_WIDTH);
      
      average_r += int(red(pixels[pixel_index]));
      average_g += int(green(pixels[pixel_index]));
      average_b += int(blue(pixels[pixel_index]));
    }

    rgb[0] = average_r / (total_pixels / pixel_coverage);
    rgb[1] = average_g / (total_pixels / pixel_coverage);
    rgb[2] = average_b / (total_pixels / pixel_coverage);

    represent(rgb[0], rgb[1], rgb[2]);
    return rgb;
  }

  void represent(int r, int g, int b) {
    stroke(0);
    fill(r, g, b);
    rect(x, y, width, height);
    rect(x + ( width / 2 ), y + ( height / 2 ), 1, 1);
  }
}