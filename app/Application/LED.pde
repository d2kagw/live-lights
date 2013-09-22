class LED {
  int x, y, width, height, coverage;

  boolean should_buffer = false;
  boolean should_manage_contrast = false;
  static final int color_buffer_length = 15;
  int[][] color_buffer = new int[color_buffer_length][3];

  LED(PApplet applet, int tX, int tY, int tWidth, int tHeight, int tCoverage) {
    x        = tX;
    y        = tY;
    width    = tWidth;
    height   = tHeight;
    coverage = tCoverage;

    // fill the color buffer with black
    for (int i=0; i < color_buffer_length; i ++) {
      color_buffer[i][0] = 0;
      color_buffer[i][1] = 0;
      color_buffer[i][2] = 0;
    }

    println("Adding LED at: " + x + "x" + y);
  }

  void buffer(boolean newState) {
    should_buffer = newState;
  }

  void manage_contrast(boolean newState) {
    should_manage_contrast = newState;
  }

  int[] rgbValue() {
    colorMode(RGB, 100);

    // new variable
    int[] rgb = new int[3];

    // calculate the coverage
    int total_pixels   = width * height;
    int pixel_coverage = floor(100 / coverage);
    
    int average_r = 0;
    int average_g = 0;
    int average_b = 0;
    
    // sum up all the pixel values
    int pixel_index;
    for(int index=0; index < total_pixels; index += pixel_coverage) {
      pixel_index = x + (floor(index/width) * DISPLAY_WIDTH) + (y * DISPLAY_WIDTH);
      
      average_r += int(red(pixels[pixel_index]));
      average_g += int(green(pixels[pixel_index]));
      average_b += int(blue(pixels[pixel_index]));
    }

    // calc the value for each channel
    rgb[0] = average_r / (total_pixels / pixel_coverage);
    rgb[1] = average_g / (total_pixels / pixel_coverage);
    rgb[2] = average_b / (total_pixels / pixel_coverage);

    // Amplify the colour
    if (should_manage_contrast) rgb = color_amplify(rgb);

    // Buff the color... if we're buffering colours?
    if (should_buffer) rgb = bufferColor(rgb[0], rgb[1], rgb[2]);
    
    // represent & return
    represent(rgb[0], rgb[1], rgb[2]);
    return rgb;
  }

  void represent(int r, int g, int b) {
    int width_4  = width  / 4;
    int height_4 = height / 4;

    noStroke();
    fill(r, g, b);
    
    rect(x + width_4, y + height_4, width_4 * 2, height_4 * 2);
  }

  int[] bufferColor (int r, int g, int b) {
    int [][] tempBuffer = (int[][])subset(color_buffer, 1);
    color_buffer = new int[color_buffer_length][3];

    // copy the old into the new
    for (int i=0; i < color_buffer_length - 1; i ++) {
      color_buffer[i][0] = tempBuffer[i][0];
      color_buffer[i][1] = tempBuffer[i][1];
      color_buffer[i][2] = tempBuffer[i][2];
    }

    // add the new colour in at the end
    color_buffer[color_buffer_length-1][0] = r;
    color_buffer[color_buffer_length-1][1] = g;
    color_buffer[color_buffer_length-1][2] = b;

    // buff the channels (average)
    r = 0;
    g = 0;
    b = 0;
    for (int i=0; i < color_buffer_length; i ++) {
      r += color_buffer[i][0];
      g += color_buffer[i][1];
      b += color_buffer[i][2];
    }

    int[] rgb = new int[3];
    rgb[0] = r / color_buffer_length;
    rgb[1] = g / color_buffer_length;
    rgb[2] = b / color_buffer_length;

    return rgb;
  }
}