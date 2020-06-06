import sdl2/sdl

const
  Title = "SDL2 App"
  ScreenW = 640 # Window width
  ScreenH = 480 # Window height
  WindowFlags = 0
  RendererFlags = sdl.RendererAccelerated or sdl.RendererPresentVsync

type
  App = ref AppObj
  AppObj = object
    window*: sdl.Window     # Window pointer
    renderer*: sdl.Renderer # Rendering state pointer


proc init(app: App): bool =
  # Init SDL
  if sdl.init(sdl.InitVideo) != 0:
    echo "ERROR: Can't initialize SDL: ", sdl.getError()
    return false

  app.window = sdl.createWindow(
      Title,
      sdl.WindowPosUndefined,
      sdl.WindowPosUndefined,
      ScreenW,
      ScreenH,
      WindowFlags)
  if app.window == nil:
    echo "ERROR: Can't create window: ", sdl.getError()
    return false

  # Create renderer
  app.renderer = sdl.createRenderer(app.window, -1, RendererFlags)
  if app.renderer == nil:
    echo "ERROR: Can't create renderer: ", sdl.getError()
    return false

  # Set draw color
  if app.renderer.setRenderDrawColor(0xFF, 0xFF, 0xFF, 0xFF) != 0:
    echo "ERROR: Can't set draw color: ", sdl.getError()
    return false

  echo "SDL initialized successfully"
  return true


proc exit(app: App) =
  app.renderer.destroyRenderer()
  app.window.destroyWindow()
  sdl.quit()
  echo "SDL shutdown completed"


var
  app = App(window: nil, renderer: nil)

if init(app):
  discard app.renderer.renderClear()
  app.renderer.renderPresent()
  sdl.delay(2000)

exit(app)
