# calc_setpoint

## What Does it Do?

`calc_setpoint` adjusts the setpoint of your `climate` device based on a custom temperature sensor.

Many thermostats are not positioned in an ideal location to sense the temperature of the rooms you care about. This adjusts the setpoint according to that measured temperature and its difference from the temperature measured at the Thermostat.

`calc_setpoint` can be used again any temperature sensor. 

This could be a single sensor for a single room.

Or, you can set up a [min/max sensor](https://www.home-assistant.io/integrations/min_max/) to average the temperature in your home.

Or, you can use [calc_conditional_avg](https://github.com/dlashua/pyscript-calc_conditional_avg) to only average the temperatures of occupied rooms.

This app also supports using a separate away temperature.

## Using it!

This works as an "app" in `pyscript`. Therefore, pyscript is required and configuration is done through Home Assistant's `configuration.yaml` file.

You can see a [full configuration example](config.sample.yaml) in this repository.

These are the configuration keys:

key | description | example | default
--- | --- | --- | ---
sensor_temp (required) | the temperature sensor to serve as the reference to compare the actual temperature to. Usually, this is your thermostat's temperature sensor. | climate.hvac.current_temperature | No Default
actual_temp (required) | the temperature sensor to adjust the setpoint to. This is a sensor for a single room in your home, or a sensor that averages many sensors together | sensor.avg_occupied_temperature | No Default
occupied (optional) | A sensor that should have a state of `on` when the `desired_temp` should be used | binary_sensor.occupied | No Default
desired_temp (required) | An entity to provide the desired temperature for the thermostat. Do not use your thermostat's setpoint as this app will change the setpoint to compenstate for temperature differences | input_number.desired_temperature | No Default
away_temp (optional) | Same as `desired_temp` but used when `occupied` is not `on` | input_number.away_temperature | No Default
climate_entity (required) | The entity_id of the climate device with the setpoint that should be managed | climate.hvac | No Default



## Requirements

* [PyScript custom_component](https://github.com/custom-components/pyscript)

## Install

### Install this script
```
# get to your homeassistant config directory
cd /config

cd pyscript
mkdir -p apps/
cd apps
git clone https://github.com/dlashua/pyscript-calc_setpoint calc_setpoint
```

### Edit `configuration.yaml`

```yaml
pyscript:
  apps:
    calc_setpoint:
      - sensor_temp: climate.hvac.current_temperature
        actual_temp: sensor.avg_occupied_temperature
        occupied: binary_sensor.occupied
        desired_temp: input_number.desired_temperature
        away_temp: input_number.away_temperature
        climate_entity: climate.hvac
```

### Reload PyScript
