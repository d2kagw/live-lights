class Histogram {
  static final int points = 255;
  static final int display_width = Histogram.points;
  
  int width, height, x, y;

  Histogram(PApplet applet, int tX, int tY, int tHeight) {
    x = tX;
    y = tY;
    height = tHeight;
    width  = Histogram.display_width;
  }
}