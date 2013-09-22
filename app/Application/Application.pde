////
// Import Modules
import processing.serial.*;
import processing.video.*;

Serial serialConnection;

void movieEvent(Movie m) {
  m.read();
}


////
// Setup Constants

// TV/Video Processing Constants
static final float VIDEO_RATIO  = 16.0 / 9.0;
static final int   VIDEO_WIDTH  = 1920 / 4;
static final int   VIDEO_HEIGHT = ceil( VIDEO_WIDTH / VIDEO_RATIO );

// LED Constants
static final int LED_TV_COLUMNS     = 18;
static final int LED_TV_ROWS        = 10;
static final int LED_TV_TOTAL       = ( ( LED_TV_COLUMNS + LED_TV_ROWS ) * 2 ) - 4;

static final int LED_TV_LED_WIDTH    = ceil( VIDEO_WIDTH / ( LED_TV_COLUMNS * 1.0 ) );
static final int LED_TV_LED_HEIGHT   = ceil( ceil( VIDEO_WIDTH / VIDEO_RATIO ) / LED_TV_ROWS );
static final int LED_TV_LED_COVERAGE = 100; // PERCENT

static final int LED_SURROUND_MAX      = 4;
static final int LED_SURROUND_COUNT    = 4; // 0 = no surround lights
static final int LED_SURROUND_COVERAGE = 100; // PERCENT

// Logging
static final boolean VERBOSE_LOGGING     = true;
static final boolean ENABLE_SERIAL_COMMS = false;

// Display Constants
static final int DISPLAY_WIDTH  = VIDEO_WIDTH + Histogram.display_width;
static final int DISPLAY_HEIGHT = VIDEO_HEIGHT;

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
  // Create Display...
  println(" - Creating display: " + DISPLAY_WIDTH + "x" + DISPLAY_HEIGHT);
  size(DISPLAY_WIDTH, DISPLAY_HEIGHT);
  noSmooth();

  // ------------------------
  // Setup Video Processing & UX...
  Histogram.display_height = floor( DISPLAY_HEIGHT / 3.0 );
  cropper = new Cropper(this, 0, 0, VIDEO_WIDTH, VIDEO_HEIGHT);

  // ------------------------
  // Create the TV LEDs
  for (int i = 0; i < LED_TV_TOTAL; i++) {
    int[] temp = columnAndRowForLED(i);
    int x = temp[0] * LED_TV_LED_WIDTH;
    int y = temp[1] * LED_TV_LED_HEIGHT;
    tvLEDArray.add( new LED(this, x, y, LED_TV_LED_WIDTH, LED_TV_LED_HEIGHT, LED_TV_LED_COVERAGE) );
  }

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
  Renderer.addRenderMode( new MovieMode(this)    );
  Renderer.addRenderMode( new ImageMode(this)    );
  Renderer.addRenderMode( new ColorMode(this)    );
  Renderer.addRenderMode( new SpectrumMode(this) );
  Renderer.addRenderMode( new DiscoMode(this)    );
  Renderer.addRenderMode( new VideoMode(this)    );
  Renderer.setRenderMode(0);

  // ------------------------
  // Enable Serial Comms...
  if (ENABLE_SERIAL_COMMS) {
    println("Here are our serial ports:");
    println(Serial.list());
    serialConnection = new Serial(this, Serial.list()[6], 115200);
  }

  println("Setup Complete.");
}

////
// Draw
void draw() {
  // clear the screen
  colorMode(RGB, 100);
  background(255,255,255);

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

  // Process TV LEDs
  for (int i = 0; i < LED_TV_TOTAL; i++) {
    int[] rgb = ((LED)tvLEDArray.get(i)).rgbValue();
  }

  // Process Surround LEDs
  for (int i = 0; i < LED_SURROUND_COUNT; i++) {
    int[] rgb = ((LED)surroundLEDArray.get(i)).rgbValue();
  }

}

////
// Change Render Mode
void modeChanged() {
  boolean shouldBuf = Renderer.currentRenderer().shouldBufferColour();

  // update render modes on the LEDs
  for (int i = 0; i < LED_TV_TOTAL; i++) {
    ((LED)tvLEDArray.get(i)).buffer(shouldBuf);
  }
  for (int i = 0; i < LED_SURROUND_COUNT; i++) {
    ((LED)surroundLEDArray.get(i)).buffer(shouldBuf);
  }
}