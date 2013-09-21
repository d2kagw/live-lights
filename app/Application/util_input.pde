void keyPressed(){
  switch(key) {
    case('w'):
      println("Brightness Up");
      // if (modifier_brightness < 100) modifier_brightness += 10;
      break;
    case('s'):
      println("Brightness Down");
      // if (modifier_brightness > 10) modifier_brightness -= 10;
      break;
      

    case('d'):
      println("Render Option Next");
      Renderer.currentRenderer().optionCycleNext();
      break;
    case('a'):
      println("Renderer Option Previous");
      Renderer.currentRenderer().optionCyclePrevious();
      break;
    

    case(' '):
      println("Renderer Cycle");
      Renderer.modeCycle();
      modeChanged();
      break;
      
    default:
      println("Not sure what '" + key + "' is meant to do?");
  }
}