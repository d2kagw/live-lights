static class Renderer {
  int mode = 0;
  ArrayList modes;

  private Renderer() {
    super();

    // Setup the Renderers
    modes = new ArrayList();
  }

  public static void addRenderMode(RenderMode new_mode) {
    Renderer.getInstance().modes.add( new_mode );
  }

  public static void setRenderMode(int new_mode) {
    // tell the renderer to stop processing anything it might be processing
    Renderer.getInstance().currentRenderer().sleep();

    // set the renderer
    Renderer.getInstance().mode = new_mode;

    // get it running
    Renderer.getInstance().currentRenderer().wake_up();
  }

  public static void modeCycle() {
    println("Next Render Mode...");

    int tmp = Renderer.getInstance().mode + 1;
    if (tmp > Renderer.getInstance().modes.size()-1) {
      tmp = 0;
    }

    Renderer.getInstance().setRenderMode(tmp);
  }  

  public static RenderMode currentRenderer() {
    return (RenderMode)Renderer.getInstance().modes.get(Renderer.getInstance().mode);
  }  

  public static void draw(int x, int y, int width, int height) {
    ((RenderMode)Renderer.getInstance().modes.get(Renderer.getInstance().mode)).draw(x, y, width, height);
  }
  
  // SINGLETON BELOW

  private static class SingletonHolder { 
     private static final Renderer INSTANCE = new Renderer();
  }
  
  public static Renderer getInstance() {
    return SingletonHolder.INSTANCE;
  }
}