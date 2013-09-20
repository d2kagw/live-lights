public class ImageMode extends RenderMode {
  PImage img;

  boolean draw(PApplet applet, int x, int y, int width, int height) {
    image(img, 0, 0);

    // no errors to report
    return true;
  }

  // set the framerate to something relevant
  void wake_up() {
    println("Color Wake Up");
    img = loadImage("image.jpg");

    frameRate(12);
  }

  // No need for sleep here
  void sleep() {
    println("Color Sleep");
  }
}