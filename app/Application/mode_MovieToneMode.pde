class MovieToneMode extends RenderMode {
  Movie movie;

  MovieToneMode (PApplet tApplet) {
    super(tApplet);
  }

  void movieEvent(Movie m) {
    m.read();
  }

  boolean draw(int x, int y, int width, int height) {
    image(movie, x, y, width, height);
    return true;
  }

  int tvColorMode() {
    return TV_COLOR_GLOBAL;
  }

  boolean shouldBufferColour() {
    return true;
  }

  boolean shouldManageCropping() {
    return true;
  }

  boolean shouldManageContrast() {
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