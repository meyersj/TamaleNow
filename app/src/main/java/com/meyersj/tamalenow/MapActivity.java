/*
 * Copyright (c) 2015 Jeffrey Meyers
 *
 * This program is released under the "MIT License".
 * Please see the file COPYING in this distribution for license terms.
 */

package com.meyersj.tamalenow;

import android.content.Context;
import android.content.Intent;
import android.location.Location;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;

import com.mapbox.mapboxsdk.geometry.LatLng;
import com.mapbox.mapboxsdk.overlay.GpsLocationProvider;
import com.mapbox.mapboxsdk.overlay.UserLocationOverlay;
import com.mapbox.mapboxsdk.tileprovider.tilesource.MapboxTileLayer;
import com.mapbox.mapboxsdk.views.MapView;
import com.meyersj.tamalenow.location.UpdateLocationService;


import butterknife.Bind;
import butterknife.ButterKnife;


public class MapActivity extends AppCompatActivity {

    private TamaleApplication app;
    private Boolean isReporting = false;
    private UserLocationOverlay locationOverlay;

    @Bind(R.id.mapview) MapView mapView;
    @Bind(R.id.toggle_reporting) Button toggleReporting;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_map);
        ButterKnife.bind(this);
        app = (TamaleApplication) getApplication();
        setTiles();
        setGPSProvider();

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_landing, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    private void setTiles() {
        mapView.setAccessToken(app.getToken());
        mapView.setTileSource(new MapboxTileLayer(app.getMapID()));
        mapView.setZoom(13);
        mapView.setCenter(new LatLng(45.52, -122.681944), true);
    }

    private void setGPSProvider() {
        GpsLocationProvider provider = new GPSProvider(this, app.getGPSInterval());
        provider.setLocationUpdateMinTime(app.getGPSInterval());
        locationOverlay = new UserLocationOverlay(provider, mapView);
    }

    public void onToggleReporting(View view) {
        if(!isReporting) {
            startReporting();
        }
        else {
            stopReporting();
        }
    }

    public void startReporting() {
        isReporting = true;
        toggleReporting.setText(R.string.stop_reporting);
        locationOverlay.enableMyLocation();
        locationOverlay.setDrawAccuracyEnabled(true);
        mapView.getOverlays().add(locationOverlay);
        Intent intent = new Intent(getApplicationContext(), UpdateLocationService.class);
        startService(intent);
    }

    private void stopReporting() {
        isReporting = false;
        toggleReporting.setText(R.string.start_reporting);
        locationOverlay.disableMyLocation();
        locationOverlay.setDrawAccuracyEnabled(false);
        mapView.getOverlays().remove(locationOverlay);
        Intent intent = new Intent(getApplicationContext(), UpdateLocationService.class);
        stopService(intent);
    }

    public class GPSProvider extends GpsLocationProvider {

        public GPSProvider(Context context, Long gpsInterval) {
            super(context);
            this.setLocationUpdateMinTime(gpsInterval);
        }

        @Override
        public void onLocationChanged(Location location) {
            LatLng latLng = new LatLng(location.getLatitude(), location.getLongitude());
            mapView.setCenter(latLng, true);
        }
    }

}