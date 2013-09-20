public class SpectrumMode extends RenderMode {
  float hue    = 0.0;
  float hueMax = 100.0;

  boolean draw(PApplet applet, int x, int y, int width, int height) {
    // HSB makes spectrums easy
    colorMode(HSB, hueMax);

    // Fill and rect
    fill(hue, hueMax, hueMax);
    noStroke();
    rect(x, y, width, height);

    hue += 1;
    if (hue > hueMax) hue = 0;
    if (hue <      0) hue = hueMax;

    // no errors to report
    return true;
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