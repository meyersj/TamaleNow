package com.meyersj.tamalenow;

import android.app.Application;
import android.content.res.AssetManager;
import android.content.res.Configuration;
import android.content.res.Resources;

import com.meyersj.tamalenow.utilities.PropKeys;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;


public class TamaleApplication extends Application {

    private static TamaleApplication singleton;
    private Properties properties;

    public TamaleApplication getInstance() {
        return singleton;
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
    }

    @Override
    public void onCreate() {
        super.onCreate();
        singleton = this;
        readProperties();
    }

    @Override
    public void onLowMemory() {
        super.onLowMemory();
    }

    @Override
    public void onTerminate() {
        super.onTerminate();
    }

    private void readProperties() {
        Resources resources = this.getResources();
        AssetManager assetManager = resources.getAssets();

        // read properties from /assets directory
        try {
            InputStream inputStream = assetManager.open("config.properties");
            properties = new Properties();
            properties.load(inputStream);
        } catch (IOException e) {

            e.printStackTrace();
        }
    }

    public String getToken() {
        return properties.getProperty(PropKeys.MAPBOX_TOKEN, "");
    }

    public String getMapID() {
        return properties.getProperty(PropKeys.MAP_ID, "");
    }

    public Long getGPSInterval() {
        return Long.valueOf(properties.getProperty(PropKeys.GPS_INTERVAL, "")) * 1000;
    }

}
