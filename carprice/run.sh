#!/bin/bash

my_array=('allcars.com',
        'autonation.com',
        'autotrader.com',
        'carbrain.com',
        'carfax.com',
        'cargurus.com',
        'carmax.com',
        'cars.com',
        'carsforsale.com',
        'carvana.com',
        'carvana.io',
        'driveway.com',
        'edmunds.com',
        'herbchambers.com',
        'kbb.com',
        'ksl.com',
        'peddle.com',
        'sellmax.com',
        'shift.com',
        'truecar.com',
        'azcarcentral.com',
        'webuyanycarusa.com',
        'www.vroom.com',
        'www.wheelzy.com',)

echo ${my_array[@]} | sed 's/\</-/g'