class RenderMode {

  // Use the average colour from the region
  static final int SURROUND_COLOR_AVERAGE = 0;

  // Use the average colour from the centre of the frame
  static final int TV_COLOR_GLOBAL = 0;

  // Use the average colour from a localised block near the location of the LED
  static final int TV_COLOR_LOCAL  = 1;

  PApplet applet;

  RenderMode (PApplet tApplet) {
    applet = tApplet;
  }

  void wake_up() {
    // Override
  }
  void sleep() {
    // Override
  }

  // Render the actual frame
  boolean draw(int x, int y, int width, int height) {
    // Override
    return true;
  }

  // LED Colouring Modes
  int surroundColorMode() {
    return SURROUND_COLOR_AVERAGE;
  }
  int tvColorMode() {
    return TV_COLOR_LOCAL;
  }

  // Frame Management
  boolean shouldManageCropping() {
    return false;
  }
  boolean shouldManageContrast() {
    return false;
  }
  boolean shouldBufferColour() {
    return false;
  }

  // Mode Support
  void optionCycleNext() {
    // override
  }
  void optionCyclePrevious() {
    // override
  }
}