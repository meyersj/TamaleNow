/*
 * Copyright (c) 2015 Jeffrey Meyers
 *
 * This program is released under the "MIT License".
 * Please see the file COPYING in this distribution for license terms.
 */

package com.meyersj.tamalenow;

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
import com.mapbox.mapboxsdk.overlay.Marker;
import com.mapbox.mapboxsdk.tileprovider.tilesource.MapboxTileLayer;
import com.mapbox.mapboxsdk.views.MapView;
import com.meyersj.tamalenow.location.TamaleLocationListener;
import com.meyersj.tamalenow.location.UpdateLocationService;
import com.meyersj.tamalenow.utilities.Endpoints;
import com.squareup.okhttp.Callback;
import com.squareup.okhttp.FormEncodingBuilder;
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.RequestBody;
import com.squareup.okhttp.Response;

import java.io.IOException;

import butterknife.Bind;
import butterknife.ButterKnife;


public class MapActivity extends AppCompatActivity {

    private final String TAG = getClass().getCanonicalName();
    private final String VENDOR = "test_vendor";

    private TamaleApplication app;
    private Boolean isReporting = false;
    private TamaleLocationListener gpsListener;
    private Marker locationMarker;
    private OkHttpClient httpClient;


    @Bind(R.id.mapview) MapView mapView;
    @Bind(R.id.toggle_reporting) Button toggleReporting;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_map);
        ButterKnife.bind(this);
        app = (TamaleApplication) getApplication();
        httpClient = new OkHttpClient();
        setTiles();
        setGPSListener();
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
        mapView.setZoom(16);
        LatLng portland = new LatLng(45.52, -122.681944);
        mapView.setCenter(portland, true);

    }

    private void setGPSListener() {
        gpsListener = new TamaleLocationListener(this, app.getGPSInterval()) {
            @Override
            public void onLocationChanged(Location location) {
                Log.d(TAG, "listener: " + location.toString());
                LatLng latLng = this.getLatLng(location);
                if (locationMarker == null) {
                    locationMarker = new Marker(mapView, "title", "desc", latLng);
                    mapView.addMarker(locationMarker);
                }
                else {
                    locationMarker.setPoint(latLng);
                }
                mapView.setCenter(latLng);
            }
        };
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
        toggleReporting.setText(R.string.stop_reporting);
        isReporting = true;
        updateStatus(VENDOR, true);
        gpsListener.start();
        Intent intent = new Intent(getApplicationContext(), UpdateLocationService.class);
        startService(intent);
    }

    private void stopReporting() {
        toggleReporting.setText(R.string.start_reporting);
        isReporting = false;
        updateStatus(VENDOR, false);
        gpsListener.stop();
        mapView.removeMarker(locationMarker);
        locationMarker = null;
        Intent intent = new Intent(getApplicationContext(), UpdateLocationService.class);
        stopService(intent);
    }

    private void updateStatus(String vendorID, Boolean newStatus) {

        RequestBody formBody = new FormEncodingBuilder()
                .add("vendor_id", vendorID)
                .add("active", newStatus.toString())
                .build();

        Request request = new Request.Builder()
                .url(app.getAPIBase() + "/" + Endpoints.ACTIVE)
                .post(formBody)
                .build();

        httpClient.newCall(request).enqueue(new Callback() {

            @Override
            public void onFailure(Request request, IOException e) {
                Log.d(TAG, "failure");
            }

            @Override
            public void onResponse(Response response) throws IOException {
                if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);
                Log.d(TAG, response.body().string());
            }
        });
    }


}