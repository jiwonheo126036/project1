package com.example.kiosk

import android.content.DialogInterface
import android.content.Intent
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.TextView
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AlertDialog
import com.bumptech.glide.Glide
import com.example.mqtt_ex.Mqtt
import kotlinx.android.synthetic.main.activity_second.*
import kotlinx.android.synthetic.main.dialog.*
import retrofit2.Callback
import retrofit2.Call
import retrofit2.Response
import kotlin.concurrent.timer

private const val SUB_TOPIC = "Android" //받아오기
private const val PUB_COUPON_TOPIC = "iot/coupon" //mqtt로 보내기
private const val PUB_COUNT_TOPIC = "iot/count"
private const val SERVER_URI = "tcp://172.30.1.18:1883"

class SecondActivity : AppCompatActivity() {
    @RequiresApi(Build.VERSION_CODES.M)

    var firstFloor = listOf<String>("hera.png", "lancome.png", "montblanc.png", "gentle+monster.png")
    var secondFloor = listOf<String>("ululemon.png", "isabel+marant.png", "vanessabruno.png", "zadig+and+voltaire.png", "golden+dew.png", "maison+kitsune.png" )
    var thirdFloor = listOf<String>("rockport.png", "luxottica.png", "time+homme.png")
    var fourthFloor = listOf<String>("louis+poulsen.png")
    var fifthFloor = listOf<String>("dyson.png", "balmuda.png")
    var sixthFloor = listOf<String>("balmuda.png", "alt1.png", "alt2.png")
    var b1Floor = listOf<String>("williams+sonoma.png", "dairy+boutique.png", "nutritionist.png")
    var b2Floor = listOf<String>("tissot.png", "nike.png")
    private val api = RetrofitService.create()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_second)

        val ctx = this

        lateinit var msg : String

        val urlPath : String = intent.getStringExtra("info_data").toString()

        val mqttClient: Mqtt = Mqtt(this, SERVER_URI)
        try {
            // mqttClient.setCallback { topic, message ->}

            mqttClient.connect(arrayOf<String>(SUB_TOPIC))

        } catch (e: Exception) {
            e.printStackTrace()
        }

        Log.i("Mqtt_result", "intent 넘겨준 데이터 값 : $urlPath")

        val urlContainer = MyImage(null)

        val data = PostImage(kiosk_id = 1, face_image = urlPath)
        api.postImagePath(data).enqueue(object : Callback<ImageUrlData> {
            override fun onResponse(
                call: Call<ImageUrlData>,
                response: Response<ImageUrlData>
            ){
                val urlList = response.body()?.url_list?.let { ArrayList(it) }
                Log.d("url_list2", response.headers().toString())
//                Log.d("url_list2", urlList.toString())
//                Log.d("url_list2", response.body().toString())
//                Log.d("url_list2", response.code().toString())

                urlContainer.imageurl = urlList

                Log.d("Adapter Code", "had got entered")

                Glide.with(ctx)
                    .load(urlContainer.imageurl?.get(0))
                    .into(img_ad1)


                Glide.with(ctx)
                    .load(urlContainer.imageurl?.get(1))
                    .into(img_ad2)


                Glide.with(ctx)
                    .load(urlContainer.imageurl?.get(2))
                    .into(img_ad3)


                Glide.with(ctx)
                    .load(urlContainer.imageurl?.get(3))
                    .into(img_ad4)


                Glide.with(ctx)
                    .load(urlContainer.imageurl?.get(4))
                    .into(img_ad5)


                Glide.with(ctx)
                    .load(urlContainer.imageurl?.get(5))
                    .into(img_ad6)
            }

            override fun onFailure(call: Call<ImageUrlData>, t: Throwable) {
                Log.d("log", t.toString())
                Log.d("log", "fail")
            }

        })


        val secondSetter = SecondSetter(0)

        val t= timer(period = 1000, initialDelay = 1000){
            secondSetter.second += 1
            Log.i("Mqtt_result", "timer" + secondSetter.second.toString())
            if (secondSetter.second == 40) {
                goMain()
                cancel()
            }
        }


        img_floor.setImageResource(R.drawable.dep_basement_2)
        img_floor.setOnClickListener{
            secondSetter.second = 0
        }

        btn_b2.setOnClickListener{
            img_floor.setImageResource(R.drawable.dep_basement_2)
            secondSetter.second = 0
            check(btn_b2)
        }
        btn_b1.setOnClickListener{
            img_floor.setImageResource(R.drawable.dep_basement_1)
            secondSetter.second = 0
            check(btn_b1)
        }
        btn_1.setOnClickListener{
            img_floor.setImageResource(R.drawable.dep_1)
            secondSetter.second = 0
            check(btn_1)
        }
        btn_2.setOnClickListener{
            img_floor.setImageResource(R.drawable.dep_2)
            secondSetter.second = 0
            check(btn_2)
        }
        btn_3.setOnClickListener{
            img_floor.setImageResource(R.drawable.dep_3)
            secondSetter.second = 0
            check(btn_3)
        }
        btn_4.setOnClickListener{
            img_floor.setImageResource(R.drawable.dep_4)
            secondSetter.second = 0
            check(btn_4)
        }
        btn_5.setOnClickListener{
            img_floor.setImageResource(R.drawable.dep_5)
            secondSetter.second = 0
            check(btn_5)
        }
        btn_6.setOnClickListener{
            img_floor.setImageResource(R.drawable.dep_6)
            secondSetter.second = 0
            check(btn_6)
        }

        btn_back.setOnClickListener {
            t.cancel()
            finish()

        }

        img_ad1.setOnClickListener{

            Log.i("Mqtt_result", mqttClient.toString())
            mqttClient.publish(PUB_COUNT_TOPIC, "ad1_click")
            secondSetter.second = 0

            val storeName : String? = urlContainer.imageurl?.get(0)?.split('/')?.last()

            dialog(mqttClient, secondSetter, storeName)

        }

        img_ad2.setOnClickListener{
            mqttClient.publish(PUB_COUNT_TOPIC, "ad2_click")
            Log.i("Mqtt_result", "전송 > ad2_click ")
            secondSetter.second = 0

            val storeName : String? = urlContainer.imageurl?.get(1)?.split('/')?.last()

            dialog(mqttClient, secondSetter, storeName)
        }

        img_ad3.setOnClickListener{

            mqttClient.publish(PUB_COUNT_TOPIC, "ad3_click")
            Log.i("Mqtt_result", "전송 > ad3_click ")
            secondSetter.second = 0

            val storeName : String? = urlContainer.imageurl?.get(2)?.split('/')?.last()

            dialog(mqttClient, secondSetter, storeName)

        }
        img_ad4.setOnClickListener{

            mqttClient.publish(PUB_COUNT_TOPIC, "ad4_click")
            Log.i("Mqtt_result", "전송 > ad3_click ")
            secondSetter.second = 0

            val storeName : String? = urlContainer.imageurl?.get(3)?.split('/')?.last()

            dialog(mqttClient, secondSetter, storeName)

        }

        img_ad5.setOnClickListener{

            mqttClient.publish(PUB_COUNT_TOPIC, "ad5_click")
            Log.i("Mqtt_result", "전송 > ad3_click ")
            secondSetter.second = 0

            val storeName : String? = urlContainer.imageurl?.get(4)?.split('/')?.last()

            dialog(mqttClient, secondSetter, storeName)

        }
        img_ad6.setOnClickListener{
            mqttClient.publish(PUB_COUNT_TOPIC, "ad3_click")
            Log.i("Mqtt_result", "전송 > ad3_click ")
            secondSetter.second = 0

            val storeName : String? = urlContainer.imageurl?.get(5)?.split('/')?.last()

            dialog(mqttClient, secondSetter, storeName)

        }
    }

    class SecondSetter(sec : Int){
        var second = sec
    }

    fun dialog(mqttClient : Mqtt, second : SecondSetter, storeName : String?){
        val builder = AlertDialog.Builder(this)
        builder.setTitle("매장 상세 안내도")
        builder.setIcon(R.mipmap.ic_launcher)
        val v1 = layoutInflater.inflate(R.layout.dialog, null)
        builder.setView(v1)

//        if(storeName in firstFloor){
//            img_storelocation.setImageResource(R.drawable.dep_1)
//        }
//        else if(storeName in secondFloor){
//            img_storelocation.setImageResource(R.drawable.dep_2)
//        }
//        else if(storeName in thirdFloor){
//            img_storelocation.setImageResource(R.drawable.dep_3)
//        }
//        else if(storeName in fourthFloor){
//            img_storelocation.setImageResource(R.drawable.dep_4)
//        }
//        else if(storeName in fifthFloor){
//            img_storelocation.setImageResource(R.drawable.dep_5)
//        }
//        else if(storeName in sixthFloor){
//            img_storelocation.setImageResource(R.drawable.dep_6)
//        }
//        else if(storeName in b1Floor){
//            img_storelocation.setImageResource(R.drawable.dep_basement_1)
//        }
//        else {
//            img_storelocation.setImageResource(R.drawable.dep_basement_2)
//        }


        val listener = DialogInterface.OnClickListener{ p0, p1->
            val alert = p0 as AlertDialog
            val edit1 : TextView?= alert.findViewById<TextView>(R.id.edit_phonenum)
            Log.i("Mqtt_result", "핸드폰 번호 입력 > ${edit1?.text}")
            second.second = 0
            val phonenum = edit1?.text.toString()
            mqttClient.publish(PUB_COUPON_TOPIC, phonenum)
            Log.i("Mqtt_result", "핸드폰번호 전송 > $phonenum")
        }

        builder.setPositiveButton("확인", listener)
        builder.setNegativeButton("취소", null)

        val dialog = builder.create()
        dialog.show()

        val display = this.resources.displayMetrics
        val width = display.widthPixels
        val height = display.heightPixels
        Log.i("Mqtt_result", "pixel $width $height")

        dialog.getWindow()?.setLayout(1100, 2000)

        var phoneNum =dialog.edit_phonenum.text.toString()

        dialog.btn1.setOnClickListener{
            phoneNum += "1"
            dialog.edit_phonenum.text = phoneNum
            second.second = 0

        }
        dialog.btn2.setOnClickListener{
            phoneNum += "2"
            dialog.edit_phonenum.text = phoneNum
            second.second = 0

        }
        dialog.btn3.setOnClickListener{
            phoneNum += "3"
            dialog.edit_phonenum.text = phoneNum
            second.second = 0

        }
        dialog.btn4.setOnClickListener{
            phoneNum += "4"
            dialog.edit_phonenum.text = phoneNum
            second.second = 0

        }
        dialog.btn5.setOnClickListener{
            phoneNum += "5"
            dialog.edit_phonenum.text = phoneNum
            second.second = 0

        }
        dialog.btn6.setOnClickListener{
            phoneNum += "6"
            dialog.edit_phonenum.text = phoneNum
            second.second = 0

        }
        dialog.btn7.setOnClickListener{
            phoneNum += "7"
            dialog.edit_phonenum.text = phoneNum
            second.second = 0

        }
        dialog.btn8.setOnClickListener{
            phoneNum += "8"
            dialog.edit_phonenum.text = phoneNum
            second.second = 0

        }
        dialog.btn9.setOnClickListener{
            phoneNum += "9"
            dialog.edit_phonenum.text = phoneNum
            second.second = 0

        }
        dialog.btn0.setOnClickListener{
            phoneNum += "0"
            dialog.edit_phonenum.text = phoneNum
            second.second = 0

        }
        dialog.btn_undo.setOnClickListener{
            val len = (phoneNum.length) - 2
            phoneNum = phoneNum.slice(0..len)
            dialog.edit_phonenum.text = phoneNum
            second.second = 0

        }
    }



    //층수 버튼 눌렀을 때 버튼 한개만 불이 들어오는 기능
    private fun check(btn:Button){

        btn_b2?.isSelected = false
        btn_b1?.isSelected = false
        btn_1?.isSelected = false
        btn_2?.isSelected = false
        btn_3?.isSelected = false
        btn_4?.isSelected = false
        btn_5?.isSelected = false
        btn_6?.isSelected = false

        btn.isSelected = btn.isSelected != true

    }

    //main activity로 돌아가는 함수
    private fun goMain(){

        val intent = Intent(this, MainActivity::class.java)
        startActivity(intent)

    }

    class MyImage(imageUrls: ArrayList<String>?){
        var imageurl = imageUrls
    }

}
