////
// Import Modules
import processing.serial.*;
import processing.video.*;

Serial serialTVArduino;
Serial serialSurroundXbee;

void movieEvent(Movie m) {
  m.read();
}


////
// Setup Constants
static final boolean ENABLE_SERIAL_COMMS = false;

// TV/Video Processing Constants
static final float VIDEO_RATIO  = 16.0 / 9.0;
static final int   VIDEO_WIDTH  = 1920 / 6;
static final int   VIDEO_HEIGHT = ceil( VIDEO_WIDTH / VIDEO_RATIO );

// LED Constants
static final int LED_TV_COLUMNS     = 18;
static final int LED_TV_ROWS        = 10;
static final int LED_TV_TOTAL       = ( ( LED_TV_COLUMNS + LED_TV_ROWS ) * 2 ) - 4;

static final int LED_TV_LED_WIDTH    = ceil( VIDEO_WIDTH / ( LED_TV_COLUMNS * 1.0 ) );
static final int LED_TV_LED_HEIGHT   = ceil( ceil( VIDEO_WIDTH / VIDEO_RATIO ) / LED_TV_ROWS );
static final int LED_TV_LED_COVERAGE = 100; // PERCENT

static final int LED_SURROUND_MAX      = 4; // Don't change this
static final int LED_SURROUND_COUNT    = 2; // 0 = no surround lights, currently 4 max...
static final int LED_SURROUND_COVERAGE = 25; // PERCENT

// Display Constants
static final int DISPLAY_WIDTH  = VIDEO_WIDTH;
static final int DISPLAY_HEIGHT = VIDEO_HEIGHT;
static final int COLOR_SPACE    = 255;

// LEDs
ArrayList tvLEDArray = new ArrayList();
ArrayList surroundLEDArray = new ArrayList();
Cropper cropper;

////
// Setup
void setup() {
  println("Starting Setup...");

  // ------------------------
  // Bit of error checking
  if (LED_SURROUND_COUNT > LED_SURROUND_MAX) {
    println("You can't have more than " + LED_SURROUND_COUNT + " surround LEDs");
    exit(); 
  }

  // ------------------------
  // Enable Serial Comms...
  if (ENABLE_SERIAL_COMMS) {
    try {
      println("Connecting to TV Arduino via USB Serial...");
      String serialPort = serialIndexFor("tty.usbmodem");
      serialTVArduino = new Serial(this, serialPort, 115200);
    } catch (Exception e) {
      println(e);
      exit();
    }

    try {
      println("Connecting to Xbee via FTDI USB cable...");
      String serialPort = serialIndexFor("tty.usbserial");
      serialSurroundXbee = new Serial(this, serialPort, 9600);
    } catch (Exception e) {
      println(e);
      exit();
    }
  }

  // ------------------------
  // Create Display...
  println("Creating display: " + DISPLAY_WIDTH + "x" + DISPLAY_HEIGHT);
  size(DISPLAY_WIDTH, DISPLAY_HEIGHT);
  noSmooth();

  // ------------------------
  // Setup Video Processing & UX...
  cropper = new Cropper(this, 0, 0, VIDEO_WIDTH, VIDEO_HEIGHT);

  // ------------------------
  // Create the TV LEDs
  for (int i = 0; i < LED_TV_TOTAL; i++) {
    int[] temp = columnAndRowForLED(i);
    int x = temp[0] * LED_TV_LED_WIDTH;
    int y = temp[1] * LED_TV_LED_HEIGHT;
    tvLEDArray.add( new LED(this, x, y, LED_TV_LED_WIDTH, LED_TV_LED_HEIGHT, LED_TV_LED_COVERAGE) );
  }

  // ------------------------
  // Create the Surround LEDs
  int surround_width  = VIDEO_WIDTH  - (LED_TV_LED_WIDTH  * 2);
  int surround_height = VIDEO_HEIGHT - (LED_TV_LED_HEIGHT * 2);
  switch (LED_SURROUND_COUNT) {
    case 1:
      surroundLEDArray.add( new LED(this, LED_TV_LED_WIDTH, LED_TV_LED_HEIGHT, surround_width, surround_height, LED_SURROUND_COVERAGE) );
      break;

    case 2:
      surround_width = surround_width / 2;
      surroundLEDArray.add( new LED(this, LED_TV_LED_WIDTH                 , LED_TV_LED_HEIGHT, surround_width, surround_height, LED_SURROUND_COVERAGE) );
      surroundLEDArray.add( new LED(this, LED_TV_LED_WIDTH + surround_width, LED_TV_LED_HEIGHT, surround_width, surround_height, LED_SURROUND_COVERAGE) );
      break;

    case 3:
      surround_width = surround_width / 3;
      surroundLEDArray.add( new LED(this, LED_TV_LED_WIDTH                       , LED_TV_LED_HEIGHT, surround_width, surround_height, LED_SURROUND_COVERAGE) );
      surroundLEDArray.add( new LED(this, LED_TV_LED_WIDTH +  surround_width     , LED_TV_LED_HEIGHT, surround_width, surround_height, LED_SURROUND_COVERAGE) );
      surroundLEDArray.add( new LED(this, LED_TV_LED_WIDTH + (surround_width * 2), LED_TV_LED_HEIGHT, surround_width, surround_height, LED_SURROUND_COVERAGE) );
      break;

    case 4:
      surround_width  = surround_width  / 2;
      surround_height = surround_height / 2;
      surroundLEDArray.add( new LED(this, LED_TV_LED_WIDTH                 , LED_TV_LED_HEIGHT + surround_height, surround_width, surround_height, LED_SURROUND_COVERAGE) );
      surroundLEDArray.add( new LED(this, LED_TV_LED_WIDTH + surround_width, LED_TV_LED_HEIGHT + surround_height, surround_width, surround_height, LED_SURROUND_COVERAGE) );
      surroundLEDArray.add( new LED(this, LED_TV_LED_WIDTH + surround_width, LED_TV_LED_HEIGHT                  , surround_width, surround_height, LED_SURROUND_COVERAGE) );
      surroundLEDArray.add( new LED(this, LED_TV_LED_WIDTH                 , LED_TV_LED_HEIGHT                  , surround_width, surround_height, LED_SURROUND_COVERAGE) );
      break;
  }

  // ------------------------
  // Create Renderers...
  // Add them in order
  Renderer.addRenderMode( new MovieMode(this)     );
  Renderer.addRenderMode( new MovieToneMode(this) );
  Renderer.addRenderMode( new ImageMode(this)     );
  Renderer.addRenderMode( new ColorMode(this)     );
  Renderer.addRenderMode( new SpectrumMode(this)  );
  Renderer.addRenderMode( new DiscoMode(this)     );
  Renderer.addRenderMode( new VideoMode(this)     );
  Renderer.setRenderMode(0);
  
  modeChanged();
  println("Setup Complete.");
}

////
// Draw
void draw() {
  // clear the screen
  colorMode(RGB, COLOR_SPACE);
  background(COLOR_SPACE);

  // Renderer... DRAW!
  int render_x = 0;
  int render_y = 0;
  int render_width  = VIDEO_WIDTH;
  int render_height = VIDEO_HEIGHT;
  
  // yeah, draw
  Renderer.draw(render_x, render_y, render_width, render_height);
  loadPixels();

  // But wait, if we're managing cropping, we'll need to crop based on the picture
  if (Renderer.currentRenderer().shouldManageCropping()) {
    cropper.calculateBarHeight();

    // don't waste cycles if we're not cropping
    if ( cropper.barHeight() > 0 ) {
      render_y = 0 - cropper.barHeight();
      render_height = VIDEO_HEIGHT + ( cropper.barHeight() * 2 );

      Renderer.draw(render_x, render_y, render_width, render_height);
      loadPixels();
    }
  }

  // SURROUND LEDS ----------------------
  int[][] surroundRGB = new int[LED_SURROUND_COUNT][3];
  if (Renderer.currentRenderer().surroundColorMode() == RenderMode.SURROUND_COLOR_AVERAGE) {
    // get the LED colours
    for (int i = 0; i < LED_SURROUND_COUNT; i++) {
      surroundRGB[i] = ((LED)surroundLEDArray.get(i)).rgbValue();
    }
  } else {
    println("No idea how to handle this surround mode: " + Renderer.currentRenderer().surroundColorMode());
    exit();
  }
  
  println(surroundData(surroundRGB));
  if (ENABLE_SERIAL_COMMS) {
    serialSurroundXbee.write(surroundData(surroundRGB));
  }

  // TV LEDS ----------------------
  int[][] tvRGB = new int[LED_TV_TOTAL][3];
  if (Renderer.currentRenderer().tvColorMode() == RenderMode.TV_COLOR_GLOBAL) {
    for (int i = 0; i < LED_TV_TOTAL; i++) {
      tvRGB[i] = color_average(surroundRGB);
      ((LED)tvLEDArray.get(i)).represent( tvRGB[i][0], tvRGB[i][1], tvRGB[i][2] );
    }
  } else if (Renderer.currentRenderer().tvColorMode() == RenderMode.TV_COLOR_LOCAL) {
    for (int i = 0; i < LED_TV_TOTAL; i++) {
      tvRGB[i] = ((LED)tvLEDArray.get(i)).rgbValue();
    }
  } else {
    println("No idea how to handle this tv mode: " + Renderer.currentRenderer().tvColorMode());
    exit();
  }

  if (ENABLE_SERIAL_COMMS) {
    serialTVArduino.write(tvData(tvRGB));
  }

}

////
// Change Render Mode
void modeChanged() {
  boolean shouldBuf = Renderer.currentRenderer().shouldBufferColour();
  boolean shouldCon = Renderer.currentRenderer().shouldManageContrast();

  // update render modes on the LEDs
  for (int i = 0; i < LED_TV_TOTAL; i++) {
    ((LED)tvLEDArray.get(i)).buffer(shouldBuf);
    ((LED)tvLEDArray.get(i)).manage_contrast(shouldCon);
  }
  for (int i = 0; i < LED_SURROUND_COUNT; i++) {
    ((LED)surroundLEDArray.get(i)).buffer(shouldBuf);
    ((LED)surroundLEDArray.get(i)).manage_contrast(shouldCon);
  }
}
