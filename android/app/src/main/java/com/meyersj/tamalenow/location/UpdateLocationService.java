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
import com.meyersj.tamalenow.utilities.Endpoints;
import com.meyersj.tamalenow.utilities.Utils;
import com.squareup.okhttp.Callback;
import com.squareup.okhttp.FormEncodingBuilder;
import com.squareup.okhttp.Headers;
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.RequestBody;
import com.squareup.okhttp.Response;

import java.io.IOException;
import java.util.Date;


public class UpdateLocationService extends Service {

    public final String TAG = getClass().getCanonicalName();

    private TamaleApplication app;
    private TamaleLocationListener listener;
    private OkHttpClient httpClient;


    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onCreate() {
        super.onCreate();

        app = (TamaleApplication) getApplication();

        httpClient = new OkHttpClient();
        listener = new TamaleLocationListener(getApplicationContext(), app.getGPSInterval()) {
            @Override
            public void onLocationChanged(Location location) {
                postLocation(location);
            }
        };
        listener.start();
    }

    @Override
    public void onDestroy() {
        super.onCreate();
        listener.stop();
    }

    public void postLocation(Location location) {
        String date = Utils.dateFormat.format(new Date());
        Log.d(TAG, date);
        RequestBody formBody = new FormEncodingBuilder()
                .add("vendor_id", "test_vendor")
                .add("tstamp", Utils.dateFormat.format(new Date()))
                .add("lat", String.valueOf(location.getLatitude()))
                .add("lon", String.valueOf(location.getLongitude()))
                .build();

        Request request = new Request.Builder()
                .url(app.getAPIBase() + "/" + Endpoints.LOCATION)
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
