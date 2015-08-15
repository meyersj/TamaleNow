/*
 * Copyright (c) 2015 Jeffrey Meyers
 *
 * This program is released under the "MIT License".
 * Please see the file COPYING in this distribution for license terms.
 */

package com.meyersj.tamalenow.location;


import android.app.Service;
import android.content.Intent;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;

import com.meyersj.tamalenow.TamaleApplication;


public class UpdateLocationService extends Service {

    public final String TAG = getClass().getCanonicalName();
    LocListener listener;
    LocationManager locationManager;

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onCreate() {
        super.onCreate();
        Long gpsInterval = ((TamaleApplication) getApplication()).getGPSInterval();

        listener = new LocListener();
        locationManager = (LocationManager) getApplicationContext()
                .getSystemService(getApplicationContext().LOCATION_SERVICE);
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER,
                gpsInterval, 20, listener);

    }

    @Override
    public void onDestroy() {
        super.onCreate();
        locationManager.removeUpdates(listener);
    }


    public class LocListener implements LocationListener {

        @Override
        public void onLocationChanged(Location location) {
            Log.d(TAG, location.toString());
        }

        @Override
        public void onStatusChanged(String provider, int status, Bundle extras) {

        }

        @Override
        public void onProviderEnabled(String provider) {

        }

        @Override
        public void onProviderDisabled(String provider) {

        }
    }
}
