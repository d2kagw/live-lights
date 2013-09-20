class RenderMode {

  static final int SURROUND_COLOR_AVERAGE   = 0;
  static final int SURROUND_COLOR_HISTOGRAM = 1;

  PApplet applet;

  RenderMode (PApplet tApplet) {
    applet = tApplet;
  }

  boolean draw(int x, int y, int width, int height) {
    // Override
    return true;
  }

  int surroundColorMode() {
    return SURROUND_COLOR_AVERAGE;
  }

  boolean shouldManageCropping() {
    return false;
  }

  boolean shouldBufferColour() {
    return false;
  }

  void optionCycleNext() {
    // override
  }

  void optionCyclePrevious() {
    // override
  }

  void wake_up() {
    // Override
  }

  void sleep() {
    // Override
  }
}