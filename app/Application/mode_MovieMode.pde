class MovieMode extends RenderMode {
  Movie movie;

  MovieMode (PApplet tApplet) {
    super(tApplet);
  }

  void movieEvent(Movie m) {
    m.read();
  }

  boolean draw(int x, int y, int width, int height) {
    image(movie, x, y, width, height);
    return true;
  }

  boolean shouldBufferColour() {
    return true;
  }

  boolean shouldManageCropping() {
    return true;
  }

  // Start the camera
  void wake_up() {
    println("Movie Wake Up");

    frameRate(30);

    // Get the camera list
    movie = new Movie(applet, "sample.avi");
    movie.loop();
  }

  // Stop the video stream
  void sleep() {
    println("Movie Sleep");
    if (movie != null) movie.stop();
  }
}