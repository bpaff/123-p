
class Settings():
    
    SCREEN_DIMENSIONS = (800, 600)
    BOARD_DIMENSIONS = (800, 500)
    CAPTION = 'Multiplayer Light Cycle'
    TICK = 100
    # LIGHT_CYCLE_SIZE must be at least 5
    LIGHT_CYCLE_SIZE = (20.0, 30.0)
    WINDOW_ADJUSTMENT = 3.0
    LIGHT_MIN_SPEED = 5.0
    LIGHT_MAX_SPEED = 20.0
    
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