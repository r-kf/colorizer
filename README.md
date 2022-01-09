# colorizer

<p align="center">
  Python app that uses deep learning to automatically colorize black and white images.</p>

<div class="img-with-text">
    <p align="center">
      <img src="https://github.com/r-kf/colorizer/blob/main/resources/app_screenshot.png"
        alt="Colorizer App Window"
        style="float: left; margin-right: 10px;" />
    </p>
    <p align="center">
      Based on the Colorful Image Colorization Algorithm by Richard Zhang (http://richzhang.github.io/colorization/)</p>
</div>

## Example

<p align="center">
  <img src="https://github.com/r-kf/colorizer/blob/main/resources/app_screenshot_with_example.png"
     alt="Colorizer App Window w/ Example"
     style="float: left; margin-right: 10px;" />
</p>

## Run

Download models
```bash
sh get_models.sh
```

Run app
```bash
python3 app.py
```


## Unsolved mysteries

For some yet unexplained reason the app will display more blue-toned version of the images compared to the colorizer-function itself. That's confusing considering the app uses that very same colorizer function and does not manipulate the image further.



| app.py             |  colorizer.py |
:-------------------------:|:-------------------------:
<img src="https://github.com/r-kf/colorizer/blob/main/resources/app_screenshot_rapeseed.png" alt="app" width="450"/>  |  <img src="https://github.com/r-kf/colorizer/blob/main/examples/rapeseed_BW_colorized.jpg" alt="app" width="400"/>
<img src="https://github.com/r-kf/colorizer/blob/main/resources/app_screenshot_pomegranate.png" alt="app" width="450"/>  |  <img src="https://github.com/r-kf/colorizer/blob/main/examples/pomegranate_colorized.jpg" alt="app" width="400"/>


  ### Attempted solutions
   - Skip image resizing before colorization
     - The only additional image manipulation the app does is to resize the images to fit the input and output windows. However we can conclude that this is not the culprit after attempting to run the app without resizing the image
   - coming soon
