package com.example.kiosk

import android.content.Context
import android.content.Intent
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.mqtt_ex.Mqtt
import org.eclipse.paho.client.mqttv3.MqttMessage

private const val PUB_TOPIC = "iot/capture" //mqtt로 보내기


class MainDataPagerAdapter(private val context: Context, private val items: ArrayList<String>, private val mqttClient:Mqtt) :
    RecyclerView.Adapter<MainDataPagerAdapter.PagerViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) : MainDataPagerAdapter.PagerViewHolder {



        val view =
            LayoutInflater.from(parent.context).inflate(R.layout.fragment_photo, parent, false)
        return PagerViewHolder(view).apply {
            view.setOnClickListener {

                mqttClient.publish(PUB_TOPIC, "touch_screen")
                Log.i("Mqtt_result", "전송 > touch screen ")

            }
        }


    }

    override fun getItemCount(): Int = items.size

    override fun onBindViewHolder(holder: PagerViewHolder, position: Int) {
        Glide.with(context).load(items[position]).into(holder.imageUrl)
    }

    class PagerViewHolder(view: View) : RecyclerView.ViewHolder(view){
        val imageUrl : ImageView = view.findViewById(R.id.mainSlideImage)
    }

}