public class ColorMode extends RenderMode {
  int hue = 0;
  int hueMax = 100;

  boolean draw(PApplet applet, int x, int y, int width, int height) {
    // HSB makes spectrums easy
    colorMode(HSB, hueMax);

    // Fill and rect
    fill(hue, hueMax, hueMax);
    noStroke();
    rect(x, y, width, height);

    // no errors to report
    return true;
  }

  // colour shift
  void optionCycleNext() {
    hue += 1;
    if (hue > hueMax) hue = 0;
  }

  // colour unshift
  void optionCyclePrevious() {
    hue -= 1;
    if (hue < 0) hue = hueMax;
  }

  // set the framerate to something relevant
  void wake_up() {
    println("Color Wake Up");
    frameRate(12);
  }

  // No need for sleep here
  void sleep() {
    println("Color Sleep");
  }
}