class DiscoMode extends RenderMode {
  int framesUntilNextModeChange = 0;
  int hueMax = 100;

  int currentMode = 0;
  static final int modeCount = 2;

  DiscoMode (PApplet tApplet) {
    super(tApplet);
  }

  boolean draw(int x, int y, int width, int height) {
    // HSB makes spectrums easy
    colorMode(HSB, hueMax);

    noStroke();
    switch(currentMode){
      case 0:
        drawHueFade(x, y, width, height);
        break;
      case 1:
        drawStrobe(x, y, width, height);
        break;
       default:
         println("No idea what " + currentMode + " mode is");
    };

    framesUntilNextModeChange -= 1;
    if (framesUntilNextModeChange < 0) {
      changeMode();
    }

    // no errors to report
    return true;
  }

  // MODES
  int hue_fade_progress = 0;
  void drawHueFade(int x, int y, int width, int height) {
    hue_fade_progress -= 10;
    if (hue_fade_progress > hueMax) hue_fade_progress = 0;
    if (hue_fade_progress <      0) hue_fade_progress = hueMax;
    
    // draw four blocks
    fill(hue_fade_progress, hueMax, hueMax);
    rect(x, y, width, height);
  }

  boolean strobe_progress = false;
  void drawStrobe(int x, int y, int width, int height) {
    // strobe state
    if (strobe_progress) {
      fill(floor(random(0, hueMax)), hueMax, hueMax);
    } else {
      fill(0, hueMax, 0);
    }
    rect(x, y, width, height);
    strobe_progress = !strobe_progress;
  }

  // Logic
  void changeMode() {
    framesUntilNextModeChange = floor(random(frameRate/2, frameRate*4));
    currentMode = floor(random(0, modeCount));
  }

  // colour shift
  void optionCycleNext() {
    changeMode();
  }

  // colour unshift
  void optionCyclePrevious() {
    changeMode();
  }

  // set the framerate to something relevant
  void wake_up() {
    println("Disco Wake Up");
    frameRate(12);
  }

  // No need for sleep here
  void sleep() {
    println("Disco Sleep");
  }
}