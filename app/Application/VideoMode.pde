import processing.video.*;

public class VideoMode extends RenderMode {
  Capture video;

  VideoMode (PApplet tApplet) {
    super(tApplet);
  }

  boolean draw(int x, int y, int width, int height) {
    if (video.available()) video.read();
    video.loadPixels();
    
    // lets render actual picture in the background for testing
    image(video, x, y, width, height);

    // no errors to report
    return true;
  }

  // Start the camera
  void wake_up() {
    println("Video Wake Up");

    // Get the camera list
    String[] cameras = Capture.list();
    
    if (cameras.length == 0) {
      println("There are no cameras available for capture.");
      exit();
    } else {
      println("Available cameras:");
      for (int i = 0; i < cameras.length; i++) {
        println(cameras[i]);
      }
      video = new Capture(applet, VIDEO_WIDTH, VIDEO_HEIGHT, 30);
    }

    frameRate(30);
    video.start();
  }

  // Stop the video stream
  void sleep() {
    println("Video Sleep");
    video.stop();
  }
}