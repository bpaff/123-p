

class Settings():
    
    # connection settings
    CLIENT_HOST = 'localhost'
    SERVER_HOST = 'localhost'
    PORT = 2020
    CLIENT_USE_AI = False
    TURN_OFF_GUI = False
    
    
    # directions
    DIRECTION_UP = 0
    DIRECTION_UP_RIGHT = 45
    DIRECTION_RIGHT = 90
    DIRECTION_DOWN_RIGHT = 135
    DIRECTION_DOWN = 180
    DIRECTION_DOWN_LEFT = 225
    DIRECTION_LEFT = 270
    DIRECTION_UP_LEFT = 315
    
    
    # message type
    MESSAGE_TYPE_TICK = 2
    MESSAGE_TYPE_INPUT = 4
    MESSAGE_TYPE_PLAYER = 6
    MESSAGE_TYPE_CYCLE_POSITION = 8
    MESSAGE_TYPE_CYCLE_ALIVE = 10
    MESSAGE_TYPE_TRAIL_ON = 12
    MESSAGE_TYPE_TRAIL_TURN = 14
    MESSAGE_TYPE_GAME_OVER = 16
    MESSAGE_TYPE_START_GAME = 18
    MESSAGE_TYPE_QUIT_GAME = 20
    MESSAGE_TYPE_RESEND_TICK = 22

    
    # game settings
    SCREEN_DIMENSIONS = (800, 600)
    BOARD_DIMENSIONS = (800, 500)
    CAPTION = 'Multiplayer Light Cycle'
    TICK = 0.1
    MAX_MESSAGES_PER_TICK = 200
    CYCLE_LOCATIONS = ([100.0, 100.0], [700.0, 100.0], [700.0, 400.0], [100.0, 400.0])
    CYCLE_DIRECTIONS = (DIRECTION_DOWN_RIGHT, DIRECTION_DOWN_LEFT, DIRECTION_UP_LEFT, DIRECTION_UP_RIGHT)
    INSTRUCTIONS = [
      'Do move window after connected',
      'Do not hit walls and other light cycles',
      'You are the blue cycle',
      'Left and right arrows to turn',
      'Up and down arrows (or a and z) to speed up and slow down',
      'Space bar to enable or disable light cycle wall',
      'If the cycle wall is off for 5 seconds, it will turn on',
      'Esc key to quit'
    ]
    CLIENT_AI_LOOK_AHEAD_TICKS = 8
    SERVER_AI_LOOK_AHEAD_TICKS = 4
    CLIENT_SECONDS_TO_WAIT = 60.0
    
    
    # matchmaker settings
    MATCHMAKER_WAIT_SECONDS = 2
    MATCHMAKER_WAIT_TICKS = MATCHMAKER_WAIT_SECONDS / TICK
    MATCHMAKER_MINIMUM_PLAYERS = 1
    MATCHMAKER_MAXIMUM_PLAYERS = 4
    
    
    # light cycle settings
    LIGHT_CYCLE_SIZE = (20.0, 30.0)
    # LIGHT_CYCLE_SIZE must be at least 5
    WINDOW_ADJUSTMENT = 3.0
    LIGHT_START_SPEED = 40.0
    LIGHT_SPEED_ADJUSTMENT = 5.0
    LIGHT_MIN_SPEED = 30.0
    LIGHT_MAX_SPEED = 60.0
    
    # create back wheels starting lower left and going clockwise with bottom middle at 0, 0
    BACK_WHEEL_POINTS = (
        # bottom left 
        (-LIGHT_CYCLE_SIZE[0] / 4.0, 0.0),
        # top left
        (-LIGHT_CYCLE_SIZE[0] / 4.0, -LIGHT_CYCLE_SIZE[1] / 4.0),
        # top right
        (LIGHT_CYCLE_SIZE[0] / 4.0, -LIGHT_CYCLE_SIZE[1] / 4.0),
        # bottom right
        (LIGHT_CYCLE_SIZE[0] / 4.0, 0)
    )
    
    # create middle starting lower left and going clockwise with bottom middle at 0, 0
    MIDDLE_POINTS = (
        # bottom left 
        (-LIGHT_CYCLE_SIZE[0] / 8.0 , 0.0),
        # top left
        (-LIGHT_CYCLE_SIZE[0] / 8.0 , -LIGHT_CYCLE_SIZE[1]),
        # top right
        (LIGHT_CYCLE_SIZE[0] / 8.0 , -LIGHT_CYCLE_SIZE[1]),
        # bottom right
        (LIGHT_CYCLE_SIZE[0] / 8.0 , 0)
    )
    MIDDLE_LINES = []
    for i in range(len(MIDDLE_POINTS) - 1):
        MIDDLE_LINES.append((MIDDLE_POINTS[i], MIDDLE_POINTS[i + 1]))
    MIDDLE_LINES.append((MIDDLE_POINTS[len(MIDDLE_POINTS) - 1], MIDDLE_POINTS[0]))
    
    # create front wheels starting lower left and going clockwise with bottom middle at 0, - LIGHT_CYCLE_SIZE[1] 3.0 / 4.0
    FRONT_WHEEL_POINTS = (
        # bottom left 
        (-LIGHT_CYCLE_SIZE[0] / 3.0 , -LIGHT_CYCLE_SIZE[1] * 3.0 / 4.0),
        # top left
        (-LIGHT_CYCLE_SIZE[0] / 3.0 , -LIGHT_CYCLE_SIZE[1]),
        # top right
        (LIGHT_CYCLE_SIZE[0] / 3.0 , -LIGHT_CYCLE_SIZE[1]),
        # bottom right
        (LIGHT_CYCLE_SIZE[0] / 3.0 , -LIGHT_CYCLE_SIZE[1] * 3.0 / 4.0)
    )
    
    # create driver window starting lower left and going clockwise with bottom middle at 0, WINDOW_ADJUSTMENT - LIGHT_CYCLE_SIZE[1] 3.0 / 4.0
    DRIVER_WINDOW_POINTS = (
        # bottom left 
        (WINDOW_ADJUSTMENT - LIGHT_CYCLE_SIZE[0] / 8.0 , WINDOW_ADJUSTMENT - LIGHT_CYCLE_SIZE[1] * 3.0 / 4.0),
        # top left
        (WINDOW_ADJUSTMENT - LIGHT_CYCLE_SIZE[0] / 8.0 , WINDOW_ADJUSTMENT - LIGHT_CYCLE_SIZE[1]),
        # top right
        (-WINDOW_ADJUSTMENT + LIGHT_CYCLE_SIZE[0] / 8.0 , WINDOW_ADJUSTMENT - LIGHT_CYCLE_SIZE[1]),
        # bottom right
        (-WINDOW_ADJUSTMENT + LIGHT_CYCLE_SIZE[0] / 8.0 , WINDOW_ADJUSTMENT - LIGHT_CYCLE_SIZE[1] * 3.0 / 4.0)
    )

    # create up arrow starting in lower left and going clockwise with bottom middle at 0, 0
    ARROW_POINTS = (
        # base left
        (-LIGHT_CYCLE_SIZE[0] / 4.0 , 0.0),
        # inside left
        (-LIGHT_CYCLE_SIZE[0] / 4.0 , -LIGHT_CYCLE_SIZE[1] * 3.0 / 4.0),
        # far left
        (-LIGHT_CYCLE_SIZE[0] / 2.0 , -LIGHT_CYCLE_SIZE[1] * 3.0 / 4.0),
        # point
        (0.0, -LIGHT_CYCLE_SIZE[1]),
        # far right
        (LIGHT_CYCLE_SIZE[0] / 2.0 , -LIGHT_CYCLE_SIZE[1] * 3.0 / 4.0),
        # inside right
        (LIGHT_CYCLE_SIZE[0] / 4.0 , -LIGHT_CYCLE_SIZE[1] * 3.0 / 4.0),
        # base right
        (LIGHT_CYCLE_SIZE[0] / 4.0 , 0.0),
    )
