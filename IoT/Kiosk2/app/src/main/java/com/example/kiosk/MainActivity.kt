package com.example.kiosk

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.example.mqtt_ex.Mqtt
import kotlinx.android.synthetic.main.activity_main.*
import android.util.Log
import androidx.annotation.RequiresApi
import androidx.viewpager2.widget.ViewPager2
import org.eclipse.paho.client.mqttv3.MqttMessage
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Call
import kotlin.concurrent.timer

private const val SUB_TOPIC = "Android" //받아오기
private const val PUB_TOPIC = "iot/capture" //mqtt로 보내기
private const val SERVER_URI = "tcp://172.30.1.18:1883"
var file_path = ""
class MainActivity : AppCompatActivity() {

    lateinit var mqttClient: Mqtt

    private val api = RetrofitService.create()

    val ctx = this

    @RequiresApi(Build.VERSION_CODES.O)
    @SuppressLint("ClickableViewAccessibility")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        mqttClient = Mqtt(this, SERVER_URI)
        try {
            mqttClient.setCallback { topic, message ->}
            mqttClient.setCallback(::onReceived)
            mqttClient.connect(arrayOf<String>(SUB_TOPIC))

        } catch (e: Exception) {
            e.printStackTrace()
        }

        val urlContainer = MyImage(null)

        api.getImagePath().enqueue(object : Callback<ImageUrlData> {
            override fun onResponse(
                call: Call<ImageUrlData>,
                response: Response<ImageUrlData>
            ) {
                val urlList = response.body()?.url_list?.let { ArrayList(it) }
                Log.d("url_list", urlList.toString())

                urlContainer.imageurl = urlList

                Log.d("Adapter Code", "had got entered")
                main_ad.adapter = urlContainer.imageurl?.let { MainDataPagerAdapter(ctx, it, mqttClient) }
                main_ad.orientation = ViewPager2.ORIENTATION_HORIZONTAL // 방향을 가로로

                timer(period = 3000) {
                    runOnUiThread {
                        main_ad.currentItem = (main_ad.currentItem + 1) % urlContainer.imageurl!!.size
                    }
                }
            }

            override fun onFailure(call: Call<ImageUrlData>, t: Throwable) {
                Log.d("log", t.toString())
                Log.d("log", "fail")
            }
        })



        main_btn.setOnClickListener {
            val intent = Intent(this, SecondActivity::class.java)
            mqttClient.publish(PUB_TOPIC, "touch_screen")

            Log.i("Mqtt_result", "전송 > touch screen ")

        }

        //viewpager 자동으로 넘어가기

    }


    fun onReceived(topic: String?, message: MqttMessage) {
        // 토픽 수신 처리
        val msg = String(message.payload)
//        Log.i("Mqtt_result","수신메세지: $msg")
        file_path = msg //문자열, 비트
        //알람

        val intent = Intent(this, SecondActivity::class.java)
        intent.putExtra("info_data", file_path)
        startActivity(intent)
    }

    class MyImage(imageUrls: ArrayList<String>?){
        var imageurl = imageUrls
    }
}

