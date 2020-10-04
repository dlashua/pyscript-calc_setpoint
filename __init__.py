def calc_setpoint(**data):
    climate_entity = data.get('climate_entity')
    if climate_entity is None:
        log.error('climate_entity is required')
        return

    task.unique('calc_setpoint_{}'.format(climate_entity))

    occupied_sensor = data.get('occupied')
    if occupied_sensor is None:
        occupied = True
    else:
        occupied = (state.get(occupied_sensor) == 'on')

    desired_temp_sensor = data.get('desired_temp')
    if desired_temp_sensor is None:
        log.error(f'{climate_entity}: desired_temp is required')
        return
    
    try:
        desired_temp = float(state.get(desired_temp_sensor))
    except:
        log.error(f'{climate_entity}: Unable to get desired_temp')
        return

    away_temp_sensor = data.get('away_temp')
    if away_temp_sensor is None:
        occupied = True
    else:
        try:
            away_temp = float(state.get(away_temp_sensor))
        except:
            log.error(f'{climate_entity}: Unable to get away_temp')
            return

    sensor_temp_sensor = data.get('sensor_temp')
    if sensor_temp_sensor is None:
        log.error(f'{climate_entity}: sensor_temp is required')
        return
    
    try:
        sensor_temp = float(state.get(sensor_temp_sensor))
    except:
        log.error(f'{climate_entity}: Unable to get sensor_temp')
        return
     

    actual_temp_sensor = data.get('actual_temp')
    if actual_temp_sensor is None:
        log.error(f'{climate_entity}: actual_temp is required')
        return

    try:
        actual_temp = float(state.get(actual_temp_sensor))
    except:
        log.error(f'{climate_entity}: Unable to get actual_temp')
        return

    try:
        current_setpoint = float(state.get_attr(climate_entity)['temperature'])
    except:
        log.error(f'{climate_entity}: Unable to get current setpoint from climate_entity')
        return

    if occupied:
        set_temp = desired_temp
    else:
        set_temp = away_temp

    temp_diff = round(actual_temp - sensor_temp, 1)
    setpoint = round(set_temp - temp_diff)
    if setpoint != current_setpoint:
        # wait for any other updates to come in
        log.debug(f'{climate_entity}: waiting for more updates')
        task.sleep(10)

        log.info(f'{climate_entity}: SETPOINT {setpoint}, DESIRED: {set_temp}, DIFF: {temp_diff}, ACTUAL: {actual_temp}, SENSOR: {sensor_temp}')
        climate.set_temperature(
            entity_id=climate_entity,
            temperature=setpoint,
        )
    else:
        log.debug(f'{climate_entity}: ALREADY AT {setpoint}, DESIRED: {set_temp}, DIFF: {temp_diff}, ACTUAL: {actual_temp}, SENSOR: {sensor_temp}')

registered_triggers = []

def register_calc_setpoint(data):
    watch_entities = []
    for key in data:
        # skip these
        if key in ['app']:
            continue

        value = data[key]
        if value in watch_entities:
            continue

        watch_entities.append(value)

    @time_trigger("startup")
    @state_trigger('True or {}'.format(" or ".join(watch_entities)))
    def inner_function():
        nonlocal data
        calc_setpoint(**data)

    registered_triggers.append(inner_function)   

##########
# Helpers
##########
def load_app(app_name, factory):
    if "apps" not in pyscript.config:
        return
    
    if app_name not in pyscript.config['apps']:
        return

    for app in pyscript.config['apps'][app_name]:
        log.info(f'loading {app_name} app with config {app}')
        factory(app)

def load_app_list(app_name, factory):
    if "apps_list" not in pyscript.config:
        return

    for app in pyscript.config['apps_list']:
        if 'app' not in app:
            continue
    
        if app['app'] == app_name:
            factory(app)

##########
# Startup
##########
load_app("calc_setpoint", register_calc_setpoint)
load_app_list("calc_setpoint", register_calc_setpoint)

