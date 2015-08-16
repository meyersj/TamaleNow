package com.meyersj.tamalenow.location;

import android.content.Context;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;

import com.mapbox.mapboxsdk.geometry.LatLng;


public class TamaleLocationListener implements LocationListener {

    private LocationManager locationManager;
    private Long gpsInterval;


    public TamaleLocationListener(Context context, Long gpsInterval) {
        this.gpsInterval = gpsInterval;
        locationManager = (LocationManager) context.getSystemService(context.LOCATION_SERVICE);

    }

    public LatLng getLatLng(Location location) {
        return new LatLng(location.getLatitude(), location.getLongitude());
    }

    @Override
    public void onLocationChanged(Location location) {

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

    public void start() {
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, gpsInterval, 20, this);
    }

    public void stop() {
        locationManager.removeUpdates(this);
    }

}