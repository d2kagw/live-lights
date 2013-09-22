static final float color_amplify_contrast = 2.0;
static final int color_amplify_brightness_floor = floor(COLOR_SPACE / 10);

int[] color_amplify(int[] tColor) {
  tColor[0] = int((tColor[0] * color_amplify_contrast));
  tColor[1] = int((tColor[1] * color_amplify_contrast));
  tColor[2] = int((tColor[2] * color_amplify_contrast));

  tColor[0] = max(min(tColor[0], COLOR_SPACE), color_amplify_brightness_floor);
  tColor[1] = max(min(tColor[1], COLOR_SPACE), color_amplify_brightness_floor);
  tColor[2] = max(min(tColor[2], COLOR_SPACE), color_amplify_brightness_floor);

  return tColor;
}

int[] color_average(int[][] tColors) {
  int[] rgb = new int[3];
  int total = tColors.length;

  // increment'em
  for(int i = 0; i < tColors.length; i ++) {
    rgb[0] += tColors[i][0];
    rgb[1] += tColors[i][1];
    rgb[2] += tColors[i][2];
  }

  // average
  rgb[0] = rgb[0] / total;
  rgb[1] = rgb[1] / total;
  rgb[2] = rgb[2] / total;

  return rgb;
}